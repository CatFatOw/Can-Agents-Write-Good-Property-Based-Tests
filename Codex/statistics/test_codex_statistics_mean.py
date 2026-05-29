from hypothesis import given, strategies as st
import math
import pytest
import statistics
from statistics import StatisticsError
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Summary: Generate empty, singleton, and multi-element sequences of bounded
# finite ints/floats so statistics.mean sees broad numeric inputs without NaN,
# infinity, or overflow-prone magnitudes.
@given(st.data())
def test_mean(data):
    finite_number = st.one_of(
        st.integers(min_value=-1000000, max_value=1000000),
        st.floats(
            min_value=-1000000,
            max_value=1000000,
            allow_nan=False,
            allow_infinity=False,
            width=64,
        ),
    )
    values = data.draw(st.lists(finite_number, min_size=0, max_size=100))

    if not values:
        with pytest.raises(StatisticsError):
            statistics.mean(values)
        return

    result = statistics.mean(values)

    # A non-empty sequence's mean is the arithmetic average.
    assert result == pytest.approx(math.fsum(values) / len(values), rel=1e-9, abs=1e-9)

    # The mean must lie between the smallest and largest input value.
    assert min(values) <= result <= max(values)

    # A singleton sequence's mean is exactly its only element.
    if len(values) == 1:
        assert result == values[0]

    # Adding a constant to every value shifts the mean by that constant.
    offset = data.draw(st.integers(min_value=-1000, max_value=1000))
    shifted = [value + offset for value in values]
    assert statistics.mean(shifted) == pytest.approx(result + offset, rel=1e-9, abs=1e-9)

    # Repeating the same data should not change its mean.
    repeat_count = data.draw(st.integers(min_value=1, max_value=5))
    repeated = values * repeat_count
    assert statistics.mean(repeated) == pytest.approx(result, rel=1e-9, abs=1e-9)
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_mean))
