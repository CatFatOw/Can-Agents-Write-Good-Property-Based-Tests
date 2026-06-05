from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_CEILING,
    ROUND_DOWN,
    ROUND_FLOOR,
    ROUND_HALF_EVEN,
    ROUND_HALF_UP,
    ROUND_UP,
)
from pathlib import Path
import sys

from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


finite_decimals = st.decimals(
    min_value=Decimal("-10000"),
    max_value=Decimal("10000"),
    places=4,
    allow_nan=False,
    allow_infinity=False,
)
quantums = st.sampled_from(
    [
        Decimal("1E+2"),
        Decimal("1E+1"),
        Decimal("1"),
        Decimal("0.1"),
        Decimal("0.01"),
        Decimal("0.001"),
        Decimal("0.0001"),
    ]
)
rounding_modes = st.sampled_from(
    [
        ROUND_CEILING,
        ROUND_DOWN,
        ROUND_FLOOR,
        ROUND_HALF_EVEN,
        ROUND_HALF_UP,
        ROUND_UP,
    ]
)


# Summary: Generate bounded finite Decimal values with up to four decimal
# places, sampled target exponents from hundreds through four decimal places,
# and common rounding modes. The bounds avoid unrelated precision errors while
# covering coarser and finer quantization, signs, zero, and ties.
@given(st.data())
def test_quantize_property(data):
    value = data.draw(finite_decimals)
    quantum = data.draw(quantums)
    rounding = data.draw(rounding_modes)

    result = value.quantize(quantum, rounding=rounding)

    # quantize returns a Decimal equal to value rounded to quantum's exponent.
    assert isinstance(result, Decimal)
    expected = (value / quantum).to_integral_value(rounding=rounding) * quantum
    assert result == expected

    # Unless an error is signaled, the result has exactly the right operand's
    # exponent, and applying the same quantize again is idempotent.
    assert result.as_tuple().exponent == quantum.as_tuple().exponent
    assert result.quantize(quantum, rounding=rounding) == result

    # Values that already have the requested exponent are unchanged.
    already_quantized = result
    assert already_quantized.quantize(quantum, rounding=rounding) == already_quantized

    # Documented example.
    assert Decimal("1.41421356").quantize(Decimal("1.000")) == Decimal("1.414")

    # Quiet NaN remains NaN, while infinities signal InvalidOperation.
    assert Decimal("NaN").quantize(quantum, rounding=rounding).is_nan()
    for special in [Decimal("Infinity"), Decimal("-Infinity")]:
        try:
            special.quantize(quantum, rounding=rounding)
        except InvalidOperation:
            pass
        else:
            assert False
# End program


