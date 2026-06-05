from hypothesis import given, strategies as st
import numpy as np
from numpy import linalg as LA

import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Summary: Generates 1-D and 2-D arrays safely using native Python primitives to prevent Hypothesis InvalidArgument errors.
@given(st.data())
def test_linalg_norm(data):
    # Determine dimension (1 or 2) to cleanly test both vector and matrix logic
    ndim = data.draw(st.integers(min_value=1, max_value=2))
    
    if ndim == 1:
        shape = (data.draw(st.integers(min_value=1, max_value=5)),)
        valid_ords = [None, 0, 1, 2, 3, float('inf'), float('-inf')]
    else:
        shape = (data.draw(st.integers(min_value=1, max_value=5)), data.draw(st.integers(min_value=1, max_value=5)))
        valid_ords = [None, 'fro', 'nuc', 1, -1, 2, -2, float('inf'), float('-inf')]
        
    # Generate the array elements safely to avoid overflows
    elements = st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    
    # FIX: Explicitly cast to a standard Python int to prevent Hypothesis InvalidArgument errors
    total_elements = int(np.prod(shape))
    flat_list = data.draw(st.lists(elements, min_size=total_elements, max_size=total_elements))
    x = np.array(flat_list).reshape(shape)
    
    ord_val = data.draw(st.sampled_from(valid_ords))
    keepdims = data.draw(st.booleans())
    
    # Execute the function
    res = LA.norm(x, ord=ord_val, axis=None, keepdims=keepdims)
    
    # Property 1: Non-negativity
    assert np.all(res >= 0.0)
    
    # Property 2: Shape Consistency
    if keepdims:
        assert res.ndim == x.ndim
        assert res.shape == tuple(1 for _ in shape)
    else:
        assert np.isscalar(res) or res.ndim == 0
        
    # Property 3: Default Equivalence
    if ord_val is None:
        if ndim == 1:
            equiv_res = LA.norm(x, ord=2, axis=None, keepdims=keepdims)
        else:
            equiv_res = LA.norm(x, ord='fro', axis=None, keepdims=keepdims)
        assert np.allclose(res, equiv_res, atol=1e-5, rtol=1e-5)
# End program
