# Survived Mutants: Codex decimal PBT Suite

`mutmut browse`

```text
codex_decimal_mutation_tests
```

| File | Survived mutants | Untested mutants |
|---|---:|---:|
| `decimal.py` | 484 | 4 |

`mutmut results` also reported 2 timeout mutants. The mutation target is the
pure-Python Decimal implementation copied as `decimal.py`.

## Confidence Scale

| Confidence | Meaning |
|---|---|
| <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | The mutant changes externally visible Decimal behavior that the tests should catch with a targeted example. |
| Medium | The mutation could matter, but not sure whether generated inputs ever reach the affected code. |
| Low | The mutation probably doesn't change anything observable. |

Overall confidence in the current Codex decimal mutation quality: **Medium-Low**.
The tests cover the happy paths for `as_integer_ratio`, `compare`, `fma`,
`from_float`, and `quantize`, but many survived mutants are in helper methods
used by those APIs or in Decimal operations outside the five target functions.
Another important issue is oracle coupling: several tests compute expected
values with the same local mutated `decimal.py`, for example `left * right`,
`value / quantum`, `Decimal(value)`, or `Fraction(value)`. If a helper mutation
affects both the implementation and the expected-value calculation, the test may
not kill it.

## Survivor Distribution

| Area | Survived | Confidence | Interpretation |
|---|---:|---|---|
| `Decimal._power_exact` | 55 | Low | Power internals are mostly outside the five documented target APIs. |
| `Decimal.__pow__` | 49 | Low | Exponentiation is covered indirectly at most, not directly tested. |
| `Decimal.__hash__` | 31 | Low | Hash behavior is not part of the target properties. |
| `Decimal.__add__` | 28 | Medium | Addition helpers can affect `fma`, but expected values also use mutated arithmetic. |
| `Decimal.quantize` | 25 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; surviving mutants show gaps around conversion, context, rounding, and error branches. |
| `Context.__init__` | 18 | Medium | Context defaults matter for rounding/traps but are not varied much. |
| `Decimal._rescale` | 17 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Directly relevant to `quantize`; padding and rounding branches are under-tested. |
| `Decimal.__str__` | 15 | Low | String formatting is not a target property. |
| `Decimal.__truediv__` / `Context.divide` | 26 | Medium | Used by quantize expected-value calculations, so oracle coupling can hide bugs. |
| `Decimal.fma` | 9 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; invalid operand and special-value paths are weak. |
| `Decimal.as_integer_ratio` | 8 | Medium | Direct target API, but some survivors are likely equivalent for generated finite decimals. |
| `Decimal.compare` | 6 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | Direct target API; invalid operand and special NaN variants are weak. |
| `Decimal.from_float` | 0 | <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span> | No survived mutants appeared in `from_float` itself. |
| Other functions | 202 | Low-Medium | Smaller clusters across comparisons, rounding helpers, context operations, and formatting. |

## Example Survived Mutants

### 1. `quantize` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁquantize__mutmut_3`

```diff
-exp = _convert_other(exp, raiseit=True)
+exp = _convert_other(exp, raiseit=None)
```

**Why it survived:** The quantize wrapper always passes valid `Decimal`
quantums. It does not check invalid operand types, so weakening conversion error
behavior is not observed.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 2. `fma` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁfma__mutmut_3`

```diff
-other = _convert_other(other, raiseit=True)
+other = _convert_other(other, raiseit=None)
```

**Why it survived:** The `fma` test only generates valid finite Decimal
operands. It checks arithmetic identities, but does not check that unsupported
operand types are rejected.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 3. `compare` operand conversion weakened

**Mutant:** `decimal.xǁDecimalǁcompare__mutmut_3`

```diff
-other = _convert_other(other, raiseit=True)
+other = _convert_other(other, raiseit=None)
```

**Why it survived:** The compare wrapper only compares valid finite Decimals and
quiet NaNs. It does not test invalid operands, signaling NaNs, or context-driven
error behavior.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 4. `as_integer_ratio` exponent boundary changed

**Mutant:** `decimal.xǁDecimalǁas_integer_ratio__mutmut_6`

```diff
-if self._exp >= 0:
+if self._exp > 0:
```

**Why it survived:** For exponent `0`, both branches can still produce the same
ratio: denominator `1` and the same numerator. This mutant is likely equivalent
for many generated finite Decimal values.

**Confidence:** Low.

### 5. `quantize` rescale padding changed

**Mutant:** `decimal.xǁDecimalǁ_rescale__mutmut_18`

```diff
-self._int + '0'*(self._exp - exp), exp)
+self._int + 'XX0XX'*(self._exp - exp), exp)
```

**Why it survived:** This branch pads the coefficient when the requested
exponent requires trailing zeros. The current quantize tests include several
quantums, but the expected calculation uses Decimal arithmetic from the same
mutated module, and the generated cases may not strongly isolate this padding
branch.

**Confidence:** <span style="background-color:#fde2e1; color:#b42318; font-weight:700; padding:2px 6px; border-radius:4px;">High</span>.

### 6. Exact power helper disabled

**Mutant:** `decimal.xǁDecimalǁ_power_exact__mutmut_1`

```diff
-x = _WorkRep(self)
+x = None
```

**Why it survived:** This is a large survivor cluster, but exponentiation is not
one of the five target APIs. It is probably only covered indirectly by helper
logic or setup code, so the current property tests do not assert power-specific
behavior.

**Confidence:** Low.

### 7. Power modulo branch inverted

**Mutant:** `decimal.xǁDecimalǁ__pow____mutmut_1`

```diff
-if modulo is not None:
+if modulo is None:
```

**Why it survived:** The suite does not test `Decimal.__pow__` or modular power
directly. This survivor mostly shows that covered-line mutation reached broader
Decimal internals, not that the target API properties are specifically weak.

**Confidence:** Low.



## Overall Assessment

Main weakness is precision on edge behavior and independent oracles. Example
failed invariants include:

1. Invalid operand handling for `quantize`, `fma`, and `compare`.
2. Special-value behavior beyond quiet NaN and infinities, especially signaling
   NaNs and context traps.
3. Quantize rescaling branches where trailing zeros are added or precision
   limits trigger `InvalidOperation`.
4. Context-dependent rounding behavior with custom contexts instead of only
   passing explicit rounding modes.
5. Independent expected-value checks that avoid using the same mutated Decimal
   arithmetic as the implementation under test.
