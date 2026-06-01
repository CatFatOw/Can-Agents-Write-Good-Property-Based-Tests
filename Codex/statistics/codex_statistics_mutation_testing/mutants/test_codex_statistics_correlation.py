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


@st.composite
def non_constant_integer_lists(draw, min_size=2, max_size=50):
    values = draw(
        st.lists(
            st.integers(min_value=-10_000, max_value=10_000),
            min_size=min_size,
            max_size=max_size,
        ).filter(lambda items: len(set(items)) > 1)
    )
    return values


# Summary: Generate equally sized, non-constant sequences of bounded integers
# so correlation is defined and arithmetic transformations stay far from
# overflow. Check its range, symmetry, self-correlation, translation
# invariance, and behavior under non-zero scaling.
@settings(max_examples=25)
@given(st.data())
def test_correlation_property(data):
    x = data.draw(non_constant_integer_lists())
    y = data.draw(non_constant_integer_lists(min_size=len(x), max_size=len(x)))

    result = statistics.correlation(x, y)

    # A Pearson correlation coefficient is between -1 and 1, modulo tiny
    # floating-point rounding at the boundary.
    assert -1 - 1e-8 <= result <= 1 + 1e-8

    # Correlation is symmetric.
    assert statistics.correlation(y, x) == pytest.approx(result, abs=1e-12)

    # Any non-constant sequence is perfectly correlated with itself.
    assert statistics.correlation(x, x) == pytest.approx(1.0, abs=1e-12)

    # Adding constants does not change correlation.
    x_offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    y_offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    shifted_x = [value + x_offset for value in x]
    shifted_y = [value + y_offset for value in y]
    assert statistics.correlation(shifted_x, shifted_y) == pytest.approx(
        result,
        abs=1e-12,
    )

    # Scaling either sequence flips the sign only for a negative scale.
    x_scale = data.draw(
        st.integers(min_value=-10, max_value=10).filter(lambda value: value != 0)
    )
    y_scale = data.draw(
        st.integers(min_value=-10, max_value=10).filter(lambda value: value != 0)
    )
    scaled_x = [value * x_scale for value in x]
    scaled_y = [value * y_scale for value in y]
    expected = result if x_scale * y_scale > 0 else -result
    assert statistics.correlation(scaled_x, scaled_y) == pytest.approx(
        expected,
        abs=1e-12,
    )
# End program


