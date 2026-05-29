from hypothesis import given, settings, strategies as st
import math
import pytest
import statistics
from statistics import StatisticsError
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


positive_number = st.one_of(
    st.integers(min_value=1, max_value=1_000_000),
    st.floats(
        min_value=1e-6,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
        width=64,
    ),
)

non_positive_number = st.one_of(
    st.integers(min_value=-1_000_000, max_value=0),
    st.floats(
        min_value=-1_000_000,
        max_value=0,
        allow_nan=False,
        allow_infinity=False,
        width=64,
    ),
)


# Summary: Draw bounded finite positive sequences for the algebraic properties
# of geometric_mean, avoiding huge products by comparing against the logarithmic
# definition. Also draw invalid empty/non-positive sequences to check errors.
@settings(max_examples=25)
@given(st.data())
def test_geometric_mean_property(data):
    invalid_values = data.draw(
        st.one_of(
            st.just([]),
            st.lists(
                st.one_of(positive_number, non_positive_number),
                min_size=1,
                max_size=25,
            ).filter(lambda values: any(value <= 0 for value in values)),
        )
    )
    with pytest.raises(StatisticsError):
        statistics.geometric_mean(invalid_values)

    values = data.draw(st.lists(positive_number, min_size=1, max_size=50))
    result = statistics.geometric_mean(values)

    expected = math.exp(math.fsum(math.log(value) for value in values) / len(values))
    assert result == pytest.approx(expected, rel=1e-12, abs=1e-12)

    # The geometric mean of positive inputs lies between their min and max,
    # allowing tiny floating-point rounding at the boundary.
    lower = min(values)
    upper = max(values)
    lower_tolerance = max(1e-12, abs(lower) * 1e-12)
    upper_tolerance = max(1e-12, abs(upper) * 1e-12)
    assert result >= lower - lower_tolerance
    assert result <= upper + upper_tolerance

    # A singleton sequence's geometric mean is its value after float coercion.
    if len(values) == 1:
        assert result == pytest.approx(float(values[0]), rel=1e-12, abs=1e-12)

    # Repeating the same data does not change the geometric mean.
    repeat_count = data.draw(st.integers(min_value=1, max_value=5))
    assert statistics.geometric_mean(values * repeat_count) == pytest.approx(
        result,
        rel=1e-12,
        abs=1e-12,
    )

    # Multiplying all inputs by a positive constant scales the mean equally.
    scale = data.draw(positive_number)
    scaled_values = [scale * value for value in values]
    assert statistics.geometric_mean(scaled_values) == pytest.approx(
        scale * result,
        rel=1e-12,
        abs=1e-12,
    )
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_geometric_mean_property))
