import math
from fractions import Fraction
from decimal import Decimal
from statistics import mean, StatisticsError
import sys
from pathlib import Path

from hypothesis import given, assume, strategies as st

PROJECT_ROOT = Path(__file__).resolve().parents[1] / "PBT_Agents"
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# --- Generators ---

def finite_int_lists(min_size=1, max_size=50):
    return st.lists(
        st.integers(min_value=-10**9, max_value=10**9),
        min_size=min_size,
        max_size=max_size,
    )


def finite_float_lists(min_size=1, max_size=30):
    return st.lists(
        st.floats(allow_nan=False, allow_infinity=False, width=64),
        min_size=min_size,
        max_size=max_size,
    )


def finite_fraction_lists(min_size=1, max_size=20):
    num = st.integers(min_value=-1000, max_value=1000)
    den = st.integers(min_value=1, max_value=1000)
    return st.lists(st.builds(Fraction, num, den), min_size=min_size, max_size=max_size)


def finite_decimal_lists(min_size=1, max_size=20):
    # Keep decimal values simple and finite.
    ints = st.integers(min_value=-10**6, max_value=10**6).map(Decimal)
    return st.lists(ints, min_size=min_size, max_size=max_size)


# --- Invariants ---

@given(finite_int_lists())
def test_mean_matches_exact_arithmetic_for_ints(xs):
    # For integers, mean should equal exact sum/n as a Fraction.
    expected = Fraction(sum(xs), len(xs))
    assert mean(xs) == expected


@given(finite_fraction_lists())
def test_mean_matches_exact_arithmetic_for_fractions(xs):
    # For Fraction inputs, arithmetic mean is exact.
    expected = sum(xs, Fraction(0, 1)) / len(xs)
    assert mean(xs) == expected


@given(finite_decimal_lists())
def test_mean_matches_exact_arithmetic_for_decimals(xs):
    # For Decimal inputs, arithmetic mean should preserve Decimal arithmetic.
    expected = sum(xs, Decimal(0)) / Decimal(len(xs))
    assert mean(xs) == expected


@given(finite_float_lists())
def test_mean_with_duplicate_concatenation_is_stable_for_floats(xs):
    # Risky/conditional: exact equality can fail for some float arrangements due to rounding.
    # Still sound when duplicating a list and comparing to the same mean value in floating arithmetic.
    assume(len(xs) > 0)
    m = mean(xs)
    doubled = xs + xs
    md = mean(doubled)
    assert math.isfinite(m)
    assert math.isfinite(md)
    assert md == m


@given(finite_int_lists())
def test_mean_is_within_data_bounds_for_ints(xs):
    # The arithmetic mean lies between min and max of the data.
    m = mean(xs)
    assert min(xs) <= m <= max(xs)


@given(st.lists(st.integers(), min_size=0, max_size=20))
def test_empty_data_raises_statistics_error(xs):
    assume(len(xs) == 0)
    try:
        mean(xs)
        assert False, "Expected StatisticsError for empty data"
    except StatisticsError:
        pass


# ACCESS Validity/Soundness
results = [
    evaluate_test(test_mean_matches_exact_arithmetic_for_ints),
    evaluate_test(test_mean_matches_exact_arithmetic_for_fractions),
    evaluate_test(test_mean_matches_exact_arithmetic_for_decimals),
    evaluate_test(test_mean_with_duplicate_concatenation_is_stable_for_floats),
    evaluate_test(test_mean_is_within_data_bounds_for_ints),
    evaluate_test(test_empty_data_raises_statistics_error),
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
