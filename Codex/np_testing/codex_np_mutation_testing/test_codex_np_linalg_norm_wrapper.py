from hypothesis import given, settings, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))




def _size(shape):
    return int(np.prod(shape, dtype=int))


def _array_for_shape(data, shape):
    elements = st.floats(
        min_value=-100,
        max_value=100,
        allow_nan=False,
        allow_infinity=False,
        width=32,
    )
    values = data.draw(st.lists(elements, min_size=_size(shape), max_size=_size(shape)))
    return np.array(values, dtype=np.float64).reshape(shape)


def _shape(data, rank):
    return data.draw(st.tuples(*[st.integers(min_value=1, max_value=4) for _ in range(rank)]))


def _vector_norm_expected(x, ord, axis, keepdims):
    absolute = np.abs(x)

    if ord is None or ord == 2:
        result = np.sqrt(np.sum(absolute ** 2, axis=axis, keepdims=keepdims))
    elif ord == np.inf:
        result = np.max(absolute, axis=axis, keepdims=keepdims)
    elif ord == -np.inf:
        result = np.min(absolute, axis=axis, keepdims=keepdims)
    elif ord == 0:
        result = np.sum(x != 0, axis=axis, keepdims=keepdims)
    else:
        result = np.sum(absolute ** ord, axis=axis, keepdims=keepdims) ** (1.0 / ord)

    return result


def _matrix_norm_expected(x, ord, axis, keepdims):
    axis = tuple(ax % x.ndim for ax in axis)
    matrices = np.moveaxis(x, axis, (-2, -1))
    absolute = np.abs(matrices)

    if ord is None or ord == "fro":
        reduced = np.sqrt(np.sum(absolute ** 2, axis=(-2, -1)))
    elif ord == np.inf:
        reduced = np.max(np.sum(absolute, axis=-1), axis=-1)
    elif ord == -np.inf:
        reduced = np.min(np.sum(absolute, axis=-1), axis=-1)
    elif ord == 1:
        reduced = np.max(np.sum(absolute, axis=-2), axis=-1)
    elif ord == -1:
        reduced = np.min(np.sum(absolute, axis=-2), axis=-1)
    elif ord == "nuc":
        reduced = np.sum(np.linalg.svd(matrices, compute_uv=False), axis=-1)
    elif ord == 2:
        reduced = np.max(np.linalg.svd(matrices, compute_uv=False), axis=-1)
    else:
        reduced = np.min(np.linalg.svd(matrices, compute_uv=False), axis=-1)

    if not keepdims:
        return reduced

    result = reduced
    for ax in sorted(axis):
        result = np.expand_dims(result, axis=ax)
    return result


# Summary: Generate finite bounded one-, two-, and three-dimensional arrays,
# valid vector and matrix norm axes, supported ord values, and both keepdims
# settings while avoiding NaN, infinity, and large values that can overflow.
@settings(max_examples=100)
@given(st.data())
def test_linalg_norm(data):
    case = data.draw(st.sampled_from(("default", "vector_axis", "matrix_axis", "matrix_none")))
    keepdims = data.draw(st.booleans())

    if case == "default":
        rank = data.draw(st.integers(min_value=1, max_value=3))
        x = _array_for_shape(data, _shape(data, rank))
        result = np.linalg.norm(x, keepdims=keepdims)
        expected = np.sqrt(np.sum(np.ravel(x) ** 2))
        if keepdims:
            expected = np.full((1,) * x.ndim, expected)

    elif case == "vector_axis":
        rank = data.draw(st.integers(min_value=1, max_value=3))
        x = _array_for_shape(data, _shape(data, rank))
        axis = data.draw(st.integers(min_value=-rank, max_value=rank - 1))
        ord_value = data.draw(st.sampled_from((None, 0, 1, 2, 3, np.inf, -np.inf)))
        result = np.linalg.norm(x, ord=ord_value, axis=axis, keepdims=keepdims)
        expected = _vector_norm_expected(x, ord_value, axis, keepdims)

    elif case == "matrix_axis":
        rank = data.draw(st.integers(min_value=2, max_value=3))
        x = _array_for_shape(data, _shape(data, rank))
        axes = data.draw(st.sampled_from(tuple((i, j) for i in range(rank) for j in range(rank) if i != j)))
        ord_value = data.draw(st.sampled_from((None, "fro", "nuc", 1, -1, 2, -2, np.inf, -np.inf)))
        result = np.linalg.norm(x, ord=ord_value, axis=axes, keepdims=keepdims)
        expected = _matrix_norm_expected(x, ord_value, axes, keepdims)

    else:
        x = _array_for_shape(data, _shape(data, 2))
        ord_value = data.draw(st.sampled_from((None, "fro", "nuc", 1, -1, 2, -2, np.inf, -np.inf)))
        result = np.linalg.norm(x, ord=ord_value, keepdims=keepdims)
        expected = _matrix_norm_expected(x, ord_value, (0, 1), keepdims)

    # The norm output has the documented scalar or reduced-array shape,
    # including singleton dimensions when keepdims=True.
    assert np.shape(result) == np.shape(expected)

    # For generated bounded finite inputs, each supported norm agrees with the
    # direct formula from the documentation.
    assert np.allclose(result, expected, rtol=1e-9, atol=1e-9)

    # Norms are non-negative for all documented vector and matrix cases here.
    assert np.all(np.asarray(result) >= -1e-12)

    # keepdims=True leaves reduced axes as size-one dimensions that broadcast
    # against the original input.
    if keepdims:
        assert np.broadcast_shapes(np.shape(result), x.shape) == x.shape
# End program


