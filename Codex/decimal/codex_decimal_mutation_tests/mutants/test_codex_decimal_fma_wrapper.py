from decimal import Decimal
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


# Summary: Generate bounded finite Decimal operands with a few decimal places,
# including zeros and signed values. The bounds keep products and sums within
# ordinary Decimal precision while still covering integer, fractional,
# positive, negative, and cancellation cases.
@given(st.data())
def test_fma_property(data):
    left = data.draw(finite_decimals)
    right = data.draw(finite_decimals)
    third = data.draw(finite_decimals)

    result = left.fma(right, third)

    # fma returns a Decimal equal to self * other + third.
    assert isinstance(result, Decimal)
    assert result == left * right + third

    # The multiplication part is commutative.
    assert result == right.fma(left, third)

    # Multiplying by zero leaves only the addend.
    assert left.fma(Decimal("0"), third) == third
    assert Decimal("0").fma(right, third) == third

    # Adding zero makes fma equivalent to Decimal multiplication.
    assert left.fma(right, Decimal("0")) == left * right

    # The documented example must hold exactly.
    assert Decimal(2).fma(Decimal(3), Decimal(5)) == Decimal("11")
# End program



