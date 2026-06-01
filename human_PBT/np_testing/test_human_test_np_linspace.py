from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------FIRST TEST: np.linspace()-----------------------------

# linspace generates a sequence of evenly spaced numbers over a specified interval
# Linespace: numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None)
# This test will focus on the parameters of: start, stop, num, endpoint (will stop be included), retstep (spacing/difference), dtype



# Generate the input (generator)
@composite 
def generate_parameters(draw):
    start = draw(integers(min_value=-80, max_value=80))
    stop = draw(integers(start, max_value=80))
    # Must be non-negative num
    num = draw(integers(min_value=0, max_value=80))
    # choose if ending value will be included or not 
    endpoint = draw(booleans())
    # include difference
    retstep = draw(booleans())
    return start, stop, num, endpoint, retstep


# Invariant 1: Test for equal spacing
@given(generate_parameters())
def test_eq_spacing(params):
    start, stop, num, endpoint, retstep = params
    #we will let retstep be true for this test
    retstep = True 
    if retstep:
        result, diff = np.linspace(start, stop, num, endpoint, retstep)
        # Assert that the diff is true
        for i in range(1, len(result)):
            assert np.isclose(result[i] - result[i-1], diff)


# Invariant 2: Test for endpoint included
@given(generate_parameters())
def test_endpoint_included_original(params):
    start, stop, num, endpoint, retstep = params

    retstep = False

    if num == 0:
        return

    result = np.linspace(start, stop, num, endpoint, retstep)

    if endpoint:
        assert np.isclose(result[-1], stop)
    else:
        assert not np.isclose(result[-1], stop)


# Invariant 3: Test for monotonic increasing 
@given(generate_parameters())
def test_monotonic_increasing(params):
    start, stop, num, endpoint, retstep = params
    retstep = False
    result = np.linspace(start, stop, num, endpoint, retstep)

    # must be always increasing 
    for i in range(1, len(result)):
        assert result[i] >= result[i-1]


        
# Evaulate Soundness /validity
map1 = evaluate_test(test_eq_spacing)
map2 = evaluate_test(test_endpoint_included_original)
map3 = evaluate_test(test_monotonic_increasing)

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