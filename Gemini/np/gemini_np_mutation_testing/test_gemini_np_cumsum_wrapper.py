from hypothesis import given, strategies as st
import numpy as np
from hypothesis.extra.numpy import arrays, array_shapes
import sys 
from pathlib import Path 
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from hypothesis import given, strategies as st
import numpy as np
from hypothesis.extra.numpy import arrays, array_shapes

# Summary: Generates arbitrary multi-dimensional NumPy arrays with varying shapes, dtypes, valid axis parameters, and target dtypes to comprehensively test edge cases like empty arrays and varying dimensions while handling float32 precision limits safely.
@given(st.data())
def test_numpy_cumsum(data):
    # 1. Generate an arbitrary valid shape for the array
    shape = data.draw(array_shapes(min_side=0, max_side=4, min_dims=1, max_dims=3))
    
    # 2. Pick a valid input data type
    input_dtype = data.draw(st.sampled_from([np.int32, np.int64, np.float32, np.float64]))
    
    # 3. Generate elements based on the data type
    if np.issubdtype(input_dtype, np.integer):
        elements = st.integers(min_value=-10000, max_value=10000)
    else:
        elements = st.floats(min_value=-1000.0, max_value=1000.0, allow_nan=False, allow_infinity=False)
        
    a = data.draw(arrays(dtype=input_dtype, shape=shape, elements=elements))
    
    # 4. Pick a valid axis parameter relative to the generated shape
    axis = data.draw(st.none() | st.integers(min_value=-len(shape), max_value=len(shape)-1))
    
    # 5. Pick an optional destination accumulator dtype
    dtype_opt = data.draw(st.none() | st.sampled_from([np.int64, np.float64]))
    
    # Execute the cumulative sum operation
    res = np.cumsum(a, axis=axis, dtype=dtype_opt)
    
    # Property 1: Size preservation
    assert res.size == a.size
    
    # Property 2: Shape preservation based on axis selection
    if axis is not None:
        assert res.shape == a.shape
    else:
        assert res.ndim == 1
        assert res.shape == (a.size,)
        
    # Property 3: Dtype correctness
    if dtype_opt is not None:
        assert res.dtype == np.dtype(dtype_opt)
        
    # Property 4: Mathematical correctness via inverse operation (differentiation)
    if a.size > 0:
        if axis is None:
            a_flat = a.flatten()
            if np.issubdtype(res.dtype, np.integer):
                assert res[0] == a_flat[0].astype(res.dtype)
                np.testing.assert_array_equal(np.diff(res), a_flat[1:].astype(res.dtype))
            else:
                # Dynamic tolerance adjusting for float32 precision limitations
                tol = 1e-3 if res.dtype == np.float32 else 1e-6
                np.testing.assert_allclose(res[0], a_flat[0], rtol=tol, atol=tol)
                np.testing.assert_allclose(np.diff(res), a_flat[1:], rtol=tol, atol=tol)
        else:
            # Check along a specific structural axis
            first_slice_res = np.take(res, 0, axis=axis)
            first_slice_a = np.take(a, 0, axis=axis)
            
            diff_res = np.diff(res, axis=axis)
            remaining_slices_a = np.take(a, range(1, a.shape[axis]), axis=axis)
            
            if np.issubdtype(res.dtype, np.integer):
                np.testing.assert_array_equal(first_slice_res, first_slice_a.astype(res.dtype))
                np.testing.assert_array_equal(diff_res, remaining_slices_a.astype(res.dtype))
            else:
                # Dynamic tolerance adjusting for float32 precision limitations
                tol = 1e-3 if res.dtype == np.float32 else 1e-6
                np.testing.assert_allclose(first_slice_res, first_slice_a, rtol=tol, atol=tol)
                np.testing.assert_allclose(diff_res, remaining_slices_a, rtol=tol, atol=tol)

