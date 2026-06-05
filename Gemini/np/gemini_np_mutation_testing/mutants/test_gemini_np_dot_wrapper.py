import numpy as np
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays

import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Summary: The strategy dynamically orchestrates four distinct dimensional scenarios (scalar, 1D, 2D, and N-D/M-D) using structured array generation with tightly paired matching axes and bounded integer values to guarantee mathematical correctness without overflow.
@given(st.data())
def test_numpy_dot(data):
    # Establish a shared dimension to maintain inner-product alignment constraints
    shared_dim = data.draw(st.integers(min_value=1, max_value=5))
    
    # Randomly select a configuration scenario from the API specification
    scenario = data.draw(st.sampled_from(["scalar", "1d_1d", "2d_2d", "nd_md"]))
    
    if scenario == "scalar":
        a = data.draw(st.integers(min_value=-50, max_value=50))
        shape_b = data.draw(st.lists(st.integers(min_value=1, max_value=4), min_size=1, max_size=3).map(tuple))
        b = data.draw(arrays(dtype=np.int32, shape=shape_b, elements=st.integers(min_value=-50, max_value=50)))
        
        res = np.dot(a, b)
        
        # Property: Equivalent to simple element-wise multiplication
        assert np.array_equal(res, a * b)
        assert res.shape == b.shape
        
    elif scenario == "1d_1d":
        a = data.draw(arrays(dtype=np.int32, shape=(shared_dim,), elements=st.integers(min_value=-50, max_value=50)))
        b = data.draw(arrays(dtype=np.int32, shape=(shared_dim,), elements=st.integers(min_value=-50, max_value=50)))
        
        res = np.dot(a, b)
        
        # Property: Output is a scalar matching the manual summation product
        assert np.isscalar(res) or res.shape == ()
        assert res == sum(a * b)
        
    elif scenario == "2d_2d":
        m = data.draw(st.integers(min_value=1, max_value=4))
        n = data.draw(st.integers(min_value=1, max_value=4))
        a = data.draw(arrays(dtype=np.int32, shape=(m, shared_dim), elements=st.integers(min_value=-50, max_value=50)))
        b = data.draw(arrays(dtype=np.int32, shape=(shared_dim, n), elements=st.integers(min_value=-50, max_value=50)))
        
        res = np.dot(a, b)
        
        # Property: Exact match with preferred matmul operator (@) and expected 2D shape
        assert np.array_equal(res, a @ b)
        assert res.shape == (m, n)
        
    elif scenario == "nd_md":
        # a is N-D array, b is M-D array (where M >= 2)
        shape_a_prefix = data.draw(st.lists(st.integers(min_value=1, max_value=3), min_size=1, max_size=2).map(tuple))
        shape_b_prefix = data.draw(st.lists(st.integers(min_value=1, max_value=3), min_size=1, max_size=2).map(tuple))
        shape_b_last = data.draw(st.integers(min_value=1, max_value=3))
        
        shape_a = shape_a_prefix + (shared_dim,)
        shape_b = shape_b_prefix + (shared_dim, shape_b_last)
        
        a = data.draw(arrays(dtype=np.int32, shape=shape_a, elements=st.integers(min_value=-10, max_value=10)))
        b = data.draw(arrays(dtype=np.int32, shape=shape_b, elements=st.integers(min_value=-10, max_value=10)))
        
        res = np.dot(a, b)
        
        # Property: Shape conforms precisely to sum product rule over specified axes
        expected_shape = shape_a[:-1] + shape_b[:-2] + (shape_b_last,)
        assert res.shape == expected_shape
        
        # Property: Linearity under scalar multiplication holds true
        res_scaled = np.dot(2 * a, b)
        assert np.array_equal(res_scaled, 2 * res)