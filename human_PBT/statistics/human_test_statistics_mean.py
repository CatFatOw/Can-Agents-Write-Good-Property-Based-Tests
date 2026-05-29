from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
import statistics 
from statistics import  StatisticsError



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------statistics.mean()-----------------------------

# mean() returns the arithmetric mean from a sequence of iterable 
# If Data is empty, then statistics error is raised 
# statistics.mean(data) where data is a iterable or list



# Generate an arr of values 
@composite 
def generate_values(draw):
    """Function generates an array of values (floats or integers) from -50 to 50"""
    arr = draw(lists(integers(min_value=-50, max_value=50) | floats(min_value=-50, max_value=50).filter(lambda x: x is not None)))
    return arr 


# Invariant: Mean * len(arr) = sum(arr) 
@given(generate_values())
def test_check_sum(arr):
    try:
        mean_val = statistics.mean(arr)
        assert mean_val * len(arr) == sum(arr)
    except StatisticsError:
        pass

# Invariant: sum(arr) / len(arr) == mean
@given(generate_values())
def test_check_mean(arr):
    try:
        calculated_mean = sum(arr) / len(arr)
        mean_val = statistics.mean(arr)
        assert calculated_mean == pytest.approx(mean_val)
    except StatisticsError:
        pass 

# Invariant: min_val <= mean <= max_val
@given(generate_values())
def test_check_range(arr):
    try:
        mean_val = statistics.mean(arr)
        assert -50 <= mean_val and mean_val <= 50
    except StatisticsError:
        pass 

# Invariant: adding constnat to arr shifts the mean by that constant 
@given(generate_values(), integers(min_value=-10, max_value=10))
def test_shifted(arr, random_val):
    try:
        mean_val = statistics.mean(arr)
        # We shift the arr by
        shifted_arr = [x + random_val for x in arr]
        assert statistics.mean(shifted_arr) == mean_val + random_val
    except StatisticsError:
        pass 


        
# Evaulate Soundness /validity
map1 = evaluate_test(test_check_mean)
map2 = evaluate_test(test_check_range)
map3 = evaluate_test(test_check_sum)
map4 = evaluate_test(test_shifted)

results = [map1, map2, map3, map4]

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