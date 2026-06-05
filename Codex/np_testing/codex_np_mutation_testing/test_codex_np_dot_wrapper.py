from hypothesis import given, settings, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))




def _size(shape):
    return int(np.prod(shape, dtype=int)) if shape else 1


def _array_for_shape(data, shape):
    elements = st.floats(
        min_value=-1000,
        max_value=1000,
        allow_nan=False,
        allow_infinity=False,
        width=32,
    )

    if shape == ():
        return data.draw(elements)

    values = data.draw(st.lists(elements, min_size=_size(shape), max_size=_size(shape)))
    return np.array(values, dtype=np.float64).reshape(shape)


def _small_shape(data, rank):
    if rank == 0:
        return ()
    return data.draw(st.tuples(*[st.integers(min_value=1, max_value=4) for _ in range(rank)]))


def _expected_dot(a, b):
    a_shape = np.shape(a)
    b_shape = np.shape(b)

    if a_shape == () or b_shape == ():
        return np.multiply(a, b)
    if len(a_shape) == 1 and len(b_shape) == 1:
        return np.sum(np.asarray(a) * np.asarray(b))
    if len(b_shape) == 1:
        return np.tensordot(a, b, axes=([-1], [0]))
    return np.tensordot(a, b, axes=([-1], [-2]))


# Summary: Generate bounded finite scalars and small arrays with compatible dot
# dimensions, covering scalar multiplication, vector inner products, matrix
# multiplication, N-D by 1-D sum-products, and N-D by M-D sum-products while
# keeping values and sizes small enough to avoid overflow.
@settings(max_examples=100)
@given(st.data())
def test_dot(data):
    case = data.draw(st.sampled_from(("scalar", "vector", "matrix", "nd_vector", "nd_md")))
    shared = data.draw(st.integers(min_value=1, max_value=4))

    if case == "scalar":
        a = _array_for_shape(data, ())
        b_rank = data.draw(st.integers(min_value=0, max_value=3))
        b = _array_for_shape(data, _small_shape(data, b_rank))
    elif case == "vector":
        a = _array_for_shape(data, (shared,))
        b = _array_for_shape(data, (shared,))
    elif case == "matrix":
        rows = data.draw(st.integers(min_value=1, max_value=4))
        cols = data.draw(st.integers(min_value=1, max_value=4))
        a = _array_for_shape(data, (rows, shared))
        b = _array_for_shape(data, (shared, cols))
    elif case == "nd_vector":
        prefix_rank = data.draw(st.integers(min_value=1, max_value=3))
        prefix = _small_shape(data, prefix_rank)
        a = _array_for_shape(data, prefix + (shared,))
        b = _array_for_shape(data, (shared,))
    else:
        a_prefix_rank = data.draw(st.integers(min_value=1, max_value=3))
        b_prefix_rank = data.draw(st.integers(min_value=0, max_value=2))
        a_prefix = _small_shape(data, a_prefix_rank)
        b_prefix = _small_shape(data, b_prefix_rank)
        trailing = data.draw(st.integers(min_value=1, max_value=4))
        a = _array_for_shape(data, a_prefix + (shared,))
        b = _array_for_shape(data, b_prefix + (shared, trailing))

    result = np.dot(a, b)
    expected = _expected_dot(a, b)

    # The returned shape follows the documented scalar, vector, and general
    # sum-product cases.
    assert np.shape(result) == np.shape(expected)

    # The values match the independently computed sum product over the
    # documented contracted axes.
    assert np.allclose(result, expected, rtol=1e-10, atol=1e-10)

    # Scalars are equivalent to multiplication.
    if np.shape(a) == () or np.shape(b) == ():
        assert np.allclose(result, np.multiply(a, b), rtol=1e-10, atol=1e-10)

    # For 2-D arrays, dot agrees with matrix multiplication.
    if np.ndim(a) == 2 and np.ndim(b) == 2:
        assert np.allclose(result, a @ b, rtol=1e-10, atol=1e-10)

    # If out is supplied with the exact required shape, dtype, and contiguity,
    # NumPy writes into it and returns the same array object.
    if np.shape(result) != ():
        out = np.empty(np.shape(result), dtype=np.asarray(result).dtype, order="C")
        out_result = np.dot(a, b, out=out)
        assert out_result is out
        assert np.allclose(out, result, rtol=1e-10, atol=1e-10)
# End program


