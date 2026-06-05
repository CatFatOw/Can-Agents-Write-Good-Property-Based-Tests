from hypothesis import given, settings, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))




def _size(shape):
    return int(np.prod(shape, dtype=int))


def _array_for_shape(data, shape, dtype):
    if np.issubdtype(dtype, np.integer):
        elements = st.integers(min_value=-1000, max_value=1000)
    else:
        elements = st.floats(
            min_value=-1000,
            max_value=1000,
            allow_nan=False,
            allow_infinity=False,
            width=32,
        )

    values = data.draw(st.lists(elements, min_size=_size(shape), max_size=_size(shape)))
    return np.array(values, dtype=dtype).reshape(shape)


def _prefix_differences_match_input(result, original, axis):
    if axis is None:
        result_view = result
        original_view = original.ravel()
        axis = 0
    else:
        result_view = result
        original_view = original

    first_index = [slice(None)] * result_view.ndim
    first_index[axis] = 0
    assert np.allclose(
        result_view[tuple(first_index)],
        original_view[tuple(first_index)],
        rtol=1e-12,
        atol=1e-12,
    )

    if result_view.shape[axis] > 1:
        diffs = np.diff(result_view, axis=axis)
        trailing_index = [slice(None)] * original_view.ndim
        trailing_index[axis] = slice(1, None)
        assert np.allclose(
            diffs,
            original_view[tuple(trailing_index)],
            rtol=1e-12,
            atol=1e-12,
        )


# Summary: Generate small one-, two-, and three-dimensional integer or finite
# floating arrays, valid axes including None, optional accumulator dtypes, and
# matching out arrays.  Values and shapes are bounded to avoid overflow and
# floating-point accumulation instability while still covering flattening,
# axis-specific, dtype, and out behavior.
@settings(max_examples=100)
@given(st.data())
def test_cumsum(data):
    rank = data.draw(st.integers(min_value=1, max_value=3))
    shape = data.draw(st.tuples(*[st.integers(min_value=1, max_value=5) for _ in range(rank)]))
    input_dtype = data.draw(st.sampled_from((np.int64, np.float64)))
    dtype = data.draw(st.sampled_from((None, np.int64, np.float64)))
    axis = data.draw(st.sampled_from((None, *range(-rank, rank))))

    arr = _array_for_shape(data, shape, input_dtype)
    result = np.cumsum(arr, axis=axis, dtype=dtype)

    # With axis=None, NumPy computes over the flattened input; otherwise the
    # original shape is preserved.
    expected_shape = (arr.size,) if axis is None else arr.shape
    assert result.shape == expected_shape
    assert result.size == arr.size

    # The accumulator dtype controls the returned dtype when provided.
    if dtype is not None:
        assert result.dtype == np.dtype(dtype)
    else:
        assert result.dtype == arr.dtype

    # cumsum is the same prefix operation as add.accumulate on the selected
    # axis, including flattened behavior when axis is None.
    expected_input = arr.ravel() if axis is None else arr
    expected_axis = 0 if axis is None else axis
    expected = np.add.accumulate(expected_input, axis=expected_axis, dtype=dtype)
    assert np.allclose(result, expected, rtol=1e-12, atol=1e-12)

    # Each adjacent prefix difference recovers the original input element.
    _prefix_differences_match_input(result, arr.astype(result.dtype, copy=False), axis)

    # The final prefix value along the accumulation axis equals the ordinary
    # sum for these bounded exact/small inputs.
    final_index = [slice(None)] * result.ndim
    final_axis = 0 if axis is None else axis
    final_index[final_axis] = -1
    expected_sum = np.sum(expected_input, axis=expected_axis, dtype=dtype)
    assert np.allclose(result[tuple(final_index)], expected_sum, rtol=1e-10, atol=1e-10)

    # If out is supplied, NumPy writes into it and returns that same object.
    out = np.empty(expected_shape, dtype=result.dtype)
    out_result = np.cumsum(arr, axis=axis, dtype=dtype, out=out)
    assert out_result is out
    assert np.allclose(out, result, rtol=1e-12, atol=1e-12)
# End program



