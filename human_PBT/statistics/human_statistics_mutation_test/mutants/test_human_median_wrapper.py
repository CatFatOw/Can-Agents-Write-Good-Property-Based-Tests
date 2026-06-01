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

# -------------------statistics.median()-----------------------------

# median() finds the middle element if odd, else avg of two middle if even


# Invariant 1: sorted answer == unsorted answer 
@given(lists(integers(), min_size=1))
def test_sorted(arr):
    sorted_arr = sorted(arr.copy())
    assert statistics.median(sorted_arr) == statistics.median(arr)

# Invariant 2: if odd, its the middle index, else it should be the two for even
@given(lists(integers(), min_size=1))
def test_correct_idx(arr):
    arr = sorted(arr)

    left = 0
    right = len(arr) - 1
    mid = (left + right) // 2

    if len(arr) % 2 != 0:
        assert statistics.median(arr) == arr[mid]
    else:
        assert statistics.median(arr) == (arr[mid] + arr[mid + 1]) / 2

# invariants 3: Negative scaling is the same value but sign flipped 
@given(lists(integers(), min_size=1))
def test_sign(arr):
    flipped_arr = [val * -1 for val in arr]
    assert statistics.median(flipped_arr) == -1 * statistics.median(arr)



