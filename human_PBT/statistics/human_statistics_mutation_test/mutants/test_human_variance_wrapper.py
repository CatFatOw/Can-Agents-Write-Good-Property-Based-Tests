from hypothesis import given, settings, Verbosity, note, assume
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

# -------------------statistics.variance()-----------------------------

# variance() takes in an iterable list and finds the variance

# Invariant: multiple arr by k and variance scaled by k^2
@given(lists(integers(), min_size=2), integers())
def test_scale_k(arr, k):
    original_var = statistics.variance(arr)
    scaled_arr = [k * val for val in arr]
    scaled_var = statistics.variance(scaled_arr)
    assert pytest.approx(original_var * (k ** 2)) == scaled_var

# Invairant: adding a number results in same var
@given(lists(integers(), min_size=2), integers())
def test_add(arr, k):
    original_var = statistics.variance(arr)
    new_arr = [val + k for val in arr]
    new_var = statistics.variance(new_arr)
    assert new_var == pytest.approx(original_var)

# Invariant: vairance can never be non-negative
@given(lists(integers(), min_size=2))
def test_neg(arr):
    var = statistics.variance(arr)
    assert var >= 0



