from hypothesis import given, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Summary: Generate finite bounded scalar endpoints, small non-negative sample
# counts, endpoint flags, and retstep flags, including edge cases such as equal
# endpoints and zero or one requested samples while avoiding overflow.
@given(st.data())
def test_linspace(data):
    # Keep inputs in a moderate finite range so arithmetic in the properties
    # cannot overflow and Hypothesis can still explore integers and floats.
    finite_numbers = st.one_of(
        st.integers(min_value=-1000000, max_value=1000000),
        st.floats(
            min_value=-1000000,
            max_value=1000000,
            allow_nan=False,
            allow_infinity=False,
            width=64,
        ),
    )

    # Draw all public inputs covered by this scalar test.  NumPy also supports
    # array-like start/stop and dtype/axis parameters, but this test focuses on
    # the core one-dimensional scalar behavior documented for linspace.
    start = data.draw(finite_numbers)
    stop = data.draw(finite_numbers)
    num = data.draw(st.integers(min_value=0, max_value=200))
    endpoint = data.draw(st.booleans())
    retstep = data.draw(st.booleans())

    # retstep changes the return shape from just the generated array to a
    # pair of (generated array, spacing), so normalize both forms here.
    output = np.linspace(start, stop, num=num, endpoint=endpoint, retstep=retstep)
    if retstep:
        result, step = output
    else:
        result = output
        step = np.nan if num <= 1 else (stop - start) / (num - 1 if endpoint else num)

    # The output must contain exactly the requested number of samples.
    assert result.shape == (num,)

    # With zero requested samples, linspace returns an empty array and there
    # are no endpoint or spacing properties left to check.
    if num == 0:
        assert result.size == 0
        return

    # For non-empty outputs, the first generated value should always be start.
    assert np.isclose(result[0], start, rtol=1e-10, atol=1e-10)

    # When endpoint=True and at least two samples are requested, the final
    # value should land on stop.
    if endpoint and num > 1:
        assert np.isclose(result[-1], stop, rtol=1e-10, atol=1e-10)

    # For sequences with at least two points, every adjacent gap should match
    # the documented spacing formula.  Tolerances account for floating-point
    # rounding in NumPy's internal calculations.
    if num > 1:
        expected_step = (stop - start) / (num - 1 if endpoint else num)
        assert np.isclose(step, expected_step, rtol=1e-10, atol=1e-10)
        assert np.allclose(np.diff(result), expected_step, rtol=1e-9, atol=1e-9)

        # The sequence should move monotonically from start toward stop.
        if stop >= start:
            assert np.all(np.diff(result) >= -1e-9)
        else:
            assert np.all(np.diff(result) <= 1e-9)
# End program



# ACCESS Validity/Soundness 
print(evaluate_test(test_linspace))

