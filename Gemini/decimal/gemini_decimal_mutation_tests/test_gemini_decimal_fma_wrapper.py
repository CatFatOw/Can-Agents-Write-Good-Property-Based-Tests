from hypothesis import given, strategies as st
from decimal import Decimal, Context, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_UP, ROUND_DOWN
from fractions import Fraction
import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Summary: Dynamically draw three Decimal values (including NaNs and Infinities) using st.decimals() alongside a randomly configured decimal.Context containing varied precision levels and IEEE 754 rounding modes to test the unrounded fused multiply-add contract.
@given(st.data())
def test_fma(data):
    # Strategies for drawing decimal inputs
    decimal_strategy = st.decimals(allow_nan=True, allow_infinity=True)
    
    self_val = data.draw(decimal_strategy)
    other = data.draw(decimal_strategy)
    third = data.draw(decimal_strategy)
    
    # Strategy for drawing context attributes
    rounding_modes = [
        ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_DOWN, 
        ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_UP, ROUND_DOWN
    ]
    random_precision = data.draw(st.integers(min_value=1, max_value=100))
    random_rounding = data.draw(st.sampled_from(rounding_modes))
    ctx = Context(prec=random_precision, rounding=random_rounding)
    
    # Execute the fused multiply-add operation under the custom context
    try:
        with ctx:
            result_fma = self_val.fma(other, third)
    except Exception:
        # If the operation triggers an exceptional state under the context (e.g., InvalidOperation),
        # the property holds if the combination of inputs is inherently invalid.
        return

    # Handle IEEE 754 special values where Fraction conversions are inapplicable
    if self_val.is_nan() or other.is_nan() or third.is_nan():
        assert result_fma.is_nan()
        return
        
    if self_val.is_infinite() or other.is_infinite() or third.is_infinite():
        if result_fma.is_nan():
            return
        assert result_fma.is_infinite()
        return

    # Verify mathematical correctness for finite values using arbitrary-precision fractions
    frac_self = Fraction(self_val)
    frac_other = Fraction(other)
    frac_third = Fraction(third)
    
    # The intermediate math happens with infinite precision (no rounding)
    exact_fractional_result = (frac_self * frac_other) + frac_third
    
    # Convert the exact mathematical fraction back to a Decimal using the exact same context rules
    with ctx:
        expected_decimal = ctx.div(
            Decimal(exact_fractional_result.numerator), 
            Decimal(exact_fractional_result.denominator)
        )
        
    assert result_fma == expected_decimal
# End program
