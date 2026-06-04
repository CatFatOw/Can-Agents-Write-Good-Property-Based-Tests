from hypothesis import given, strategies as st
from decimal import Decimal
import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Summary: Draw pairs of arbitrary Decimal values including NaNs and Infinities to validate that compare() accurately maps their ordering relationships to -1, 0, 1, or NaN.
from hypothesis import given, strategies as st
from decimal import Decimal, localcontext, InvalidOperation

# Summary: Draw pairs of arbitrary Decimals. We use a local context to untrap InvalidOperation so that signaling NaNs (sNaN) return a quiet NaN instead of raising a test-crashing exception.
@given(st.data())
def test_compare(data):
    a = data.draw(st.decimals())
    b = data.draw(st.decimals())
    
    with localcontext() as ctx:
        ctx.traps[InvalidOperation] = False
        res = a.compare(b)
    
    assert isinstance(res, Decimal)
    
    if a.is_nan() or b.is_nan():
        assert res.is_nan()
    elif a < b:
        assert res == Decimal('-1')
    elif a == b:
        assert res == Decimal('0')
    elif a > b:
        assert res == Decimal('1')
# End program
