from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
from decimal import Decimal
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

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





# Evaulate Soundness /validity
map1 = evaluate_test(test_gcd)
map2 = evaluate_test(test_same_value)
map3 = evaluate_test(test_zero)


results = [map1, map2, map3]

# Keep a single plotting-friendly dictionary:
# numeric fields are averaged across tests, and error fields are flattened.
total = {
    "validity": sum(result["validity"] for result in results) / len(results),
    "soundness": sum(result["soundness"] for result in results) / len(results),

    "validity_errors": set(
        error
        for result in results
        for error in result["validity_errors"]
    ),

    "soundness_errors": set(
        error
        for result in results
        for error in result["soundness_errors"]
    ),
}

print(total)