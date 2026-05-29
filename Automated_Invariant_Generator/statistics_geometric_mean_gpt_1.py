from __future__ import annotations

import math
import statistics
from decimal import Decimal
from fractions import Fraction

import pytest
from hypothesis import assume, given, strategies as st
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1] 
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# --- Generators ---

positive_floats = st.floats(
    min_value=1e-12,
    max_value=1e12,
    allow_nan=False,
    allow_infinity=False,
    exclude_min=True,
)

positive_ints = st.integers(min_value=1, max_value=10**9)

positive_decimals = st.decimals(
    min_value=Decimal("1e-12"),
    max_value=Decimal("1e12"),
    allow_nan=False,
    allow_infinity=False,
    places=12,
)

positive_fractions = st.builds(
    Fraction,
    st.integers(min_value=1, max_value=10**6),
    st.integers(min_value=1, max_value=10**6),
).filter(lambda x: x > 0)

positive_numeric = st.one_of(
    positive_ints,
    positive_floats,
    positive_decimals,
    positive_fractions,
)

positive_numeric_lists = st.lists(positive_numeric, min_size=1, max_size=20)

positive_numeric_lists_no_extremes = st.lists(
    st.floats(
        min_value=1e-6,
        max_value=1e6,
        allow_nan=False,
        allow_infinity=False,
        exclude_min=True,
    ),
    min_size=1,
    max_size=20,
)


def _gm(xs):
    return statistics.geometric_mean(xs)


# --- Invariants ---

@given(positive_numeric_lists)
def test_geometric_mean_is_positive_for_positive_inputs(xs):
    # Sound: for strictly positive inputs, geometric mean should be strictly positive.
    result = _gm(xs)
    assert result > 0
    assert math.isfinite(float(result))


@given(positive_numeric_lists)
def test_geometric_mean_of_all_equal_values_equals_that_value(xs):
    # If all values are identical, the geometric mean should equal that common value.
    x = xs[0]
    ys = [x] * len(xs)
    result = _gm(ys)
    assert result == x or math.isclose(float(result), float(x), rel_tol=1e-12, abs_tol=0.0)


@given(positive_numeric_lists_no_extremes, positive_numeric_lists_no_extremes)
def test_geometric_mean_is_homogeneous_under_scaling(xs, ys):
    # Risky/conditional: numeric stability may slightly affect exactness.
    # For a positive scalar c, gm(c*x_i) should be c * gm(x_i).
    assume(len(xs) == len(ys))
    c = 3.5
    left = _gm([c * x for x in xs])
    right = c * _gm(xs)
    assert math.isclose(float(left), float(right), rel_tol=1e-12, abs_tol=1e-12)


@given(positive_floats, positive_floats)
def test_geometric_mean_of_two_values_matches_sqrt_product(a, b):
    # For two positive numbers, gm(a, b) = sqrt(a*b).
    result = _gm([a, b])
    expected = math.sqrt(a * b)
    assert math.isclose(float(result), expected, rel_tol=1e-12, abs_tol=1e-12)


@given(st.lists(st.one_of(st.just(0), st.floats(max_value=0, allow_nan=False, allow_infinity=False)), min_size=1, max_size=20))
def test_geometric_mean_rejects_nonpositive_values(xs):
    # Sound: zeros and negative values must raise StatisticsError.
    with pytest.raises(statistics.StatisticsError):
        _gm(xs)


@given(st.just([]))
def test_geometric_mean_rejects_empty_input(xs):
    # Sound: empty datasets must raise StatisticsError.
    with pytest.raises(statistics.StatisticsError):
        _gm(xs)


# ACCESS Validity/Soundness

results = [
    evaluate_test(test_geometric_mean_is_positive_for_positive_inputs),
    evaluate_test(test_geometric_mean_of_all_equal_values_equals_that_value),
    evaluate_test(test_geometric_mean_is_homogeneous_under_scaling),
    evaluate_test(test_geometric_mean_of_two_values_matches_sqrt_product),
    evaluate_test(test_geometric_mean_rejects_nonpositive_values),
    evaluate_test(test_geometric_mean_rejects_empty_input),
]

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
