from hypothesis import given, strategies as st
import pytest
import statistics
from statistics import StatisticsError
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Summary: Generate empty, singleton, and multi-element lists of bounded
# integers so median sees odd and even lengths without overflow risk. Check the
# documented sorted definition, input-order invariance, translation behavior,
# and behavior under positive or negative scaling.
@given(st.data())
def test_median_property(data):
    values = data.draw(
        st.lists(
            st.integers(min_value=-1_000_000, max_value=1_000_000),
            min_size=0,
            max_size=100,
        )
    )

    if not values:
        with pytest.raises(StatisticsError):
            statistics.median(values)
        return

    result = statistics.median(values)
    sorted_values = sorted(values)
    midpoint = len(sorted_values) // 2

    # Odd-length data returns the middle sorted value. Even-length data returns
    # the arithmetic mean of the two middle sorted values.
    if len(sorted_values) % 2:
        expected = sorted_values[midpoint]
    else:
        expected = (sorted_values[midpoint - 1] + sorted_values[midpoint]) / 2
    assert result == expected

    # Sorting or reversing the input does not change its median.
    assert statistics.median(sorted_values) == result
    assert statistics.median(list(reversed(values))) == result

    # Adding a constant to every value shifts the median by that constant.
    offset = data.draw(st.integers(min_value=-1_000, max_value=1_000))
    shifted = [value + offset for value in values]
    assert statistics.median(shifted) == result + offset

    # Multiplying every value scales the median, including for negative scales.
    scale = data.draw(st.integers(min_value=-10, max_value=10))
    scaled = [value * scale for value in values]
    assert statistics.median(scaled) == result * scale
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_median_property))
