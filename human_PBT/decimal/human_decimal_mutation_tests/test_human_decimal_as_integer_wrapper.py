from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
from decimal import Decimal
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Human written property based testing

# -------------------Decimal().as_integer_ratio()-----------------------------
# Method on Decimal() object, and reuturns a pair of numbers: (numerator, denominaotr) that expresses the decimal as a fraction



# Invariant: The expressed fraction of n/d should be equivalent to the original data 
@given(floats(min_value=-50, max_value=50))
def test_same_value(number):
    try:
        decimal_value = Decimal(str(number))
        n, d = decimal_value.as_integer_ratio()
        assert number == pytest.approx(n/d)
    except ValueError:
        pass

# Invariant: The n, d must be in full reduced form 
@given(floats(min_value=-50, max_value=50))
def test_gcd(number):
    decimal_value = Decimal(str(number))
    n, d = decimal_value.as_integer_ratio()
    assert math.gcd(n, d) == 1

# Invariant: the denominator must never be 0 and if 0, the numerator must be 0
@given(floats(min_value=-50, max_value=50))
def test_zero(number):
    decimal_value = Decimal(str(number))
    n, d = decimal_value.as_integer_ratio()
    assert d != 0
    if number == 0:
        assert n == 0





