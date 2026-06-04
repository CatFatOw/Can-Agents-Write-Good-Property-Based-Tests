from hypothesis import given, strategies as st
from decimal import Decimal, DecimalException
import decimal

import sys 
from pathlib import Path 



# Summary: Generates pairs of finite Decimals alongside a randomly selected rounding mode to verify exponent matching and idempotency, while gracefully catching expected out-of-bounds decimal exceptions.
@given(st.data())
def test_quantize(data):
    # Generate the primary Decimal and the exponent-defining Decimal
    target = data.draw(st.decimals(allow_nan=False, allow_infinity=False))
    exp = data.draw(st.decimals(allow_nan=False, allow_infinity=False))
    
    # Sample a valid rounding mode
    rounding_modes = [
        decimal.ROUND_CEILING, decimal.ROUND_FLOOR, decimal.ROUND_DOWN,
        decimal.ROUND_HALF_DOWN, decimal.ROUND_HALF_EVEN, decimal.ROUND_HALF_UP,
        decimal.ROUND_UP, decimal.ROUND_05UP
    ]
    selected_rounding = data.draw(st.sampled_from(rounding_modes))

    try:
        result = target.quantize(exp, rounding=selected_rounding)
    except DecimalException:
        # Acceptable behavior under the API documentation if precision is exceeded 
        # or if the resulting exponent falls outside Emax/Etiny boundaries.
        return

    # Property 1: The quantized exponent is always equal to that of the right-hand operand
    assert result.as_tuple().exponent == exp.as_tuple().exponent

    # Property 2: Idempotency (quantizing an already quantized value changes nothing)
    assert result.quantize(exp, rounding=selected_rounding) == result
# End program
