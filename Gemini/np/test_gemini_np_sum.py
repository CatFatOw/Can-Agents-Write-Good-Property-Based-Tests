from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays, array_shapes
import numpy as np

import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Summary: Generates random multi-dimensional float64 arrays alongside valid axis configurations, keepdims choices, and initial scalar values to comprehensively verify shape manipulation and mathematical invariants.
@given(st.data())
def test_np_sum(data):
    # 1. Generate a valid array shape and populate it with float64 values
    shape = data.draw(array_shapes(min_dims=0, max_dims=4, min_side=0, max_side=4))
    a = data.draw(arrays(dtype=np.float64, shape=shape, elements=st.floats(min_value=-100.0, max_value=100.0)))
    ndim = a.ndim
    
    # 2. Dynamically build a valid axis argument based on array dimensionality
    if ndim == 0:
        axis = data.draw(st.none() | st.just(0) | st.just(-1))
    else:
        valid_axes = list(range(ndim))
        axis = data.draw(
            st.none() | 
            st.sampled_from(valid_axes) | 
            st.sets(st.sampled_from(valid_axes)).map(tuple)
        )
        
    keepdims = data.draw(st.booleans())
    
    # Execute the primary function execution under test
    res = np.sum(a, axis=axis, keepdims=keepdims)
    
    # PROPERTY 1: Verify output shape calculations match specification
    if keepdims:
        if axis is None:
            expected_shape = tuple(1 for _ in shape)
        else:
            axes_set = {axis} if isinstance(axis, int) else set(axis)
            expected_shape = tuple(1 if i in axes_set else s for i, s in enumerate(shape))
    else:
        if axis is None:
            expected_shape = ()
        else:
            axes_set = {axis} if isinstance(axis, int) else set(axis)
            expected_shape = tuple(s for i, s in enumerate(shape) if i not in axes_set)
            
    assert res.shape == expected_shape
    
    # PROPERTY 2: Verify explicit 'initial' parameter math invariant
    initial_val = data.draw(st.floats(min_value=-50.0, max_value=50.0))
    res_initial = np.sum(a, axis=axis, keepdims=keepdims, initial=initial_val)
    assert np.allclose(res_initial, res + initial_val, rtol=1e-5, atol=1e-5)
    
    # PROPERTY 3: Verify identity behavior on empty inputs
    if a.size == 0:
        res_empty = np.sum(a, axis=axis, keepdims=keepdims)
        assert np.all(res_empty == 0.0)

# End program
if __name__ == "__main__":
    print(evaluate_test(test_np_sum))