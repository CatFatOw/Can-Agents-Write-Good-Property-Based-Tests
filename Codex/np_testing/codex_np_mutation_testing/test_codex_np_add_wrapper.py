from hypothesis import given, settings, strategies as st
import numpy as np
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))




def _size(shape):
    return int(np.prod(shape, dtype=int)) if shape else 1


def _broadcastable_shape_strategy(result_shape):
    if not result_shape:
        return st.just(())

    return st.tuples(
        *[
            st.sampled_from((1, dimension))
            if dimension != 1
            else st.just(1)
            for dimension in result_shape
        ]
    )


def _array_for_shape(data, shape):
    elements = st.floats(
        min_value=-1000000,
        max_value=1000000,
        allow_nan=False,
        allow_infinity=False,
        width=32,
    )

    if shape == ():
        return data.draw(elements)

    values = data.draw(st.lists(elements, min_size=_size(shape), max_size=_size(shape)))
    return np.array(values, dtype=np.float64).reshape(shape)


# Summary: Generate finite bounded numeric scalars and small arrays whose
# shapes are broadcast-compatible, including scalar, one-dimensional, and
# multi-dimensional cases while avoiding overflow-prone values.
@settings(max_examples=100)
@given(st.data())
def test_add(data):
    rank = data.draw(st.integers(min_value=0, max_value=3))
    result_shape = data.draw(
        st.tuples(*[st.integers(min_value=1, max_value=5) for _ in range(rank)])
        if rank
        else st.just(())
    )

    x1_shape = data.draw(_broadcastable_shape_strategy(result_shape))
    x2_shape = data.draw(_broadcastable_shape_strategy(result_shape))
    x1 = _array_for_shape(data, x1_shape)
    x2 = _array_for_shape(data, x2_shape)

    result = np.add(x1, x2)

    # The output shape is the common broadcast shape of the two inputs.
    assert np.shape(result) == np.broadcast_shapes(np.shape(x1), np.shape(x2))

    # np.add is equivalent to the + operator under NumPy broadcasting.
    assert np.allclose(result, x1 + x2, rtol=1e-12, atol=1e-12)

    # Element-wise addition is commutative for these finite numeric inputs.
    assert np.allclose(result, np.add(x2, x1), rtol=1e-12, atol=1e-12)

    # Adding zero leaves each input unchanged.
    assert np.allclose(np.add(x1, 0), x1, rtol=1e-12, atol=1e-12)
    assert np.allclose(np.add(0, x2), x2, rtol=1e-12, atol=1e-12)

    # With out and where, True positions receive the sum and False positions
    # keep the original out value.
    out = np.full(np.shape(result), 7.0)
    where = data.draw(
        st.lists(st.booleans(), min_size=_size(np.shape(result)), max_size=_size(np.shape(result)))
    )
    where = np.array(where, dtype=bool).reshape(np.shape(result))
    masked_result = np.add(x1, x2, out=out.copy(), where=where)
    expected = np.where(where, result, 7.0)
    assert np.allclose(masked_result, expected, rtol=1e-12, atol=1e-12)
# End program



