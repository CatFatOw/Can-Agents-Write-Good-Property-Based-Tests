import importlib.util
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given, strategies as st
from hypothesis.extra import numpy as hnp


def _load_norm():
    try:
        from numpy.linalg import norm as runtime_norm
        return runtime_norm
    except Exception:
        here = Path(__file__).resolve()
        src = here.parent / "source_code" / "numpy" / "linalg" / "_linalg.py"
        spec = importlib.util.spec_from_file_location("tested_numpy_linalg__linalg", src)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        return module.norm


norm = _load_norm()


finite_float = st.floats(
    min_value=-10,
    max_value=10,
    allow_nan=False,
    allow_infinity=False,
    width=64,
)
finite_complex = st.complex_numbers(
    min_magnitude=0,
    max_magnitude=10,
    allow_nan=False,
    allow_infinity=False,
)


@st.composite
def arrays_any_nd(draw):
    ndim = draw(st.integers(min_value=0, max_value=4))
    shape = tuple(draw(st.integers(min_value=0, max_value=3)) for _ in range(ndim))
    dtype = draw(st.sampled_from([np.float64, np.complex128]))
    elements = finite_complex if np.issubdtype(dtype, np.complexfloating) else finite_float
    return draw(hnp.arrays(dtype=dtype, shape=shape, elements=elements))


@st.composite
def vector_arrays_and_axis(draw):
    ndim = draw(st.integers(min_value=1, max_value=4))
    shape = tuple(draw(st.integers(min_value=0, max_value=4)) for _ in range(ndim))
    dtype = draw(st.sampled_from([np.float64, np.complex128, np.int64]))
    elements = (
        finite_complex
        if np.issubdtype(dtype, np.complexfloating)
        else st.integers(-5, 5) if np.issubdtype(dtype, np.integer)
        else finite_float
    )
    arr = draw(hnp.arrays(dtype=dtype, shape=shape, elements=elements))
    axis = draw(st.integers(min_value=-ndim, max_value=ndim - 1))
    keepdims = draw(st.booleans())
    return arr, axis, keepdims


@st.composite
def matrix_arrays_axes_keepdims(draw):
    ndim = draw(st.integers(min_value=2, max_value=4))
    shape = tuple(draw(st.integers(min_value=0, max_value=3)) for _ in range(ndim))
    dtype = draw(st.sampled_from([np.float64, np.complex128]))
    elements = finite_complex if np.issubdtype(dtype, np.complexfloating) else finite_float
    arr = draw(hnp.arrays(dtype=dtype, shape=shape, elements=elements))

    ax1 = draw(st.integers(min_value=-ndim, max_value=ndim - 1))
    ax1_norm = ax1 % ndim
    possible_ax2 = [a for a in range(-ndim, ndim) if (a % ndim) != ax1_norm]
    ax2 = draw(st.sampled_from(possible_ax2))
    keepdims = draw(st.booleans())
    return arr, (ax1, ax2), keepdims


@st.composite
def matrix_arrays_and_axes(draw):
    ndim = draw(st.integers(min_value=2, max_value=4))
    shape = tuple(draw(st.integers(min_value=0, max_value=3)) for _ in range(ndim))
    dtype = draw(st.sampled_from([np.float64, np.complex128]))
    elements = finite_complex if np.issubdtype(dtype, np.complexfloating) else finite_float
    arr = draw(hnp.arrays(dtype=dtype, shape=shape, elements=elements))

    ax1 = draw(st.integers(min_value=-ndim, max_value=ndim - 1))
    ax1_norm = ax1 % ndim
    possible_ax2 = [a for a in range(-ndim, ndim) if (a % ndim) != ax1_norm]
    ax2 = draw(st.sampled_from(possible_ax2))
    return arr, (ax1, ax2)


