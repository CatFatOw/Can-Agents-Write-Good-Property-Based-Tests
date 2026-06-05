from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------np.cumsum()-----------------------------

# np.cumsum() calculates the running/prefix sum of an np array

#Invariant: np.cumsum() last value == sum of the np array and shape is preserved
@given(lists(integers(min_value=-50, max_value=50), min_size=1))
def test_sum(arr):
    arr = np.array(arr)
    prefix = np.cumsum(arr)
    assert prefix[-1] == np.sum(arr)
    assert prefix.shape == arr.shape

# Invariant: Multiplicating every element also scales the cumsum result
@given(lists(integers(min_value=-50, max_value=50), min_size=1), integers(min_value=-5, max_value=5))
def test_scale(arr, k):
    arr = np.array(arr)
    prefix = np.cumsum(arr)
    assert np.array_equal(k * prefix, np.cumsum(k*arr))

# Invariant: prefix[i] - prefix[i-1] == arr[i]
@given(lists(integers(min_value=-50, max_value=50), min_size=1))
def test_range_sum(arr):
    arr = np.array(arr)
    prefix = np.cumsum(arr)
    for i in range(1, len(arr)):
        assert prefix[i] - prefix[i-1] == arr[i]


        
# Evaulate Soundness /validity
map1 = evaluate_test(test_range_sum)
map2 = evaluate_test(test_scale)
map3 = evaluate_test(test_sum)

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