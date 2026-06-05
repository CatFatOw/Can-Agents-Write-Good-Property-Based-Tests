from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Human written property based testing

# -------------------FIRST TEST: np.add()-----------------------------

# np.add() is elementwise addition between two np arrays only. 

# Generate data
@composite 
def generate_data(draw):
    """Function generates two equal length np arrays"""
    arr1 = draw(lists(floats(min_value=-50, max_value=50, allow_infinity=False, allow_nan=False), min_size=1))
    arr2 = draw(lists(floats(min_value=-50, max_value=50, allow_infinity=False, allow_nan=False), min_size=len(arr1), max_size=len(arr1)))
    return np.array(arr1), np.array(arr2)

# Invariant: Addition preserves shape and length
@given(generate_data())
def test_preservation(params):
    arr1, arr2 = params
    new_arr = np.add(arr1, arr2)
    assert len(new_arr) == len(arr1) and len(new_arr) == len(arr2)
    assert new_arr.shape == arr1.shape and new_arr.shape == arr2.shape

# Invariant: addition is commutative and adding 0 is just the array itself
@given(generate_data())
def test_commutative(params):
    arr1, arr2 = params 
    assert np.array_equal(np.add(arr1, arr2), np.add(arr2, arr1))
    assert np.array_equal(np.add(arr1, 0), arr1) 
    assert np.array_equal(np.add(arr2, 0), arr2)

# Invariant: dtype is consistant with numpy's standard dtype promotion 
@given(generate_data())
def test_dtype(params):
    arr1, arr2 = params 
    assert np.add(arr1, arr2).dtype == (arr1+arr2).dtype


        
