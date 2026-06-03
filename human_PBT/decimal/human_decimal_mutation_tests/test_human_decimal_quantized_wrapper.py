from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
from decimal import Decimal, getcontext, InvalidOperation
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Human written property based testing

# -------------------Decimal.quantize()-----------------------------
# Round decimal to match the exponent (number of decimal places of another decimal)
# Makes decimal have same number of decimal places as other other decimal

# Invariant: ideompt (quantiziing twice == quantizing once) 
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), sampled_from([Decimal("1"), Decimal("0.1"), Decimal("0.01"), Decimal("0.001"), Decimal("0.0001")]))
def test_ideompt(x, exponent):
    x = Decimal(str(x))
    assert x.quantize(exponent) == x.quantize(exponent).quantize(exponent)

# Invariant: special cases like nan, infinity, -infinity
@given(sampled_from([Decimal("1"), Decimal("0.1"), Decimal("0.01"), Decimal("0.001"), Decimal("0.0001")]))
def test_special_cases(exponent):
    nan_value = Decimal("nan")
    inf_value = Decimal("Infinity")
    neg_inf_value = Decimal("-Infinity")



    # nan should stay nan
    assert nan_value.quantize(exponent).is_nan()
    # Infinity should rase Invalid Operation error 
    with pytest.raises(InvalidOperation):
        inf_value.quantize(exponent)
    with pytest.raises(InvalidOperation):
        neg_inf_value.quantize(exponent)


    
# Invariant: The results should have the same expoenents as the target
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), sampled_from([Decimal("1"), Decimal("0.1"), Decimal("0.01"), Decimal("0.001"), Decimal("0.0001")]))
def test_same_exponent(x, q:Decimal):
    x = Decimal(str(x))
    result = x.quantize(q)
    assert result.as_tuple().exponent == q.as_tuple().exponent
    


