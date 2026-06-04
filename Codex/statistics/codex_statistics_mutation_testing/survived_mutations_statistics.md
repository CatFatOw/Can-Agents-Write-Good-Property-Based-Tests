# Survived Mutants: Codex statistics PBT Suite

`mutmut results`

```text
codex_statistics_mutation_testing
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `statistics.py` | 51 | 13 |

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible numeric results or documented error behavior that should be caught by a targeted example. |
| Medium | The mutation could matter, but may require less common input types, weighted data, or exact edge cases. |
| Low | The mutation mainly changes exception text, assertions, or internal behavior that normal property tests may not reasonably check. |

Overall confidence in the current Codex statistics mutation quality: **Medium**.

The suite covers the main success paths for `mean`, `median`, `variance`,
`geometric_mean`, `correlation`, and `linear_regression`, but the survivors show
weak pressure on exact arithmetic internals, type preservation, weighted means,
ranked correlation, and regression edge modes.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `_ss` exact sum-of-squares helper | 9 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Variance and related calculations are not strongly checked against exact oracle values or translation invariants. |
| `_coerce` type resolution | 8 | Low-Medium | Internal numeric type-routing survives, especially assertion text and mixed-type coercion cases. |
| `_convert` result type conversion | 3 | Medium | Result-type preservation for `Fraction`, `Decimal`, float infinities, and NaNs needs sharper checks. |
| `mean` | 3 | Low-Medium | Mostly empty-input exception-message changes and type-conversion edge cases survive. |
| `fmean` | 4 | Medium | Weighted and empty-input behavior is not fully constrained. |
| `geometric_mean` | 5 | Medium | Non-positive, empty, and exception behavior survives more than the positive-data path. |
| `median` | 3 | Low-Medium | Empty-input error text and even-length midpoint details survive. |
| `variance` | 5 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Sample-variance denominator and insufficient-data behavior need targeted examples. |
| `correlation` | 7 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Ranked correlation and method validation are under-tested. |
| `linear_regression` | 4 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Centering, intercept, and proportional-mode behavior need exact assertions. |
| Untested functions | 13 | Medium | `_fail_neg`, `_rank`, `median_grouped`, `quantiles`, and `NormalDist` have no covered mutants in this run. |

## Example Survived Mutants

### 1. Sum-of-squares accumulation changed

**Mutant:** `statistics.x__ss__mutmut_23`

```diff
-            sx_partials[d] += n
+            sx_partials[d] -= n
```

**Why it survived:** `_ss` is the exact arithmetic helper behind variance-style
calculations. Changing the sign of the accumulated sum should affect the center
and, for some inputs, downstream variance-related results. Survival suggests the
tests do not compare against enough small exact examples or translation
invariants.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact sample variance for small lists such as
`[1, 2, 3]`, `[2, 4, 4, 4, 5, 5, 7, 9]`, and equivalent `Fraction` inputs.
Also assert `variance([x + c for x in data]) == variance(data)`.

### 2. Center value from `_ss` replaced

**Mutant:** `statistics.x__ss__mutmut_51`

```diff
-        c = sx / count
+        c = sx * count
```

**Why it survived:** This changes the computed center returned by `_ss`.
Although `_ss` is internal, it affects code paths that use an inferred mean
rather than a supplied one. The current tests likely check broad properties but
not exact relationships between `xbar`, centered data, and variance.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Compare `variance(data)` with
`variance(data, xbar=mean(data))` for small integer and `Fraction` datasets.

### 3. Result type conversion weakened

**Mutant:** `statistics.x__convert__mutmut_1`

```diff
-    if type(value) is T:
+    if type(None) is T:
```

**Why it survived:** This changes the fast path that preserves values already
in the requested numeric type. The visible effect is most likely to appear with
non-float numeric types such as `Fraction` or `Decimal`, or with NaN and infinity
values.

**Confidence:** Medium.

**Targeted test idea:** Assert output types for `mean([Fraction(1, 3),
Fraction(2, 3)])`, `mean([Decimal("1.1"), Decimal("2.2")])`, and datasets
containing Decimal infinities or NaNs where supported.

### 4. Ranked correlation path disabled

**Mutant:** `statistics.x_correlation__mutmut_14`

```diff
-    if method == 'ranked':
+    if method == 'RANKED':
```

**Why it survived:** The ranked-correlation branch is externally visible through
`correlation(x, y, method="ranked")`. This mutation skips ranking and falls back
to linear correlation on raw values, which can silently produce different
answers for monotonic but nonlinear relationships.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert `correlation([1, 2, 3], [10, 20, 100],
method="ranked") == 1.0`, while the linear correlation for the same data is not
exactly `1.0`.

### 5. Regression centering changed

**Mutant:** `statistics.x_linear_regression__mutmut_16`

```diff
-        y = (yi - ybar for yi in y)
+        y = (yi + ybar for yi in y)
```

**Why it survived:** The regression implementation centers `x` and `y` before
computing slope. Adding the mean instead of subtracting it should break the
slope or intercept for ordinary nonzero-mean data.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert exact slope and intercept for simple lines such
as `y = 2*x + 3` with nonzero-mean `x`, for example
`linear_regression([1, 2, 3], [5, 7, 9]) == (slope=2.0, intercept=3.0)`.

### 6. Proportional regression intercept changed

**Mutant:** `statistics.x_linear_regression__mutmut_32`

```diff
-    intercept = 0.0 if proportional else ybar - slope * xbar
+    intercept = 1.0 if proportional else ybar - slope * xbar
```

**Why it survived:** With `proportional=True`, the intercept is documented to be
forced to zero. This mutant changes that externally visible result, so the tests
are not asserting proportional-mode output directly.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

**Targeted test idea:** Assert
`linear_regression([1, 2, 3], [2, 4, 6], proportional=True).intercept == 0.0`.

## Overall Assessment

The current Codex statistics tests are useful for broad success-path behavior,
but the survivors point to missing exactness. The most important gaps are:

1. Exact small-oracle checks for variance and `_ss`-dependent behavior.
2. Direct tests for `correlation(..., method="ranked")` and invalid method
   handling.
3. Exact slope/intercept assertions for `linear_regression`, including
   `proportional=True`.
4. Type-preservation checks for `Fraction`, `Decimal`, NaN, and infinity cases.
5. Coverage for currently untested helpers and functions: `_rank`,
   `median_grouped`, `quantiles`, and `NormalDist`.
