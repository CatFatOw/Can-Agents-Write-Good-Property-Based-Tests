from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
import statistics 
from statistics import  StatisticsError
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------statistics.geometric_mean()-----------------------------

# geometric_mean() takens in an array/iteral and calcaultes the geometric mean
# If input is empty it raises a statistic error
# Converts the data to flotas 



# Generate an arr of values 
@composite 
def generate_values(draw):
    """Function generates an array of values (floats or integers) from -50 to 50"""
    arr = draw(lists(integers(min_value=-50, max_value=50) | floats(min_value=-50, max_value=50).filter(lambda x: x is not None)))
    return arr 

# Invariant: calculated value == statistics.geo
@given(generate_values())
def test_geometric_mean(arr):
    """Checks to see if the geometric mean the API provides is the same"""
    try:
        geometric_mean = statistics.geometric_mean(arr, n)
        total = 1
        for x in arr:
            total *= x
        calculated_geometric_mean = total ** (1/len(arr))
        assert calculated_geometric_mean == pytest.approx(geometric_mean)
    except StatisticsError:
        pass 

# Invariant: Duplication doesn't change 
@given(generate_values())
def test_duplication(arr):
    try:
        duplicated = arr + arr 
        assert statistics.geometric_mean(duplicated) == statistics.geometric_mean(arr)
    except StatisticsError:
        pass

# Invariant: Multiplying constant scales the mean by that onstant 
@given(generate_values(), integers(min_value=-10, max_value=10).filter(lambda x: x!=0))
def test_scale_c(arr, c):
    try:
        scaled_arr = [c * x for x in arr]
        assert statistics.geometric_mean(scaled_arr) == c * statistics.geometric_mean(arr)
    except StatisticsError:
        pass

# Invariant: Ln the geometric mean should equal the geometric mean
@given(generate_values())
def test_ln(arr):
    # Logging it we get 1/k sum_1_k(ln_i)
    try:
        total = 0
        for i in range(len(arr)):
            total += math.log(arr[i])

        assert (1/len(arr)) * total == statistics.geometric_mean(arr)
    except StatisticsError:
        pass


        
# Evaulate Soundness /validity
map1 = evaluate_test(test_geometric_mean)
map2 = evaluate_test(test_duplication)
map3 = evaluate_test(test_scale_c)
map4 = evaluate_test(test_ln)

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