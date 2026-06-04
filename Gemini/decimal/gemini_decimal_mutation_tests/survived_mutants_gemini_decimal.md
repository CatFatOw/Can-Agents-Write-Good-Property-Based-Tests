# Survived Mutants: Gemini decimal PBT Suite

`mutmut results`

```text
gemini_decimal_mutation_tests
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `decimal.py` | 456 | 4 |

`mutmut results` also reported 3 timeout mutants. The mutation target is the
pure-Python Decimal implementation copied as `decimal.py`.

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible Decimal behavior that the tests should catch with a targeted example. |
| Medium | The mutation could matter, but not sure whether generated inputs ever reach the affected code. |
| Low | The mutation probably doesn't change anything observable. |

Overall confidence in the current Gemini decimal mutation quality:
**Medium-Low**. The tests cover broad generated inputs for `as_integer_ratio`,
`compare`, `fma`, `from_float`, and `quantize`, including NaNs and infinities in
several wrappers. However, many survivors remain in helper methods used by those
APIs or in Decimal operations outside the five target functions.

The main weakness is edge-behavior precision. Some tests also have oracle
coupling: for example, `quantize` checks exponent/idempotency rather than
independent expected values, and `fma` computes the final expected Decimal using
the local Decimal implementation and context operations. Mutations in helpers
used by both the target operation and the oracle can therefore survive.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `Decimal._power_exact` | 55 | Low | Power internals are outside the five documented target APIs. |
| `Decimal.__pow__` | 49 | Low | Exponentiation and modular power are not directly tested. |
| `Decimal.__hash__` | 31 | Low | Hash behavior is not part of the target properties. |
| `Decimal.__add__` | 28 | Medium | Addition affects `fma`, but the expected-value path can also use mutated Decimal arithmetic. |
| `Decimal.quantize` | 25 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; survivors show gaps around conversion, context, rounding, and error branches. |
| `Decimal.__str__` | 17 | Low | String formatting is only indirectly relevant. |
| `Context.__init__` | 14 | Medium | Context defaults and signal dictionaries matter, but are not checked directly. |
| `Decimal.__truediv__` / `Context.divide` | 18 | Medium | Division helpers are used in expected-value construction and context arithmetic. |
| `_normalize` | 13 | Low-Medium | Normalization details can affect canonical forms and string-like behavior, but many paths are outside direct targets. |
| `Decimal.fma` | 9 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; invalid operand, special-value, and context-forwarding paths are weak. |
| `Decimal._rescale` | 9 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Directly relevant to `quantize`; boundary rounding and exponent cases are under-tested. |
| `Decimal.as_integer_ratio` | 7 | Medium | Direct target API, but some survivors are likely equivalent for generated finite decimals. |
| `Decimal.compare` | 6 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; invalid operand and NaN/context edge paths are weak. |
| `Decimal.from_float` | 0 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | No survived mutants appeared in `from_float` itself. |
| Other functions | 175 | Low-Medium | Smaller clusters across comparisons, rounding helpers, context operations, conversion helpers, and formatting. |

## Example Survived Mutants

### 1. `quantize` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁquantize__mutmut_3`

```diff
-exp = _convert_other(exp, raiseit=True)
+exp = _convert_other(exp, raiseit=None)
```

**Why it survived:** The quantize wrapper draws valid finite Decimals for both
operands. It checks exponent matching and idempotency after successful calls, but
does not check invalid operand types or conversion failures.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 2. `fma` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁfma__mutmut_3`

```diff
-other = _convert_other(other, raiseit=True)
+other = _convert_other(other, raiseit=None)
```

**Why it survived:** The `fma` test draws Decimal-compatible operands. It
checks finite arithmetic with `Fraction` and handles NaNs/infinities, but it does
not assert that unsupported operand types are rejected.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 3. `fma` context forwarding dropped

**Mutant:** `decimal.xǁDecimalǁfma__mutmut_28`

```diff
-return product.__add__(third, context)
+return product.__add__(third, None)
```

**Why it survived:** The test creates random contexts, but many invalid-context
or special-value cases are accepted by returning early. For finite values, the
expected result is also converted back through the local Decimal/context
machinery, so context-sensitive helper mutations can be hidden.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 4. `compare` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁcompare__mutmut_3`

```diff
-other = _convert_other(other, raiseit=True)
+other = _convert_other(other, raiseit=None)
```

**Why it survived:** The compare wrapper draws Decimal values and untraps
`InvalidOperation` for signaling NaNs. It does not test non-Decimal operands or
the strict conversion behavior of `compare()`.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 5. `as_integer_ratio` exponent boundary changed

**Mutant:** `decimal.xǁDecimalǁas_integer_ratio__mutmut_6`

```diff
-if self._exp >= 0:
+if self._exp > 0:
```

**Why it survived:** For exponent `0`, both branches can still produce the same
ratio: denominator `1` and the same numerator. This mutant is likely equivalent
for many generated finite Decimal values.

**Confidence:** Low.

### 6. `_rescale` boundary changed

**Mutant:** `decimal.xǁDecimalǁ_rescale__mutmut_23`

```diff
-if digits < 0:
+if digits <= 0:
```

**Why it survived:** This boundary controls a quantize/rescale path where the
coefficient is replaced before rounding. The quantize property verifies the
result exponent and idempotency, but does not compare exact rounded values
against an independent oracle for boundary cases.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 7. Addition special-value branch narrowed

**Mutant:** `decimal.xǁDecimalǁ__add____mutmut_6`

```diff
-if self._is_special or other._is_special:
+if self._is_special and other._is_special:
```

**Why it survived:** Addition is not a direct target API, but it is used by
`fma`. The current `fma` test returns early for many special-value cases and
accepts either NaN or infinity in some infinite combinations, so addition's exact
mixed-special behavior is not strongly pinned down.

**Confidence:** Medium.

### 8. Exact power helper disabled

**Mutant:** `decimal.xǁDecimalǁ_power_exact__mutmut_1`

```diff
-x = _WorkRep(self)
+x = None
```

**Why it survived:** This is the largest survivor cluster, but exponentiation is
not one of the five target APIs. These survivors mostly show that mutation
testing reached broader Decimal internals, not that the Gemini target properties
specifically intended to verify power behavior.

**Confidence:** Low.

### 9. Power modulo branch inverted

**Mutant:** `decimal.xǁDecimalǁ__pow____mutmut_1`

```diff
-if modulo is not None:
+if modulo is None:
```

**Why it survived:** The suite does not test `Decimal.__pow__` or modular power
directly. This survivor is low confidence for the current target-function study,
but it explains a large portion of the raw survivor count.

**Confidence:** Low.

## Overall Assessment

The Gemini decimal suite validates a useful set of broad properties, especially
for generated finite values and basic special-value handling. The surviving
mutants show that the suite needs sharper edge-case assertions and more
independent expected values. Highest-priority gaps:

1. Invalid operand handling for `quantize`, `fma`, and `compare`.
2. Exact context forwarding and rounding behavior for `fma` and `quantize`.
3. Quantize rescale boundary cases where precision, exponent limits, and
   rounding decisions are externally visible.
4. Special-value combinations in arithmetic helpers used by `fma`.
5. Independent oracles that avoid using the same mutated Decimal helpers as the
   implementation under test.
6. Direct examples for NaN variants, signaling NaNs, traps, and custom contexts.
