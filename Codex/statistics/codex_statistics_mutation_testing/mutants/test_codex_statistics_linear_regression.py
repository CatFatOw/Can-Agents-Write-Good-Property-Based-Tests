from hypothesis import given, settings, strategies as st
import pytest
import statistics
from pathlib import Path
import sys


PROJECT_ROOT = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "metrics.py").is_file()
)
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


ABS_TOLERANCE = 1e-9


@st.composite
def regression_inputs(draw, min_size=2, max_size=50):
    x = draw(
        st.lists(
            st.integers(min_value=-10_000, max_value=10_000),
            min_size=min_size,
            max_size=max_size,
        ).filter(lambda values: len(set(values)) > 1)
    )
    y = draw(
        st.lists(
            st.integers(min_value=-10_000, max_value=10_000),
            min_size=len(x),
            max_size=len(x),
        )
    )
    return x, y


# Summary: Generate equal-length sequences of bounded integers with at least
# two distinct x-values so linear_regression is defined and transformations
# remain far from overflow. Check exact lines, the fitted centroid, translations
# of each axis, and scaling of y.
@settings(max_examples=25)
@given(st.data())
def test_linear_regression_property(data):
    x, y = data.draw(regression_inputs())
    result = statistics.linear_regression(x, y)

    # The fitted line passes through the centroid of the observed data.
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(y)
    assert result.slope * x_mean + result.intercept == pytest.approx(
        y_mean,
        rel=1e-10,
        abs=ABS_TOLERANCE,
    )

    # Data drawn from an exact line recovers that line's slope and intercept.
    exact_slope = data.draw(st.integers(min_value=-100, max_value=100))
    exact_intercept = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    exact_y = [exact_slope * value + exact_intercept for value in x]
    exact_result = statistics.linear_regression(x, exact_y)
    assert exact_result.slope == pytest.approx(exact_slope, abs=ABS_TOLERANCE)
    assert exact_result.intercept == pytest.approx(
        exact_intercept,
        abs=ABS_TOLERANCE,
    )

    # Adding a constant to x leaves the slope unchanged and adjusts intercept.
    x_offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    shifted_x = [value + x_offset for value in x]
    shifted_x_result = statistics.linear_regression(shifted_x, y)
    assert shifted_x_result.slope == pytest.approx(result.slope, abs=ABS_TOLERANCE)
    assert shifted_x_result.intercept == pytest.approx(
        result.intercept - result.slope * x_offset,
        rel=1e-10,
        abs=ABS_TOLERANCE,
    )

    # Adding a constant to y leaves the slope unchanged and shifts intercept.
    y_offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    shifted_y = [value + y_offset for value in y]
    shifted_y_result = statistics.linear_regression(x, shifted_y)
    assert shifted_y_result.slope == pytest.approx(result.slope, abs=ABS_TOLERANCE)
    assert shifted_y_result.intercept == pytest.approx(
        result.intercept + y_offset,
        rel=1e-10,
        abs=ABS_TOLERANCE,
    )

    # Scaling y scales both output coefficients by the same constant.
    y_scale = data.draw(st.integers(min_value=-10, max_value=10))
    scaled_y = [value * y_scale for value in y]
    scaled_y_result = statistics.linear_regression(x, scaled_y)
    assert scaled_y_result.slope == pytest.approx(
        result.slope * y_scale,
        rel=1e-10,
        abs=ABS_TOLERANCE,
    )
    assert scaled_y_result.intercept == pytest.approx(
        result.intercept * y_scale,
        rel=1e-10,
        abs=ABS_TOLERANCE,
    )
# End program



