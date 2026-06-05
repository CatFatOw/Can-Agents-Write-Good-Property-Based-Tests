from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------np.sum()-----------------------------
# Finds finds the sum of an an tensor/array. if no axis is given, it find sthe total sum. 
# If axis=0, it finds the cumulative row sum for each each olumn. If axis=1, it finds the cumulative col sum for each row


# Invariant 1: if not axis, it gives the total sum, if axis=0, it gives the row sum via columns, and if axis = 1, it gives the col sum via row
@given(integers(min_value=1, max_value=4), integers(min_value=1, max_value=4))
def test_axis(row, col):
    # Test no axis specified

    array = np.random.randn(row, col)
    total = 0
    for r in range(len(array)):
        for c in range(len(array[0])):
            total += array[r][c]
    assert np.allclose(total,np.sum(array))

    # If axis = 0 specfied 
    array = np.random.randn(row, col)
    result = []
    for c in range(len(array[0])):
        total = 0
        for r in range(len(array)):
            total += array[r][c]
        result.append(total)
    assert np.allclose(np.sum(array, axis=0), result)

    # If axis = 1 specified 
    result = []
    for r in range(len(array)):
        total = 0
        for c in range(len(array[0])):
            total += array[r][c]
        result.append(total)
    assert np.allclose(np.sum(array, axis=1), result)

# Invariant: Mean case + if empty the sum is 0
@given(integers(min_value=1, max_value=4), integers(min_value=1, max_value=4))
def test_edge_cases(row, col):
    array = np.random.rand(row, col)
    assert np.allclose(np.sum(array), np.mean(array) * array.size)
    assert np.sum([]) == 0

# Invariant: Scalar multiplication
@given(integers(min_value=1, max_value=4), integers(min_value=1, max_value=4), integers(min_value=-5, max_value=5))
def test_scalar(row, col, k):
    array = np.random.randn(row, col)
    assert np.allclose(k * np.sum(array), np.sum(k * array))



        
# Evaulate Soundness /validity
map1 = evaluate_test(test_axis)
map2 = evaluate_test(test_edge_cases)
map3 = evaluate_test(test_scalar)


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