# dot

## Overview

`numpy.dot(a, b, out=None)` computes a dot product or sum-product between two inputs.

Its meaning depends on the dimensionality of `a` and `b`:

- **Two 1-D arrays**: returns the ordinary inner product of the vectors.
- **Two 2-D arrays**: returns matrix multiplication.
- **One or both 0-D inputs**: behaves like ordinary multiplication.
- **N-D array with 1-D array**: sums over the last axis of `a` and the only axis of `b`.
- **N-D array with M-D array (`M >= 2`)**: sums over the last axis of `a` and the second-to-last axis of `b`.

For 2-D matrix multiplication, `a @ b` or `numpy.matmul(a, b)` is generally preferred for readability.

## Parameters

### `a`
array_like  
First input.

### `b`
array_like  
Second input.

### `out`
ndarray, optional  
Optional output array in which to place the result.

If provided, `out` must be compatible with the result that `numpy.dot(a, b)` would otherwise produce. In particular, it must have the correct shape and dtype, and NumPy requires a suitable contiguous memory layout for this argument.

## Returns

ndarray or scalar

- Returns a **scalar** when:
  - both inputs are scalars, or
  - both inputs are 1-D arrays.
- Returns an **array** in the other supported cases.
- If `out` is provided and valid, the computed result is written there and that array is returned.

## Raises

### `ValueError`
Raised when the contraction dimensions do not match.

In particular:

- for 1-D inputs, the vector lengths must match;
- for N-D with 1-D, `a.shape[-1]` must equal `b.shape[0]`;
- for N-D with M-D (`M >= 2`), `a.shape[-1]` must equal `b.shape[-2]`.

Other exceptions may be raised for invalid input types or an incompatible `out` array.

## Semantic Guarantees

The following behaviors are part of the public contract of `numpy.dot`:

### 1. Scalar and vector cases return scalars
If both inputs are scalars, or both inputs are 1-D arrays, `dot` returns a scalar result rather than an array.

```python
import numpy as np

np.dot(3, 4)
# 12

np.dot([1, 2, 3], [4, 5, 6])
# 32
```

### 2. If either argument is 0-D, `dot` behaves like multiplication
When at least one argument is scalar-like (0-D), `dot(a, b)` is equivalent in meaning to `a * b`.

```python
import numpy as np

np.dot(10, np.array([1, 2, 3]))
# array([10, 20, 30])

np.dot(np.array(2.5), np.array([[1., 2.], [3., 4.]]))
# array([[ 2.5,  5. ],
#        [ 7.5, 10. ]])
```

### 3. For 1-D complex inputs, `dot` does not conjugate
For complex vectors, `dot` computes the ordinary inner product without conjugating the first argument.

```python
import numpy as np

a = np.array([1 + 2j, 3 + 4j])
b = np.array([5 + 6j, 7 + 8j])

np.dot(a, b)
# ordinary non-conjugating inner product
```

This differs from `numpy.vdot(a, b)`, which conjugates the first argument.

### 4. Higher-dimensional `dot` uses a specific axis contraction rule
For `a.ndim >= 1` and `b.ndim >= 2`, `dot` contracts:

- the **last axis of `a`**
with
- the **second-to-last axis of `b`**

So the result shape is:

```python
a.shape[:-1] + b.shape[:-2] + b.shape[-1:]
```

This is the defining higher-dimensional behavior of `dot`.

### 5. Mismatched contraction dimensions are an error
`dot` does not broadcast or flatten its inputs to resolve incompatible contraction axes. If the required dimensions do not match, it raises `ValueError`.

## Edge Cases

### Empty vectors
Empty 1-D arrays are valid as long as their lengths match.

```python
import numpy as np

np.dot(np.array([]), np.array([]))
# 0.0
```

The exact dtype of the result depends on the input dtypes.

### 0-D NumPy arrays
A 0-D NumPy array is treated like a scalar for `dot` semantics.

```python
import numpy as np

np.dot(np.array(3), np.array([1, 2]))
# array([3, 6])
```

### Complex vectors vs `vdot`
For real-valued inputs, `dot` and `vdot` often agree. For complex inputs, they may differ because `dot` does **not** conjugate the first argument.

```python
import numpy as np

x = np.array([2j, 3j])
np.dot(x, x)
# (-13+0j)

np.vdot(x, x)
# (13+0j)
```

### Shape rules for higher-dimensional input
For higher-dimensional arrays, only one axis from each operand participates in the contraction. This can produce shapes that differ from matrix multiplication intuition if either operand has more than 2 dimensions.

## Examples

### Scalar multiplication behavior
```python
import numpy as np

np.dot(3, 4)
# 12

np.dot(2, np.array([1, 2, 3]))
# array([2, 4, 6])
```

### Vector inner product
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.dot(a, b)
# 32
```

### Matrix multiplication
```python
import numpy as np

a = np.array([[1, 0],
              [0, 1]])
b = np.array([[4, 1],
              [2, 2]])

np.dot(a, b)
# array([[4, 1],
#        [2, 2]])
```

### N-D with 1-D
```python
import numpy as np

a = np.arange(12).reshape(3, 4)
b = np.array([1, 0, 0, 1])

np.dot(a, b)
# sums over the last axis of a and the only axis of b
```

### N-D with M-D (`M >= 2`)
```python
import numpy as np

a = np.arange(24).reshape(2, 3, 4)
b = np.arange(20).reshape(5, 4, 1)

result = np.dot(a, b)
result.shape
# (2, 3, 5, 1)
```

Here, `a.shape[-1] == 4` matches `b.shape[-2] == 4`, so the contraction is valid.

### Shape mismatch raises `ValueError`
```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([1, 2])

np.dot(a, b)
# ValueError
```

### Complex vectors are non-conjugating
```python
import numpy as np

a = np.array([1 + 1j, 2 + 0j])
b = np.array([1 + 0j, 3 + 0j])

np.dot(a, b)
# (7+1j)

np.vdot(a, b)
# (7-1j)
```

## Notes

- `dot` is a general-purpose operation whose meaning changes with input dimensionality.
- If you want explicit matrix multiplication semantics, prefer `@` or `numpy.matmul`.
- If you want conjugation of the first argument for complex vectors, use `numpy.vdot`.
- If you need contraction over arbitrary axes, consider `numpy.tensordot`.
- When using `out`, treat it as a performance-oriented feature: it must already be correctly shaped and typed for the result.
