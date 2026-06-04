# Survived Mutants: Codex html PBT Suite

`mutmut browse`

```text
codex_html_mutation_testing
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `html/__init__.py` | 12 | 0 |

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible escaping or unescaping behavior that should be caught by a targeted example. |
| Medium | The mutation could matter, but only for uncommon HTML character-reference forms or boundary values. |
| Low | The mutation probably does not change observable behavior for realistic inputs. |

Overall confidence in the current Codex html mutation quality: **Medium-High**.

The tests strongly exercise normal `escape()` behavior and common `unescape()`
round trips, but the surviving mutants show weaker pressure on decoder edge
cases: uppercase hexadecimal references, optional semicolon handling, surrogate
boundaries, out-of-range code points, and invalid numeric references.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `escape` default quote behavior | 1 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The default `quote=True` behavior should be explicitly asserted and mutation results should be rerun if this still survives. |
| `_replace_charref` numeric parsing | 4 | Medium | Hex/decimal parsing and optional semicolon stripping need direct examples beyond ordinary valid references. |
| `_replace_charref` invalid Unicode boundaries | 7 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Surrogate and out-of-range references are externally visible and should return replacement characters or empty strings exactly. |

## Example Survived Mutants

### 1. Default quote escaping changed

**Mutant:** `html.x_escape__mutmut_1`

```diff
-def escape(s, quote=True):
+def escape(s, quote=False):
```

**Why it survived:** This changes the documented default behavior of
`html.escape()`: double and single quotes should be escaped when `quote` is not
provided. The current wrapper appears to include a direct default-quote check, so
this survivor should be rerun and verified. If it still survives after a fresh
mutation run, the likely issue is stale mutation state or test discovery/import
configuration rather than a missing assertion.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact output for default calls such as
`html.escape('"\'&<>') == '&quot;&#x27;&amp;&lt;&gt;'`.

### 2. Uppercase hexadecimal numeric references are not distinguished

**Mutant:** `html.x__replace_charref__mutmut_10`

```diff
-        if s[1] in 'xX':
+        if s[1] in 'xx':
```

**Why it survived:** The unescape tests cover valid numeric references, but do
not appear to require both lowercase `&#x...;` and uppercase `&#X...;` forms.
This mutation makes uppercase hexadecimal references follow the decimal parsing
path instead.

**Confidence:** Medium.

**Targeted test idea:** Assert `html.unescape('&#x41;') == 'A'` and
`html.unescape('&#X41;') == 'A'`.

### 3. Optional semicolon stripping changed

**Mutant:** `html.x__replace_charref__mutmut_20`

```diff
-            num = int(s[2:].rstrip(';'), 16)
+            num = int(s[2:].rstrip('XX;XX'), 16)
```

**Why it survived:** The decoder accepts some numeric references with and
without semicolons. This mutation changes which trailing characters are stripped
before parsing, but the tests mostly check standard semicolon-terminated
references.

**Confidence:** Medium.

**Targeted test idea:** Add paired examples for semicolon and non-semicolon
forms, such as `&#65;`, `&#65`, `&#x41;`, and `&#x41`.

### 4. Surrogate and out-of-range handling weakened

**Mutant:** `html.x__replace_charref__mutmut_29`

```diff
-        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
+        if 0xD800 <= num <= 0xDFFF and num > 0x10FFFF:
```

**Why it survived:** The tests avoid invalid Unicode categories when generating
valid character references, so they do not assert the documented replacement
behavior for surrogate code points or values above the Unicode maximum.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact replacement behavior for examples such as
`html.unescape('&#xD800;') == '\uFFFD'` and
`html.unescape('&#x110000;') == '\uFFFD'`.

### 5. Boundary values around surrogate limits survived

**Mutants:** `html.x__replace_charref__mutmut_30`,
`html.x__replace_charref__mutmut_31`, `html.x__replace_charref__mutmut_32`,
`html.x__replace_charref__mutmut_33`, `html.x__replace_charref__mutmut_34`,
`html.x__replace_charref__mutmut_35`

```diff
-        if 0xD800 <= num <= 0xDFFF or num > 0x10FFFF:
+        if 0xD800 < num <= 0xDFFF or num > 0x10FFFF:
```

**Why it survived:** These mutants alter inclusive/exclusive boundary checks for
surrogate code points and the maximum valid Unicode code point. The existing
tests generate ordinary valid characters, but do not target the exact invalid
boundaries.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add boundary examples for `0xD7FF`, `0xD800`,
`0xDFFF`, `0xE000`, `0x10FFFF`, and `0x110000`, checking whether each should
produce the original character or `'\uFFFD'`.

## Overall Assessment

The surviving mutants point to missing precision on
documented edge behavior:

1. Default quote escaping for `html.escape()` should be verified after a fresh
   mutation run.
2. Uppercase hexadecimal references and optional-semicolon numeric references
   need exact output checks.
3. Invalid numeric references need targeted assertions for surrogates,
   noncharacters, control characters, and values above `0x10FFFF`.
