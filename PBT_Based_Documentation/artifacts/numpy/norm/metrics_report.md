# Metrics Report

## Scores

- Validity: 1.00
- Soundness: 0.80
- Mutation usefulness: None
- Confidence: 0.860
- Documentation gate: pass
- Note: Mutation testing was skipped.

## Pytest

- Command: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3 -m pytest -q /Users/michaelwu/cmu-research_PBT/PBT_Based_Documentation/artifacts/numpy/norm/generated_tests.py`
- Available: True
- Return code: 1

```text
....F                                                                    [100%]
=================================== FAILURES ===================================
________ test_norm_matrix_svd_based_orders_match_singular_value_oracle _________

    @given(matrix_arrays_and_axes())
>   def test_norm_matrix_svd_based_orders_match_singular_value_oracle(data):
                   ^^^

artifacts/numpy/norm/generated_tests.py:185: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
artifacts/numpy/norm/generated_tests.py:194: in test_norm_matrix_svd_based_orders_match_singular_value_oracle
    expected_2 = np.max(s, axis=-1)
                 ^^^^^^^^^^^^^^^^^^
/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/numpy/_core/fromnumeric.py:3164: in max
    return _wrapreduction(a, np.maximum, 'max', axis, None, out,
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

obj = array([], dtype=float64), ufunc = <ufunc 'maximum'>, method = 'max'
axis = -1, dtype = None, out = None
kwargs = {'initial': <no value>, 'keepdims': <no value>, 'where': <no value>}
passkwargs = {}

    def _wrapreduction(obj, ufunc, method, axis, dtype, out, **kwargs):
        passkwargs = {k: v for k, v in kwargs.items()
                      if v is not np._NoValue}
    
        if type(obj) is not mu.ndarray:
            try:
                reduction = getattr(obj, method)
            except AttributeError:
                pass
            else:
                # This branch is needed for reductions like any which don't
                # support a dtype.
                if dtype is not None:
                    return reduction(axis=axis, dtype=dtype, out=out, **passkwargs)
                else:
                    return reduction(axis=axis, out=out, **passkwargs)
    
>       return ufunc.reduce(obj, axis, dtype, out, **passkwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       ValueError: zero-size array to reduction operation maximum which has no identity
E       Falsifying example: test_norm_matrix_svd_based_orders_match_singular_value_oracle(
E           data=(array([], shape=(0, 0), dtype=float64), (0, -1)),
E       )

/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/numpy/_core/fromnumeric.py:86: ValueError
================================== Hypothesis ==================================
`git apply .hypothesis/patches/2026-06-05--cad51a30.patch` to add failing examples to your code.
=========================== short test summary info ============================
FAILED artifacts/numpy/norm/generated_tests.py::test_norm_matrix_svd_based_orders_match_singular_value_oracle
1 failed, 4 passed in 1.80s

```
