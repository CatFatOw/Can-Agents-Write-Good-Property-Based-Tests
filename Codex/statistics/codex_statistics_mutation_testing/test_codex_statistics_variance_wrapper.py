from hypothesis import given, strategies as st
import pytest
import statistics
from statistics import StatisticsError
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Summary: Generate bounded integer lists, including empty and singleton
# sequences, so statistics.variance sees its documented error cases and a wide
# variety of valid sample data without overflow-prone arithmetic.
@given(st.data())
def test_variance_property(data):
    values = data.draw(
        st.lists(
            st.integers(min_value=-100_000, max_value=100_000),
            min_size=0,
            max_size=100,
        )
    )

    if len(values) < 2:
        with pytest.raises(StatisticsError):
            statistics.variance(values)
        return

    result = statistics.variance(values)

    # Sample variance uses the sum of squared deviations divided by n - 1.
    mean = statistics.mean(values)
    expected = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    assert result == pytest.approx(expected, rel=1e-12, abs=1e-12)

    # Variance cannot be negative, and constant data has zero variance.
    assert result >= 0
    if len(set(values)) == 1:
        assert result == 0

    # Adding a constant to every value does not change variance.
    offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    shifted = [value + offset for value in values]
    assert statistics.variance(shifted) == pytest.approx(
        result,
        rel=1e-12,
        abs=1e-12,
    )

    # Multiplying every value by k scales variance by k squared.
    scale = data.draw(st.integers(min_value=-10, max_value=10))
    scaled = [value * scale for value in values]
    assert statistics.variance(scaled) == pytest.approx(
        result * scale**2,
        rel=1e-12,
        abs=1e-12,
    )
# End program



