from decimal import Decimal
from fractions import Fraction
import math
from pathlib import Path
import sys

from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test



from hypothesis import given, strategies as st

# Summary: Generates full-spectrum Decimal instances including NaNs, Infinities, 
# and extreme scales, utilizing arbitrary-precision Fraction comparison for 
# 100% test soundness unaffected by standard local context precision limits.
@given(st.data())
def test_as_integer_ratio(data):
    d = data.draw(st.decimals(allow_nan=True, allow_infinity=True))
    
    # 1. Handle exceptional edge-cases defined by the API
    if d.is_nan():
        try:
            d.as_integer_ratio()
            assert False, "Expected ValueError on NaN values"
        except ValueError:
            return
            
    elif d.is_infinite():
        try:
            d.as_integer_ratio()
            assert False, "Expected OverflowError on Infinity values"
        except OverflowError:
            return
            
    # 2. Handle standard finite decimals
    else:
        n, denom = d.as_integer_ratio()
        
        # Verify output types
        assert isinstance(n, int), "Numerator must be an integer"
        assert isinstance(denom, int), "Denominator must be an integer"
        
        # Verify denominator constraints
        assert denom > 0, "Denominator must be strictly positive"
        
        # Verify lowest terms constraint (coprime check)
        assert math.gcd(n, denom) == 1, "Fraction must be in lowest terms"
        
        # Verify exact structural mathematical equivalence.
        # Converting directly to Fraction ensures no precision loss or context clipping.
        assert Fraction(d) == Fraction(n, denom), "Fraction value does not exactly equal original Decimal"

# End program
if __name__ == "__main__":
    print(evaluate_test(test_as_integer_ratio))