# Property 1:
# With axis=None, ord=None always computes the Euclidean norm of x.ravel(order='K');
# keepdims=True reshapes to ndim * [1].
@given(arrays_any_nd(), st.booleans())
def test_norm_axis_none_default_is_flattened_euclidean(arr, keepdims):
    result = norm(arr, axis=None, ord=None, keepdims=keepdims)

    flat = np.ravel(np.asarray(arr), order="K")
    if np.issubdtype(flat.dtype, np.complexfloating):
        sqnorm = flat.real.dot(flat.real) + flat.imag.dot(flat.imag)
    else:
        work = flat.astype(float, copy=False) if not np.issubdtype(flat.dtype, np.inexact) else flat
        sqnorm = work.dot(work)
    expected = np.sqrt(sqnorm)

    if keepdims:
        expected = np.asarray(expected).reshape((1,) * np.asarray(arr).ndim)

    np.testing.assert_allclose(result, expected, rtol=1e-12, atol=1e-12)


# Property 2:
# For vector norms, ord=0 counts nonzero entries along the axis, with numeric dtype.
@given(vector_arrays_and_axis())
def test_norm_vector_ord_zero_counts_nonzero(data):
    arr, axis, keepdims = data
    result = norm(arr, ord=0, axis=axis, keepdims=keepdims)

    x = np.asarray(arr)
    expected = (x != 0).astype(x.real.dtype).sum(axis=axis, keepdims=keepdims)

    assert np.issubdtype(np.asarray(result).dtype, np.number)
    np.testing.assert_array_equal(result, expected)


# Property 3:
# String orders are mode-dependent: vector mode rejects string orders; matrix mode
# accepts 'fro', 'f', and 'nuc', and 'f' matches 'fro'.
@given(vector_arrays_and_axis())
def test_norm_string_orders_split_by_vector_vs_matrix_mode(data):
    arr, axis, _ = data

    with pytest.raises(ValueError):
        norm(arr, ord="fro", axis=axis)

    with pytest.raises(ValueError):
        norm(arr, ord="nuc", axis=axis)

    # Matrix-mode acceptance and alias behavior on a fixed small matrix.
    m = np.array([[1.0, -2.0], [3.5, 4.0]])
    np.testing.assert_allclose(norm(m, ord="f", axis=(0, 1)), norm(m, ord="fro", axis=(0, 1)))
    np.testing.assert_allclose(
        norm(m, ord="nuc", axis=(0, 1)),
        np.sum(np.linalg.svd(np.moveaxis(m, (0, 1), (-2, -1)), compute_uv=False), axis=-1),
        rtol=1e-12,
        atol=1e-12,
    )


# Property 4:
# For matrix norms, duplicate axes are rejected; keepdims=True keeps exactly those axes as size 1.
@given(matrix_arrays_axes_keepdims())
def test_norm_matrix_axes_duplicate_rejected_and_keepdims_shape(data):
    arr, axis, keepdims = data
    x = np.asarray(arr)

    dup_axis = (axis[0], axis[0])
    with pytest.raises(ValueError):
        norm(x, ord="fro", axis=dup_axis)

    result = norm(x, ord="fro", axis=axis, keepdims=keepdims)
    if keepdims:
        expected_shape = list(x.shape)
        expected_shape[axis[0]] = 1
        expected_shape[axis[1]] = 1
        assert result.shape == tuple(expected_shape)
    else:
        normalized = tuple(a % x.ndim for a in axis)
        expected_shape = tuple(s for i, s in enumerate(x.shape) if i not in normalized)
        assert result.shape == expected_shape


# Property 5:
# For matrix norms with ord in {2, -2, 'nuc'}, result is based on singular values
# of the matrices identified by the chosen axes.
@given(matrix_arrays_and_axes())
def test_norm_matrix_svd_based_orders_match_singular_value_oracle(data):
    arr, axis = data
    x = np.asarray(arr)
    row_axis = axis[0] % x.ndim
    col_axis = axis[1] % x.ndim

    moved = np.moveaxis(x, (row_axis, col_axis), (-2, -1))
    s = np.linalg.svd(moved, compute_uv=False)

    expected_2 = np.max(s, axis=-1)
    expected_neg2 = np.min(s, axis=-1)
    expected_nuc = np.sum(s, axis=-1)

    np.testing.assert_allclose(norm(x, ord=2, axis=axis), expected_2, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(norm(x, ord=-2, axis=axis), expected_neg2, rtol=1e-10, atol=1e-10)
    np.testing.assert_allclose(norm(x, ord="nuc", axis=axis), expected_nuc, rtol=1e-10, atol=1e-10)
