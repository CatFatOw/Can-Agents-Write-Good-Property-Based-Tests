from decimal import Decimal
from pathlib import Path
import sys

from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


finite_decimals = st.decimals(
    min_value=Decimal("-1000000000000"),
    max_value=Decimal("1000000000000"),
    places=12,
    allow_nan=False,
    allow_infinity=False,
)
decimal_values = st.one_of(finite_decimals, st.just(Decimal("NaN")))


# Summary: Generate bounded finite Decimal values plus quiet NaN operands, so
# compare sees less-than, equal, greater-than, and documented NaN cases without
# infinities, signaling NaNs, or very large exponents.
@given(st.data())
def test_compare_property(data):
    left = data.draw(decimal_values)
    right = data.draw(decimal_values)

    result = left.compare(right)

    # compare() always returns a Decimal instance.
    assert isinstance(result, Decimal)

    # If either operand is NaN, the result is NaN.
    if left.is_nan() or right.is_nan():
        assert result.is_nan()
        return

    # For finite operands, the result encodes the value ordering exactly.
    if left < right:
        assert result == Decimal("-1")
    elif left == right:
        assert result == Decimal("0")
    else:
        assert result == Decimal("1")

    # Reversing unequal operands flips the comparison sign.
    reverse = right.compare(left)
    if left == right:
        assert reverse == Decimal("0")
    else:
        assert reverse == -result

    # A finite Decimal compares equal to itself.
    assert left.compare(left) == Decimal("0")
    assert right.compare(right) == Decimal("0")
# End program


