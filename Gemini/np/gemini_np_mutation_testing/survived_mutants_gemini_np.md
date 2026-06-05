# Survived Mutants: Gemini numpy PBT Suite

`mutmut browse`

```text
gemini_np_mutation_testing
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `numpy/_core/fromnumeric.py` | 26 | 0 |
| `numpy/_core/multiarray.py` | 6 | 0 |
| `numpy/linalg/_linalg.py` | 24 | 1 |

The mutation target includes the Python-facing NumPy helpers for `sum`,
`cumsum`, `dot`, and `linalg.norm`. `np.add` is a compiled ufunc, so mutmut
cannot directly mutate the core addition implementation; the `add` wrapper
tests still run as part of the selected pytest suite.

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible target API behavior that should be caught by a targeted property or fixed example. |
| Medium | The mutant changes dispatch, dtype, subclass, or validation behavior that matters for NumPy compatibility, but may not be reached by ordinary generated arrays. |
| Low | The mutant is outside the target API behavior, probably equivalent for generated inputs, or only affects metadata/internal setup. |

Overall confidence in the current Gemini numpy mutation quality: **Medium-Low**.

The Gemini tests cover ordinary happy-path behavior for the five NumPy targets:
`add` checks algebraic identities and `where`, `cumsum` checks shape/dtype and
prefix differences, `dot` checks common product scenarios, `sum` checks output
shape plus an `initial` invariant, and `linalg.norm` checks non-negativity,
shape, and default-order equivalence. The survivors show that several important
semantic details are still weak: `sum` does not independently verify values for
general axes/dtypes, `linalg.norm` does not compare most ord values against
independent formulas, and subclass/dispatch/error-path behavior is largely
untested. Some assertions also use NumPy helpers from the same mutated package,
which can create oracle coupling.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `_wrapfunc` in `fromnumeric.py` | 5 | Medium | `cumsum` method dispatch for subclasses/custom array-like objects is untested. |
| `_wrapreduction` in `fromnumeric.py` | 7 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Extra survivors include dropped `dtype` forwarding for reductions, showing weak `sum` dtype/value checks. |
| `_wrapreduction_any_all` in `fromnumeric.py` | 14 | Low-Medium | Mostly helper mutations reached through test assertions such as `np.all`; not direct target behavior. |
| `_override___module__` in `multiarray.py` | 6 | Low | Ufunc metadata setup survived; ordinary `np.add` arithmetic still works. |
| `_makearray` in `linalg/_linalg.py` | 6 | Medium | Array wrapping/subclass behavior for `linalg.norm` is not tested. |
| `_realType` and `_commonType` in `linalg/_linalg.py` | 8 | Medium | Complex and single-precision dtype behavior is weak because norm inputs are ordinary float arrays. |
| `_assert_2d` and `_assert_stacked_square` in `linalg/_linalg.py` | 6 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Invalid-dimensionality and non-square matrix validation paths are not directly checked. |
| `_multi_svd_norm` in `linalg/_linalg.py` | 4 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | SVD-based norms such as nuclear, spectral, and smallest-singular-value norms are not independently checked. |
| `_multi_dot_matrix_chain_order` in `linalg/_linalg.py` | 0 survived, 1 untested | Low | `multi_dot` is outside the selected target APIs. |

## Example Survived Mutants

### 1. `sum` accumulator dtype dropped

**Mutant:** `numpy._core.fromnumeric.x__wrapreduction__mutmut_12`

```diff
-    return ufunc.reduce(obj, axis, dtype, out, **passkwargs)
+    return ufunc.reduce(obj, axis, None, out, **passkwargs)
```

**Why it survived:** The `sum` wrapper generates only `float64` arrays and does
not pass a `dtype` argument. It checks shape and a simplified `initial`
relationship, but not documented accumulator dtype behavior. Dropping the
`dtype` argument therefore has no observable effect in the generated domain.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Generate integer and lower-precision floating arrays
with explicit `dtype` values, then assert both output dtype and independently
computed values.

### 2. `sum` reduction argument forwarding changed

**Mutant:** `numpy._core.fromnumeric.x__wrapreduction__mutmut_16`

```diff
-    return ufunc.reduce(obj, axis, dtype, out, **passkwargs)
+    return ufunc.reduce(obj, axis, out, **passkwargs)
```

**Why it survived:** This changes positional forwarding to `ufunc.reduce`.
Because the test does not cover explicit `dtype`, `out`, `where`, or detailed
value oracles for many combinations, the bad forwarding can survive for normal
float64 arrays.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add `out`, `dtype`, `where`, and tuple-axis cases with a
manual oracle rather than comparing only shape or broad invariants.

### 3. `cumsum` dispatch to object methods bypassed

**Mutant:** `numpy._core.fromnumeric.x__wrapfunc__mutmut_1`

```diff
-    bound = getattr(obj, method, None)
+    bound = None
```

**Why it survived:** The `cumsum` test uses ordinary arrays. Bypassing the
object method lookup still lets NumPy compute correct cumulative sums through
the fallback path. Custom array-likes and ndarray subclasses with their own
`.cumsum()` behavior are not tested.

**Confidence:** Medium.

**Targeted test idea:** Add an ndarray subclass or simple custom object with a
`.cumsum()` method and assert that `np.cumsum` dispatches as expected.

### 4. Custom reduction dispatch removed

**Mutant:** `numpy._core.fromnumeric.x__wrapreduction__mutmut_6`

```diff
-            reduction = getattr(obj, method)
+            reduction = getattr(None, method)
```

**Why it survived:** The suite tests plain NumPy arrays, not objects with custom
`.sum()` methods. The fallback `ufunc.reduce` path still handles ordinary
arrays, so dispatch removal is invisible.

**Confidence:** Medium.

**Targeted test idea:** Include a minimal object or ndarray subclass whose
`sum()` records received arguments, then verify forwarding of `axis`, `out`,
`keepdims`, `initial`, and `where`.

### 5. Ufunc module metadata override broken

**Mutant:** `numpy._core.multiarray.x__override___module____mutmut_1`

```diff
-    namespace_names = globals()
+    namespace_names = None
```

**Why it survived:** This affects import-time metadata override behavior for
ufuncs, not the numeric result of `np.add`. The Gemini `add` tests focus on
identity, commutativity, `where`, operator equivalence, and shape.

**Confidence:** Low.

**Targeted test idea:** Only include this if metadata compatibility matters, for
example by checking `np.add.__module__ == "numpy"`.

### 6. Linalg dtype helper weakened

**Mutant:** `numpy.linalg._linalg.x__commonType__mutmut_1`

```diff
-    result_type = single
+    result_type = None
```

**Why it survived:** `linalg.norm` inputs are generated as default floating
arrays and the test only checks broad properties such as non-negativity and
shape. It does not check dtype promotion or complex-valued norms.

**Confidence:** Medium.

**Targeted test idea:** Generate `float32`, `complex64`, and `complex128`
inputs and assert expected output dtype/precision as well as numeric formulas.

### 7. Matrix dimensionality assertion inverted

**Mutant:** `numpy.linalg._linalg.x__assert_2d__mutmut_1`

```diff
-        if a.ndim != 2:
+        if a.ndim == 2:
```

**Why it survived:** The norm wrapper only calls `LA.norm` on valid 1-D or 2-D
inputs and does not assert invalid-dimensionality behavior. This helper is more
directly relevant to matrix-only linalg paths, and its survival shows that
validation/error behavior is not part of the current properties.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Add explicit invalid-shape examples and assert the
documented `ValueError` or `LinAlgError` behavior for matrix norm modes and
other linalg calls included in the mutation target.

### 8. SVD norm axis movement changed

**Mutant:** `numpy.linalg._linalg.x__multi_svd_norm__mutmut_10`

```diff
-    y = moveaxis(x, (row_axis, col_axis), (-2, -1))
+    y = moveaxis(x, (row_axis, col_axis), (-2, +1))
```

**Why it survived:** The `linalg.norm` test checks non-negativity, output shape,
and default equivalence. It does not independently verify nuclear norm,
spectral norm, or smallest singular value formulas. A wrong internal axis move
can survive if the broad properties still hold.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** For 2-D matrices, compare `ord="nuc"`, `ord=2`, and
`ord=-2` against independent SVD-based expected values. For stacked matrices,
use explicit `axis=(..., ...)` cases.

### 9. SVD norm reduction axis changed

**Mutant:** `numpy.linalg._linalg.x__multi_svd_norm__mutmut_14`

```diff
-    result = op(svd(y, compute_uv=False), axis=-1)
+    result = op(svd(y, compute_uv=False), axis=None)
```

**Why it survived:** Reducing over all singular values instead of the final
axis can change stacked matrix norms, but the Gemini norm test uses `axis=None`
and mostly asserts scalar shape/non-negativity. It does not cover stacked
matrix norm outputs.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Generate 3-D arrays with `axis=(1, 2)` or similar and
check that SVD-based norms return one value per matrix, not a global reduction.

## Overall Assessment

The Gemini NumPy suite catches many gross result failures for ordinary arrays,
but the surviving mutants point to these main gaps:

1. `np.sum` needs an independent value oracle for axis, tuple-axis,
   `keepdims`, `dtype`, `initial`, `where`, and `out`; shape-only checks are not
   enough.
2. `np.linalg.norm` needs formula-based checks for every generated `ord`,
   especially SVD-based matrix norms and stacked matrix axes.
3. Complex, `float32`, and dtype-promotion behavior should be tested for
   `linalg.norm`.
4. Dispatch/subclass behavior for `sum`, `cumsum`, and `norm` is largely
   absent.
5. Some helper mutations survive because test assertions use mutated NumPy
   helpers as oracles; independent Python/manual calculations would improve
   mutation sensitivity.
