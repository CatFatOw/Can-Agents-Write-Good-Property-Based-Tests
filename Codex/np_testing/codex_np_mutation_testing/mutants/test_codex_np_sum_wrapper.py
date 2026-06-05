from hypothesis import given, settings, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



def _size(shape):
    return int(np.prod(shape, dtype=int)) if shape else 1


def _array_for_shape(data, shape, dtype):
    if np.issubdtype(dtype, np.integer):
        elements = st.integers(min_value=-100, max_value=100)
    else:
        elements = st.floats(
            min_value=-100,
            max_value=100,
            allow_nan=False,
            allow_infinity=False,
            width=32,
        )

    values = data.draw(st.lists(elements, min_size=_size(shape), max_size=_size(shape)))
    return np.array(values, dtype=dtype).reshape(shape)


def _normalize_axes(axis, ndim):
    if axis is None:
        return tuple(range(ndim))
    if isinstance(axis, tuple):
        return tuple(sorted(ax % ndim for ax in axis))
    return (axis % ndim,)


def _expected_shape(shape, axes, keepdims):
    if keepdims:
        return tuple(1 if dim in axes else extent for dim, extent in enumerate(shape))
    return tuple(extent for dim, extent in enumerate(shape) if dim not in axes)


def _source_index(output_index, reduced_values, shape, axes, keepdims):
    output_index = list(output_index)
    reduced_values = list(reduced_values)
    result = []
    output_pos = 0
    reduced_pos = 0

    for dim in range(len(shape)):
        if dim in axes:
            result.append(reduced_values[reduced_pos])
            reduced_pos += 1
            if keepdims:
                output_pos += 1
        else:
            result.append(output_index[output_pos])
            output_pos += 1

    return tuple(result)


def _manual_sum(arr, axis=None, dtype=None, keepdims=False, initial=0, where=True):
    axes = _normalize_axes(axis, arr.ndim)
    result_shape = _expected_shape(arr.shape, axes, keepdims)
    accumulator_dtype = np.dtype(dtype) if dtype is not None else arr.dtype
    result = np.empty(result_shape, dtype=accumulator_dtype)
    mask = np.broadcast_to(where, arr.shape)
    reduced_shape = tuple(arr.shape[dim] for dim in axes)

    for output_index in np.ndindex(result_shape):
        total = accumulator_dtype.type(initial)
        for reduced_values in np.ndindex(reduced_shape):
            source_index = _source_index(output_index, reduced_values, arr.shape, axes, keepdims)
            if mask[source_index]:
                total = total + arr[source_index].astype(accumulator_dtype, copy=False)
        result[output_index] = total

    if result_shape == ():
        return result[()]
    return result


# Summary: Generate small bounded integer and finite floating arrays, valid
# single-axis, tuple-axis, and all-axis reductions, optional accumulator dtypes,
# keepdims flags, initial values, where masks, and matching out arrays. Bounds
# keep integer overflow and floating-point instability out of the tested space.
@settings(max_examples=100)
@given(st.data())
def test_sum(data):
    rank = data.draw(st.integers(min_value=1, max_value=3))
    shape = data.draw(st.tuples(*[st.integers(min_value=0, max_value=4) for _ in range(rank)]))
    input_dtype = data.draw(st.sampled_from((np.int64, np.float64)))
    dtype = data.draw(st.sampled_from((None, np.int64, np.float64)))
    keepdims = data.draw(st.booleans())
    initial = data.draw(st.integers(min_value=-20, max_value=20))

    axis_case = data.draw(st.sampled_from(("none", "int", "tuple")))
    if axis_case == "none":
        axis = None
    elif axis_case == "int":
        axis = data.draw(st.integers(min_value=-rank, max_value=rank - 1))
    else:
        axes = data.draw(
            st.lists(
                st.integers(min_value=0, max_value=rank - 1),
                min_size=1,
                max_size=rank,
                unique=True,
            )
        )
        axis = tuple(axes)

    arr = _array_for_shape(data, shape, input_dtype)
    where = data.draw(
        st.lists(st.booleans(), min_size=_size(shape), max_size=_size(shape))
    )
    where = np.array(where, dtype=bool).reshape(shape)

    result = np.sum(arr, axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)
    expected = _manual_sum(arr, axis=axis, dtype=dtype, keepdims=keepdims, initial=initial, where=where)

    # The returned shape follows axis removal, or leaves reduced dimensions as
    # size one when keepdims=True.
    assert np.shape(result) == np.shape(expected)

    # The value is the sum of exactly the selected elements plus the initial
    # value once per reduced output cell.
    assert np.allclose(result, expected, rtol=1e-10, atol=1e-10)

    # A dtype argument controls the accumulator and returned dtype.
    if dtype is not None:
        assert np.asarray(result).dtype == np.dtype(dtype)

    # With no selected elements and the default initial, sum returns the
    # additive identity for every reduced output cell.
    empty_mask_result = np.sum(arr, axis=axis, dtype=dtype, keepdims=keepdims, initial=0, where=False)
    assert np.allclose(empty_mask_result, np.zeros_like(empty_mask_result), rtol=0, atol=0)

    # If out is supplied, NumPy writes into it and returns that same object.
    out = np.empty(np.shape(result), dtype=np.asarray(result).dtype)
    out_result = np.sum(
        arr,
        axis=axis,
        dtype=dtype,
        out=out,
        keepdims=keepdims,
        initial=initial,
        where=where,
    )
    assert out_result is out
    assert np.allclose(out, expected, rtol=1e-10, atol=1e-10)
# End program



