from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------np.linalg.norm()-----------------------------
# calculates the norm given an ord (by default ord=2, the euclidian norm)
# sum from i = 1 to n abs(x_i)^p ) ^ (1/p)


# Generate two same arrays
from hypothesis import given
from hypothesis.strategies import integers, composite, lists, sampled_from
import numpy as np

@composite
def generate_data(draw):
    arr1 = draw(lists(integers(-50, 50), min_size=1, max_size=50))
    arr2 = draw(lists(integers(-50, 50), min_size=len(arr1), max_size=len(arr1)))
    return np.array(arr1, dtype=float), np.array(arr2, dtype=float)

ord_strategy = sampled_from([1, 2, 3, 4, np.inf])

# Invariant: square of L2 norm equals dot product
@given(lists(integers(-50, 50), min_size=1, max_size=50))
def test_l2norm(arr):
    array = np.array(arr, dtype=float)
    assert np.isclose(np.linalg.norm(array, ord=2) ** 2, np.dot(array, array))

# Invariant: norm(a+b) <= norm(a) + norm(b)
@given(generate_data(), ord_strategy)
def test_triangle(params, p):
    arr1, arr2 = params
    left = np.linalg.norm(arr1 + arr2, ord=p)
    right = np.linalg.norm(arr1, ord=p) + np.linalg.norm(arr2, ord=p)

    assert left <= right or np.isclose(left, right)

# Invariant: zero norm is 0, infinity norm is max absolute value
@given(lists(integers(-50, 50), min_size=1, max_size=50))
def test_specific_norms(arr):
    zeros = np.zeros((5, 5))
    array = np.array(arr, dtype=float)

    assert np.linalg.norm(zeros) == 0
    assert np.linalg.norm(array, ord=np.inf) == max(abs(x) for x in arr)




        
# Evaulate Soundness /validity
map1 = evaluate_test(test_l2norm)
map2 = evaluate_test(test_specific_norms)
map3 = evaluate_test(test_triangle)


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