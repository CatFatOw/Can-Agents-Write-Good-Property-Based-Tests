from hypothesis import given, strategies as st
from decimal import Decimal
import math
import sys 
from pathlib import Path 


# Summary: Generate a diverse mix of arbitrary integers and floats—explicitly enabling NaN and infinity configurations—to evaluate type casting, boundary limits, and strict value precision.
@given(st.data())
def test_from_float(data):
    # Dynamically draw an input that matches the accepted types (int or float)
    input_val = data.draw(st.one_of(st.integers(), st.floats(allow_nan=True, allow_infinity=True)))
    
    # Execute the alternative constructor
    result = Decimal.from_float(input_val)
    
    # Property 1: Output must be a Decimal instance
    assert isinstance(result, Decimal)
    
    # Property 2: Handle NaN safely
    if isinstance(input_val, float) and math.isnan(input_val):
        assert result.is_nan()
        
    # Property 3: Handle positive and negative infinities correctly
    elif isinstance(input_val, float) and math.isinf(input_val):
        assert result.is_infinite()
        assert math.copysign(1, input_val) == math.copysign(1, float(result))
        
    # Property 4: Finite numbers must reflect their exact binary-to-decimal representation
    else:
        assert result == Decimal(input_val)

# End program
