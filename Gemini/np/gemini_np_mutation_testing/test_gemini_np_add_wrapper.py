import numpy as np
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# --- Input Generation Strategy ---
# This composite strategy generates pairs of arrays (x1, x2) that are 
# guaranteed to be broadcast-compatible with each other.
@st.composite
def broadcastable_pairs(draw, dtype=np.int32):
    # 1. Generate a master target shape that both arrays will broadcast into
    target_shape = draw(array_shapes(min_dims=0, max_dims=4, min_side=0, max_side=5))
    
    def transform_to_broadcastable(shape):
        # NumPy broadcasting rules allow a dimension to be 1 or omitted
        mutated = list(shape)
        for i in range(len(mutated)):
            if draw(st.booleans()):
                mutated[i] = 1
        # Randomly drop dimensions from the left to vary the number of dimensions
        drop_count = draw(st.integers(0, len(mutated)))
        return tuple(mutated[drop_count:])
    
    shape1 = transform_to_broadcastable(target_shape)
    shape2 = transform_to_broadcastable(target_shape)
    
    # 2. Generate arrays with bounded integer elements to prevent overflow bounds violations
    x1 = draw(arrays(dtype, shape1, elements=st.integers(-10000, 10000)))
    x2 = draw(arrays(dtype, shape2, elements=st.integers(-10000, 10000)))
    
    return x1, x2


# --- Property-Based Test Suite ---

@given(broadcastable_pairs())
def test_numpy_add_commutativity(pairs):
    """Property 1: Addition is commutative (x1 + x2 == x2 + x1)"""
    x1, x2 = pairs
    res1 = np.add(x1, x2)
    res2 = np.add(x2, x1)
    np.testing.assert_array_equal(res1, res2)


@given(broadcastable_pairs())
def test_numpy_add_identity(pairs):
    """Property 2: Zero is the additive identity (x1 + 0 == x1)"""
    x1, _ = pairs
    res = np.add(x1, 0)
    np.testing.assert_array_equal(res, x1)


@given(broadcastable_pairs())
def test_numpy_add_operator_equivalence(pairs):
    """Property 3: np.add(x1, x2) is strictly equivalent to the + operator shorthand"""
    x1, x2 = pairs
    res_ufunc = np.add(x1, x2)
    res_operator = x1 + x2
    np.testing.assert_array_equal(res_ufunc, res_operator)


@given(broadcastable_pairs())
def test_numpy_add_output_shape(pairs):
    """Property 4: The output shape strictly matches the expected broadcast shape"""
    x1, x2 = pairs
    expected_shape = np.broadcast_shapes(x1.shape, x2.shape)
    res = np.add(x1, x2)
    assert res.shape == expected_shape


@given(st.data(), broadcastable_pairs())
def test_numpy_add_where_condition(data, pairs):
    """
    Property 5: The 'where' parameter correctly masks operations.
    Where True, output updates to sum. Where False, output retains original 'out' values.
    """
    x1, x2 = pairs
    out_shape = np.broadcast_shapes(x1.shape, x2.shape)
    
    # Generate a boolean mask matching the broadcasted output shape
    where_mask = data.draw(arrays(np.bool_, out_shape))
    
    # Initialize 'out' array with a distinct sentinel value (e.g., -99999)
    out_array = np.full(out_shape, -99999, dtype=np.int32)
    
    # Execute addition with condition mask
    np.add(x1, x2, out=out_array, where=where_mask)
    
    # Direct element-wise addition for verification
    standard_sum = x1 + x2
    
    # Verify elements where mask is True match the calculated sum
    np.testing.assert_array_equal(out_array[where_mask], standard_sum[where_mask])
    
    # Verify elements where mask is False remained completely unmodified
    np.testing.assert_array_equal(out_array[~where_mask], -99999)

# End program
        
