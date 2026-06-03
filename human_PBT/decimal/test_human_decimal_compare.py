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

# -------------------Decimal().compare()-----------------------------
# if self < other returns -1 
# if self == other returns 0
# if self > other returns 1
# Either is NaN returns NAN



# Invariant: The return values are correct 
@given(
    floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
    floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
)
def test_correct_return(num1, num2):
    value = Decimal(str(num1)).compare(Decimal(str(num2)))
    if num1 > num2:
        assert value == Decimal("1")
    elif num1 < num2:
        assert value == Decimal("-1")
    elif num1 == num2:
        assert value == Decimal("0")

# Invariant: reflexive for all a, (a, a) E R
@given(floats(min_value=-50, max_value=50, allow_infinity=False, allow_nan=False))
def test_reflexivity(x):
    assert Decimal(str(x)).compare(Decimal(str(x))) == Decimal("0")

# Invariant: symmetric 
# (a, b) E R and (b, a) E R
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False), floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False))
def test_symmetric(num1, num2):
    if num1 != 0 and num2 !=0 and num1 != num2:
        if num1 > num2:
            assert Decimal(str(num1)).compare(Decimal(str(num2))) == Decimal("1")
            assert Decimal(str(num2)).compare(Decimal(str(num1))) == Decimal("-1")
        else:
            assert Decimal(str(num1)).compare(Decimal(str(num2))) == Decimal("-1")
            assert Decimal(str(num2)).compare(Decimal(str(num1))) == Decimal("1")

# Invariant: Transitive 
# If (a,b) E R ^ (b, c) E R -> (a, c) E R 
@given(
    integers(min_value=-50, max_value=48),
    integers(min_value=1, max_value=49),
    integers(min_value=1, max_value=50),
)
def test_transitivity(a, gap1, gap2):
    b = a + gap1
    c = b + gap2
    assume(c <= 50)

    assert Decimal(str(a)).compare(Decimal(str(b))) == Decimal("-1")
    assert Decimal(str(b)).compare(Decimal(str(c))) == Decimal("-1")
    assert Decimal(str(a)).compare(Decimal(str(c))) == Decimal("-1")

# Test nan 
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False))
def test_nan_return(num):
    assert Decimal("NaN").compare(Decimal(str(num))).is_nan()
    assert Decimal(str(num)).compare(Decimal("NaN")).is_nan()



# Evaulate Soundness /validity
map1 = evaluate_test(test_correct_return)
map2 = evaluate_test(test_reflexivity)
map3 = evaluate_test(test_symmetric)
map4 = evaluate_test(test_transitivity)
map5 = evaluate_test(test_nan_return)


results = [map1, map2, map3, map4, map5]

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