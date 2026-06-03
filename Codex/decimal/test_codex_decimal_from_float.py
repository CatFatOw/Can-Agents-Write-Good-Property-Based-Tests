from decimal import Decimal
import math
from pathlib import Path
import sys

from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


float_or_int_values = st.one_of(
    st.floats(
        allow_nan=True,
        allow_infinity=True,
        width=64,
    ),
    st.integers(min_value=-(2**53), max_value=2**53),
)


# Summary: Generate Python floats across finite, NaN, and infinity cases, plus
# bounded integers accepted by from_float. This covers exact binary-float
# conversion without constructing huge Decimals or depending on decimal context.
@given(st.data())
def test_from_float_property(data):
    value = data.draw(float_or_int_values)
    result = Decimal.from_float(value)

    # from_float returns a Decimal instance.
    assert isinstance(result, Decimal)

    if isinstance(value, float) and math.isnan(value):
        assert result.is_nan()
        return

    if isinstance(value, float) and math.isinf(value):
        if value > 0:
            assert result == Decimal("Infinity")
        else:
            assert result == Decimal("-Infinity")
        return

    # Finite floats and ints are represented by the exact numeric value.
    assert result == Decimal(value)
    assert float(result) == float(value)

    # The sign of finite nonzero values is preserved.
    if value > 0:
        assert result > Decimal("0")
    elif value < 0:
        assert result < Decimal("0")
    else:
        assert result == Decimal("0")

    # Binary floating-point values are not converted as their short repr.
    if isinstance(value, float) and value == 0.1:
        assert result != Decimal("0.1")

    # The documented examples must hold exactly.
    assert Decimal.from_float(0.1) == Decimal(
        "0.1000000000000000055511151231257827021181583404541015625"
    )
    assert Decimal.from_float(float("nan")).is_nan()
    assert Decimal.from_float(float("inf")) == Decimal("Infinity")
    assert Decimal.from_float(float("-inf")) == Decimal("-Infinity")
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_from_float_property))
