from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
import statistics 
from statistics import  StatisticsError
import math

PROJECT_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "metrics.py").is_file()
)
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------statistics.correlation()-----------------------------

# correlation() takes two arrays and measures the correlation coefficnet -1 <= r <= 1
# Where -1 is perfect neg, 1 is perfect pos, and 0 is no linear correlation. 


# Generate the two arrays
@composite 
def generate_two_arrs(draw):
    arr1 = draw(lists(integers(min_value=-10000, max_value=10000), min_size=2, max_size=50))
    arr2 = draw(lists(integers(min_value=-10000, max_value=10000), min_size=len(arr1), max_size=len(arr1)))

    assume(len(set(arr1)) > 1)
    assume(len(set(arr2)) > 1)
    return arr1, arr2


# Invariant 1: The result has to be between -1 <= r <= 1
@given(generate_two_arrs())
def test_between_bounds(params):
    try:
        arr1, arr2 = params
        correlation = statistics.correlation(arr1, arr2)
        assert -1 - 1e-9 <= correlation <= 1 + 1e-9
    except StatisticsError:
        pass

# invariant 2: The correlation of itself should be 1
@given(generate_two_arrs())
def test_same(params):
    try:
        arr1, arr2 = params
        correlation = statistics.correlation(arr1, arr1)
        assert correlation == pytest.approx(1)
    
    except StatisticsError:
        pass

# invariant 3: symmetry
@given(generate_two_arrs())
def test_symmetry(params):
    try:
        arr1, arr2 = params
        correlation1 = statistics.correlation(arr1, arr2)
        correlation2 = statistics.correlation(arr2, arr1)
        assert correlation1 == correlation2
    except StatisticsError:
        pass

# Invariant 4: scaling doesn't impact 
@given(generate_two_arrs(), floats(allow_nan=False, min_value=-10, max_value=10))
def test_scale(params, scale):
    try:
        arr1, arr2 = params
        original = statistics.correlation(arr1, arr2)
        scaled = statistics.correlation([x*scale for x in arr1], [x*scale for x in arr2])
        assert scaled == pytest.approx(original)
        
    except StatisticsError:
        pass


# # Evaulate Soundness /validity
# map1 = evaluate_test(test_between_bounds)
# map2 = evaluate_test(test_same)
# map3 = evaluate_test(test_scale)
# map4 = evaluate_test(test_symmetry)

# results = [map1, map2, map3, map4]

# # Keep a single plotting-friendly dictionary:
# # numeric fields are averaged across tests, and error fields are flattened.
# total = {
#     "validity": sum(result["validity"] for result in results) / len(results),
#     "soundness": sum(result["soundness"] for result in results) / len(results),

#     "validity_errors": set(
#         error
#         for result in results
#         for error in result["validity_errors"]
#     ),

#     "soundness_errors": set(
#         error
#         for result in results
#         for error in result["soundness_errors"]
#     ),
# }

# print(total)