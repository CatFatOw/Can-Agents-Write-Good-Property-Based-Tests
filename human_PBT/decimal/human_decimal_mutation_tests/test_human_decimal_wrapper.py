from decimal import Decimal, InvalidOperation
import math

import pytest
from hypothesis import given, strategies as st


finite_floats = st.floats(
    min_value=-50,
    max_value=50,
    allow_nan=False,
    allow_infinity=False,
)


@given(finite_floats)
def test_as_integer_ratio_value_and_reduction(number):
    value = Decimal(str(number))
    numerator, denominator = value.as_integer_ratio()

    assert denominator > 0
    assert Decimal(numerator) / Decimal(denominator) == value
    assert math.gcd(numerator, denominator) == 1


@given(finite_floats, finite_floats)
def test_compare_returns_ordering(left, right):
    left_value = Decimal(str(left))
    right_value = Decimal(str(right))
    result = left_value.compare(right_value)

    if left_value < right_value:
        assert result == Decimal("-1")
    elif left_value > right_value:
        assert result == Decimal("1")
    else:
        assert result == Decimal("0")

    assert Decimal("NaN").compare(right_value).is_nan()
    assert left_value.compare(Decimal("NaN")).is_nan()


@given(
    st.integers(min_value=-50, max_value=50),
    st.integers(min_value=-50, max_value=50),
    st.integers(min_value=-50, max_value=50),
)
def test_fma_matches_multiply_add(left, right, third):
    left_value = Decimal(left)
    right_value = Decimal(right)
    third_value = Decimal(third)

    assert left_value.fma(right_value, third_value) == left_value * right_value + third_value
    assert left_value.fma(right_value, third_value) == right_value.fma(left_value, third_value)
    assert left_value.fma(Decimal("0"), third_value) == third_value


@given(finite_floats)
def test_from_float_preserves_float_value(number):
    result = Decimal.from_float(number)

    assert isinstance(result, Decimal)
    assert float(result) == number
    if number > 0:
        assert result > Decimal("0")
    elif number < 0:
        assert result < Decimal("0")
    else:
        assert result == Decimal("0")

    assert Decimal.from_float(float("nan")).is_nan()
    assert Decimal.from_float(float("inf")) == Decimal("Infinity")
    assert Decimal.from_float(float("-inf")) == Decimal("-Infinity")


@given(
    finite_floats,
    st.sampled_from(
        [
            Decimal("1"),
            Decimal("0.1"),
            Decimal("0.01"),
            Decimal("0.001"),
            Decimal("0.0001"),
        ]
    ),
)
def test_quantize_exponent_and_special_cases(number, exponent):
    value = Decimal(str(number))
    result = value.quantize(exponent)

    assert result.as_tuple().exponent == exponent.as_tuple().exponent
    assert result.quantize(exponent) == result
    assert Decimal("NaN").quantize(exponent).is_nan()

    with pytest.raises(InvalidOperation):
        Decimal("Infinity").quantize(exponent)
    with pytest.raises(InvalidOperation):
        Decimal("-Infinity").quantize(exponent)
