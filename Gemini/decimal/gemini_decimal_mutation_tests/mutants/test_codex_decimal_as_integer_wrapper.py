from decimal import Decimal
from fractions import Fraction
import math
from pathlib import Path
import sys

from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Summary: Generate finite Decimal values with bounded magnitude and decimal
# places, including zero and signed values, so as_integer_ratio sees a wide
# range of exact base-10 fractions without NaN, infinity, or huge exponents.
@given(st.data())
def test_as_integer_ratio_property(data):
    value = data.draw(
        st.decimals(
            min_value=Decimal("-1000000000000"),
            max_value=Decimal("1000000000000"),
            places=12,
            allow_nan=False,
            allow_infinity=False,
        )
    )

    numerator, denominator = value.as_integer_ratio()

    # The result is a pair of integers representing the Decimal exactly.
    assert isinstance(numerator, int)
    assert isinstance(denominator, int)
    assert Fraction(numerator, denominator) == Fraction(value)

    # The denominator is positive and the fraction is in lowest terms.
    assert denominator > 0
    assert math.gcd(numerator, denominator) == 1

    # Zero has no sign in the returned numerator and is normalized to 0 / 1.
    if value.is_zero():
        assert numerator == 0
        assert denominator == 1
    elif value.is_signed():
        assert numerator < 0
    else:
        assert numerator > 0
# End program



