# Survived Mutants: Codex zlib PBT Suite

`mutmut results`

```text
codex_zlib_mutation_testing
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `zlib_target.py` | 3 | 0 |

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible API behavior that should be caught by a targeted example. |
| Medium | The mutation changes a forwarded option or wrapper contract, but normal round-trip properties may not observe it. |
| Low | The mutation probably does not change decompressed output and may only affect performance or allocation behavior. |

Overall confidence in the current Codex zlib mutation quality: **Medium-High**.

The tests strongly cover the most important user-visible behavior: compressed
data round-trips through decompression, decompression is deterministic, and
Adler-32 matches an independent rolling-checksum implementation. The remaining
survivors are mostly wrapper-boundary issues where an argument is ignored but
the broad property still passes.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `compress` option forwarding | 1 | Medium | Ignoring the explicit `level` argument still round-trips, so tests need to compare the wrapper against stdlib output for explicit options. |
| `decompress` buffer-size forwarding | 1 | Low-Medium | Ignoring `bufsize` usually does not change decompressed bytes, so this is mostly an adapter-contract or performance-sensitive survivor. |
| `adler32` default seed | 1 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Changing the default seed from `1` to `2` is externally visible and should be killed by a direct default-vs-explicit assertion. |

## Example Survived Mutants

### 1. Compression level argument dropped

**Mutant:** `zlib_target.x_compress__mutmut_5`

```diff
-    return _zlib.compress(data, level=level, wbits=wbits)
+    return _zlib.compress(data, wbits=wbits)
```

**Why it survived:** The current tests check that compressed data round-trips
and that compression is deterministic. Those properties still hold if the
wrapper ignores a non-default `level`, because the compressed stream is still
valid and decompresses to the original bytes.

**Confidence:** Medium.

**Targeted test idea:** Compare the adapter directly against stdlib for
explicit levels, for example
`zlib_target.compress(data, level=0, wbits=15) == zlib.compress(data, level=0, wbits=15)`.
Use fixed payloads where level differences are observable, such as repeated
bytes.

### 2. Decompression buffer-size argument dropped

**Mutant:** `zlib_target.x_decompress__mutmut_6`

```diff
-    return _zlib.decompress(data, wbits=wbits, bufsize=bufsize)
+    return _zlib.decompress(data, wbits=wbits, )
```

**Why it survived:** `bufsize` controls the initial output-buffer size, but it
does not normally change the final decompressed bytes. Since the tests mainly
assert byte-for-byte decompression results, this mutation can survive without
indicating a serious functional gap.

**Confidence:** Low-Medium.

**Targeted test idea:** If wrapper fidelity is important, monkeypatch or wrap
the underlying `_zlib.decompress` call to assert that the adapter forwards
`bufsize`. Otherwise, this survivor is lower priority because the public result
is unchanged.

### 3. Adler-32 default seed changed

**Mutant:** `zlib_target.x_adler32__mutmut_1`

```diff
-def adler32(data, value=1):
+def adler32(data, value=2):
```

**Why it survived:** Adler-32 uses `1` as the documented default starting value.
Changing it to `2` changes results for default calls. The current wrapper appears
to include `zlib.adler32(first) == zlib.adler32(first, 1)`, so this survivor
should be verified with a fresh mutation run. If it still survives, the likely
issue is stale mutation state or test discovery/import configuration.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact defaults on fixed examples:
`zlib_target.adler32(b"") == 1` and
`zlib_target.adler32(b"abc") == zlib.adler32(b"abc", 1)`.

## Overall Assessment

The zlib suite is in relatively good shape because its properties validate the
core semantic contracts. The remaining gaps are adapter-specific:

1. Explicit compression options should be compared against stdlib, not only
   checked by round-trip decompression.
2. Adler-32 default-seed behavior should be confirmed after a fresh mutation
   run, because the current test logic should kill that mutant.
3. `bufsize` forwarding is lower priority unless the goal is exact wrapper
   fidelity rather than only decompressed output correctness.
s