# Survived Mutants: Codex numpy PBT Suite

`mutmut browse`

```text
codex_np_mutation_testing
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `numpy/_core/fromnumeric.py` | 22 | 0 |
| `numpy/_core/multiarray.py` | 6 | 0 |
| `numpy/linalg/_linalg.py` | 21 | 1 |

The mutation target includes the Python-facing NumPy helpers for `sum`,
`cumsum`, `dot`, and `linalg.norm`. `np.add` is a compiled ufunc, so mutmut
cannot directly mutate the real arithmetic implementation; its wrapper test is
still part of the selected pytest suite.

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible behavior of one of the documented target APIs and should be caught by a targeted property or fixed example. |
| Medium | The mutant changes dispatch, subclass, dtype, or validation behavior that matters for NumPy compatibility, but may not be reached by ordinary ndarray inputs. |
| Low | The mutant is outside the target API behavior, likely equivalent for generated inputs, or only affects metadata/internal setup. |

Overall confidence in the current Codex numpy mutation quality: **Medium**.

The tests are strong for ordinary ndarray semantics: `sum` has an independent
manual oracle, `cumsum` checks prefix-difference behavior, `dot` checks the
documented sum-product cases, and `linalg.norm` covers many vector and matrix
norm formulas. The survivors mostly show weaker coverage of NumPy dispatch
machinery, subclass behavior, invalid-shape error paths, and linalg helper
branches. There is also some oracle coupling: several expected-value helpers
use NumPy operations such as `np.sum`, `np.add.accumulate`, `np.linalg.svd`,
`np.max`, and `np.min`, so helper mutations can affect both the implementation
and the expected calculation.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `_wrapfunc` in `fromnumeric.py` | 5 | Medium | `cumsum` dispatch behavior for objects with custom methods/subclasses is weakly tested; plain ndarrays still behave normally. |
| `_wrapreduction` in `fromnumeric.py` | 3 | Medium | `sum` dispatch to object-specific reduction methods is not tested with ndarray subclasses or custom array-likes. |
| `_wrapreduction_any_all` in `fromnumeric.py` | 14 | Low-Medium | These survivors are mostly from helper calls made by the tests, not direct target APIs. They show mutation reached NumPy internals used by test assertions. |
| `_override___module__` in `multiarray.py` | 6 | Low | Metadata/module override logic for ufuncs survived; this does not affect arithmetic results for `np.add` or `np.dot`. |
| `_makearray` in `linalg/_linalg.py` | 6 | Medium | Array wrapping/subclass return behavior is not tested for `linalg.norm`. |
| `_realType` and `_commonType` in `linalg/_linalg.py` | 8 | Medium | Dtype promotion for complex/single-precision inputs is weakly exercised because the tests generate only `float64` norm inputs. |
| `_assert_2d` and `_assert_stacked_square` in `linalg/_linalg.py` | 6 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Matrix validation branches survived, indicating missing tests for invalid dimensionality and non-square matrix-only norms. |
| `_multi_svd_norm` in `linalg/_linalg.py` | 1 | Medium | SVD-based matrix norm behavior is covered for values, but not for internal `compute_uv` forwarding. |
| `_multi_dot_matrix_chain_order` in `linalg/_linalg.py` | 0 survived, 1 untested | Low | `multi_dot` is outside the selected target APIs. |

## Example Survived Mutants

### 1. `cumsum` dispatch to object methods bypassed

**Mutant:** `numpy._core.fromnumeric.x__wrapfunc__mutmut_1`

```diff
-    bound = getattr(obj, method, None)
+    bound = None
```

**Why it survived:** The `cumsum` test uses ordinary `ndarray` inputs. For
those, falling back through NumPy's wrapper path still produces the same prefix
sums. The test does not use an ndarray subclass or array-like object with a
custom `.cumsum()` method, so method dispatch behavior is not observed.

**Confidence:** Medium.

**Targeted test idea:** Add a small custom array-like with a `.cumsum()` method
or an ndarray subclass and assert that `np.cumsum(obj, ...)` dispatches or
preserves wrapping according to NumPy's documented behavior.

### 2. `sum` dispatch to custom reduction removed

**Mutant:** `numpy._core.fromnumeric.x__wrapreduction__mutmut_6`

```diff
-            reduction = getattr(obj, method)
+            reduction = getattr(None, method)
```

**Why it survived:** The `sum` test is strong for numeric ndarray values, axes,
`dtype`, `keepdims`, `initial`, `where`, and `out`. This mutant affects the path
for non-ndarray objects that provide their own reduction method. Since generated
inputs are plain ndarrays, NumPy still reaches `ufunc.reduce` and the tested
numeric behavior remains correct.

**Confidence:** Medium.

**Targeted test idea:** Include a minimal class or ndarray subclass with a
custom `sum` method and verify that `np.sum` calls it with non-default
arguments such as `axis`, `out`, and `keepdims`.

### 3. `any`/`all` reduction axis changed

**Mutant:** `numpy._core.fromnumeric.x__wrapreduction_any_all__mutmut_10`

```diff
-            return reduction(axis=axis, out=out, **passkwargs)
+            return reduction(axis=None, out=out, **passkwargs)
```

**Why it survived:** This is not a direct target API. It appears in the mutation
set because the wrapper tests and expected-value helpers call NumPy predicates
such as `np.all` while checking outputs. A mutation in `any`/`all` dispatch can
survive if the generated assertions do not rely on subclass-specific
axis-preserving behavior.

**Confidence:** Low-Medium.

**Targeted test idea:** Do not prioritize this for the five target functions
unless the goal is broad NumPy helper coverage. If kept in scope, add direct
`np.all(..., axis=...)` or subclass dispatch checks.

### 4. Ufunc module metadata override broken

**Mutant:** `numpy._core.multiarray.x__override___module____mutmut_1`

```diff
-    namespace_names = globals()
+    namespace_names = None
```

**Why it survived:** The `np.add` wrapper checks arithmetic properties such as
shape, commutativity, zero identity, and dtype promotion. This mutant affects
module metadata override setup for ufunc objects rather than the compiled ufunc
addition behavior. It does not change `np.add(a, b)` results for ordinary
arrays.

**Confidence:** Low.

**Targeted test idea:** Only test this if metadata compatibility is in scope,
for example asserting `np.add.__module__ == "numpy"` after import.

### 5. `linalg.norm` array wrapping ignored

**Mutant:** `numpy.linalg._linalg.x__makearray__mutmut_3`

```diff
-    wrap = getattr(a, "__array_wrap__", new.__array_wrap__)
+    wrap = None
```

**Why it survived:** The norm tests generate plain `float64` ndarrays. They do
not check ndarray subclasses, matrix subclasses, or objects with custom
`__array_wrap__`. Numeric norm values are still correct for ordinary arrays, so
the wrapper contract is not exercised.

**Confidence:** Medium.

**Targeted test idea:** Add an ndarray subclass case and assert that
`np.linalg.norm` preserves or handles wrapping as expected for scalar and
reduced-array results.

### 6. Linalg real dtype default changed

**Mutant:** `numpy.linalg._linalg.x__realType__mutmut_2`

```diff
-    return _real_types_map.get(t, default)
+    return _real_types_map.get(t, None)
```

**Why it survived:** The current `linalg.norm` generation uses `float64`
arrays, so dtype mapping edge cases for single precision, complex inputs, and
unknown dtypes are mostly absent. The computed values can remain correct for
the generated domain.

**Confidence:** Medium.

**Targeted test idea:** Generate `float32`, `complex64`, and `complex128`
inputs, then assert both numeric results and output dtype/precision behavior for
vector and matrix norms.

### 7. Matrix dimensionality assertion inverted

**Mutant:** `numpy.linalg._linalg.x__assert_2d__mutmut_1`

```diff
-        if a.ndim != 2:
+        if a.ndim == 2:
```

**Why it survived:** This is a high-confidence behavioral gap if the target
scope includes matrix validation paths. The current norm test covers valid
matrix norm values, but this helper is not necessarily reached by those `norm`
branches. It is more directly relevant to linalg APIs that require 2-D arrays,
and it indicates that invalid-dimensionality error behavior is not being
checked.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add explicit invalid-shape checks for matrix-only norm
orders and related linalg paths, asserting that invalid dimensions raise
`LinAlgError` or `ValueError` exactly where NumPy documents that behavior.

### 8. SVD-based norm option forwarding changed

**Mutant:** `numpy.linalg._linalg.x__multi_svd_norm__mutmut_18`

```diff
-    result = op(svd(y, compute_uv=False), axis=-1)
+    result = op(svd(y, compute_uv=None), axis=-1)
```

**Why it survived:** For normal numeric values, `compute_uv=None` behaves
similarly enough to preserve the singular values used by nuclear and spectral
norms. The test compares final values, not internal option forwarding or
performance-sensitive behavior.

**Confidence:** Medium.

**Targeted test idea:** This is lower priority for output-only testing. If exact
internal forwarding matters, monkeypatch the local `svd` helper or add a narrow
test that detects whether singular vectors are unnecessarily requested.

## Overall Assessment

The Codex NumPy suite has good semantic checks for ordinary numeric arrays, but
the surviving mutants point to four main gaps:

1. Dispatch and subclass behavior for `np.sum`, `np.cumsum`, and
   `np.linalg.norm` is mostly untested.
2. Complex and lower-precision dtype behavior is weak for `linalg.norm`.
3. Invalid-shape and matrix-validation behavior should be tested explicitly,
   especially for matrix norm modes and linalg helper paths.
4. Expected-value helpers should avoid relying too heavily on mutated NumPy
   helpers when possible; independent formulas are strongest, while helper
   calls such as `np.sum`, `np.max`, `np.min`, and `np.linalg.svd` can create
   oracle coupling.
