from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
import statistics 
from statistics import  StatisticsError
import math


PROJECT_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "metrics.py").is_file()
)
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------statistics.linear_regression()-----------------------------

# linear_regression() returns the slope and intercept of simple linear regression via the formula y = mx + b
# inputs must be same length and intercept, we can generate an array of x values though

@composite 
def generate_data_points(draw):
    x = draw(lists(
        integers(min_value=-50, max_value=50),
        min_size=2,
        max_size=30,
        unique=True
    ))

    y = draw(lists(
        floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False),
        min_size=len(x),
        max_size=len(x)
    ))

    return x, y

# Invariant: Adding constant to every x-value should keep slope the same
@given(generate_data_points(), floats(min_value=-10, max_value=10, allow_nan=False))
def test_same_slope(params, constant):
    try:
        x, y = params
        slope, intercept = statistics.linear_regression(x, y)
        # Modify the x
        x_added = [val + constant for val in x]
        slope_modified, intercept = statistics.linear_regression(x_added, y)
        assert slope == pytest.approx(slope_modified)
    except StatisticsError:
        pass

# Invariant: scaling y by constant scales the slope by k
@given(generate_data_points(), floats(min_value=-10, max_value=10,allow_nan=False))
def test_scale_slope(params, constant):
    try:
        x, y = params 
        slope, intercept = statistics.linear_regression(x,y)
        # Scale y
        y_scaled = [constant * val for val in y]
        new_slope, new_intercept = statistics.linear_regression(x, y_scaled)
        assert new_slope == pytest.approx(slope * constant)
    except StatisticsError:
        pass

# Invariant: Same linear equation 
@given(generate_data_points(), floats(min_value=-10, max_value=10, allow_nan=False), floats(min_value=-10, max_value=10, allow_nan=False))
def test_same_equation(params, slope, intercept):
    try:
        x, _ = params 
        # Create own linear equation
        y = [slope * val + intercept for val in x]
        
        new_slope, new_intercept = statistics.linear_regression(x, y)
        assert new_slope == pytest.approx(slope)
        assert new_intercept == pytest.approx(intercept)

    except StatisticsError:
        pass

        
# # Evaulate Soundness /validity
# map1 = evaluate_test(test_same_equation)
# map2 = evaluate_test(test_same_slope)
# map3 = evaluate_test(test_scale_slope)
# results = [map1, map2, map3]

# # Keep a single plotting-friendly dictionary:
# # numeric fields are averaged across tests, and error fields are flattened.
# total = {
#     "validity": sum(result["validity"] for result in results) / len(results),
#     "soundness": sum(result["soundness"] for result in results) / len(results),

#     "validity_errors": set(
#         error
#         for result in results
#         for error in result["validity_errors"]
#     ),

#     "soundness_errors": set(
#         error
#         for result in results
#         for error in result["soundness_errors"]
#     ),
# }

# print(total)