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

# np.dot() calculates the dot product between two vectors

# generate the data 
@composite 
def generate_data(draw):
    arr1 = draw(lists(integers(min_value=-50, max_value=50), min_size=1))
    arr2 = draw(lists(integers(min_value=-50, max_value=50), min_size=len(arr1), max_size=len(arr1)))
    return np.array(arr1), np.array(arr2)


# Invariant: the dot product is always a scaler 
@given(generate_data())
def test_scalar(params):
    arr1, arr2 = params
    value = np.dot(arr1, arr2)
    assert np.isscalar(value)

# Invariant: The dot product is the sum of the product of same elements, commutative,
@given(generate_data())
def test_formula(params):
    arr1, arr2 = params
    total = 0
    for i in range(len(arr1)):
        total += (arr1[i] * arr2[i])
    assert total == np.dot(arr1, arr2)
    assert np.dot(arr1, arr2) == np.dot(arr2, arr1)

# Invariant: the dot product of the same element is just sum of squares 
@given(generate_data())
def test_same(params):
    arr1, arr2 = params 
    assert np.dot(arr1, arr1) == sum([x ** 2 for x in arr1])
    assert np.dot(arr2, arr2) == sum([x ** 2 for x in arr2])

# Invariant: Scaling the dot product
@given(generate_data(), integers(min_value=-10, max_value=10))
def test_scaling(params, k):
    arr1, arr2 = params 
    assert k * np.dot(arr1, arr2) == np.dot(arr1 * k, arr2)
    assert k * np.dot(arr1, arr2) == np.dot(arr1, arr2 * k)
    

        
# Evaulate Soundness /validity
map1 = evaluate_test(test_formula)
map2 = evaluate_test(test_same)
map3 = evaluate_test(test_scalar)
map4 = evaluate_test(test_scaling)

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