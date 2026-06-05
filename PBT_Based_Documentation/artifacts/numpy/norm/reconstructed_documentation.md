# norm

## Overview

`numpy.linalg.norm` computes a vector norm or matrix norm.

Which norm is computed depends primarily on:

- the value of `ord`, and
- whether `axis` selects a single axis (vector mode) or two axes (matrix mode).

If `axis` is not given, `norm` behaves like a vector norm for 1-D inputs and a matrix norm for 2-D inputs. There is also an important default case: `norm(x)` with `ord=None` computes the Euclidean norm of the flattened array, even for arrays with more than two dimensions.

This function supports real and complex inputs.

---

## Parameters

### `x : array_like`

Input array.

- If `axis is None`, `x` is typically interpreted as:
  - a vector when `x.ndim == 1`,
  - a matrix when `x.ndim == 2`.
- With `ord=None`, `x` may have any dimensionality; the norm is then computed from the flattened data.
- With an explicit `axis`:
  - an integer axis selects vector norms,
  - a 2-tuple of axes selects matrix norms.

### `ord : {int, float, inf, -inf, 'fro', 'nuc'}, optional`

Order of the norm.

Common values include:

- **Vector norms**
  - `None` or `2`: Euclidean norm
  - `inf`: maximum absolute value
  - `-inf`: minimum absolute value
  - `0`: number of nonzero entries
  - `1`: sum of absolute values
  - other real numbers: `sum(abs(x)**ord)**(1/ord)`

- **Matrix norms**
  - `None`, `'fro'`, `'f'`: Frobenius norm
  - `'nuc'`: nuclear norm
  - `1`, `-1`: maximum/minimum column sum
  - `inf`, `-inf`: maximum/minimum row sum
  - `2`, `-2`: largest/smallest singular value

### `axis : None, int, or tuple of two ints, optional`

Axis or axes along which to compute the norm.

- `None`:
  - default interpretation based on dimensionality and `ord`
- integer:
  - compute vector norms along that axis
- 2-tuple of integers:
  - compute matrix norms over those two axes

### `keepdims : bool, optional`

If `True`, the axes being reduced are left in the result with size 1, so the output broadcasts against the input.

Default is `False`.

---

## Returns

### `n : float or ndarray`

The computed norm.

- Returns a scalar when the reduction removes all dimensions.
- Returns an array when norms are computed across one axis of a higher-dimensional array or across matrix axes of a stack of matrices.

---

## Raises

### `ValueError`

May be raised in cases including:

- invalid norm orders for the selected mode,
- duplicate axes in a 2-axis matrix norm,
- an improper number of axes for the requested operation,
- matrix-only orders used in vector mode.

### `TypeError`

May be raised if `axis` is not `None`, an integer, or a tuple of integers.

Other axis-related exceptions may also occur for invalid axis values.

---

## Semantic Guarantees

### 1. Default `norm(x)` flattens the input when `ord=None`

When both `axis` and `ord` are omitted, `norm(x)` computes the Euclidean norm of `x.ravel(order='K')`.

This means:

- it works for arrays of any dimensionality,
- it is not restricted to only 1-D or 2-D inputs in this default case,
- with `keepdims=True`, the result keeps one singleton dimension for each original dimension.

In effect:

```python
np.linalg.norm(x)
```

behaves like the Euclidean norm of the flattened array.

### 2. In vector mode, `ord=0` counts nonzero entries

When `axis` selects a single axis, `ord=0` does **not** compute a power-based norm. Instead, it counts how many entries are nonzero along that axis.

So for vector norms:

```python
np.linalg.norm(x, ord=0, axis=axis)
```

is equivalent in meaning to counting `x != 0` along that axis.

This is numeric output, not boolean output.

### 3. String norm orders are mode-dependent

String-valued orders are interpreted differently depending on whether you are computing a vector norm or a matrix norm.

- In **vector mode** (single axis), string orders such as `'fro'` and `'nuc'` are invalid.
- In **matrix mode** (two axes), these are supported:
  - `'fro'`
  - `'f'` as an alias for Frobenius norm
  - `'nuc'`

Unsupported strings raise `ValueError`.

### 4. Matrix norms require two distinct axes

When `axis` is a 2-tuple, the two axes must be different.

Duplicate axes such as `(1, 1)` are rejected.

If `keepdims=True`, those two matrix axes are preserved as size-1 dimensions in the output. This makes the result broadcast-compatible with the original array.

### 5. Some matrix norms are defined by singular values

For matrix norms with a 2-axis `axis` tuple:

- `ord=2` returns the largest singular value,
- `ord=-2` returns the smallest singular value,
- `ord='nuc'` returns the sum of the singular values.

This applies to each selected matrix in a stack, regardless of where the matrix axes appear in the array.

---

## Edge Cases

### Higher-dimensional arrays with `axis=None`

A subtle but important distinction:

- `np.linalg.norm(x)` with `ord=None` works by flattening `x`, even if `x.ndim > 2`.
- Matrix-specific orders such as `'fro'` are not generally defined for arbitrary-rank arrays unless you explicitly specify matrix axes with `axis=(..., ...)`.

Example:

```python
x = np.ones((2, 3, 4))
np.linalg.norm(x)          # valid: norm of flattened array
np.linalg.norm(x, 'fro')   # typically not valid without explicit matrix axes
```

### `keepdims=True`

`keepdims=True` preserves reduced axes as length-1 dimensions.

- In vector mode, the selected axis remains with size 1.
- In matrix mode, both selected axes remain with size 1.

This is useful when you want to divide by norms using broadcasting.

### Complex inputs

For complex arrays, norms use absolute values in the usual way. For example, vector Euclidean norms are based on magnitudes, not on separate handling by the caller.

### Matrix-only orders in vector mode

Orders such as `'fro'` and `'nuc'` are matrix-only. They raise `ValueError` if you use them with a single-axis vector norm.

### Duplicate matrix axes

Passing the same axis twice in matrix mode raises `ValueError`.

---

## Examples

### Basic vector norm

```python
import numpy as np

x = np.array([3.0, 4.0])
np.linalg.norm(x)
# 5.0
```

### Default behavior on a higher-dimensional array

```python
x = np.arange(8).reshape(2, 2, 2)
np.linalg.norm(x)
# Euclidean norm of x.ravel(order='K')
```

### Count nonzero entries with `ord=0`

```python
x = np.array([[1, 0, 2],
              [0, 0, 3]])

np.linalg.norm(x, ord=0, axis=1)
# array([2., 1.])
```

### Vector norms along an axis

```python
x = np.array([[1, 2, 3],
              [4, 5, 6]])

np.linalg.norm(x, axis=0)
# array([4.12310563, 5.38516481, 6.70820393])

np.linalg.norm(x, ord=1, axis=1)
# array([ 6., 15.])
```

### Frobenius norm of a matrix

```python
A = np.array([[1.0, 2.0],
              [3.0, 4.0]])

np.linalg.norm(A, ord='fro')
# 5.477225575051661
```

### `'f'` is an alias for matrix Frobenius norm

```python
np.linalg.norm(A, ord='f', axis=(0, 1)) == np.linalg.norm(A, ord='fro', axis=(0, 1))
# True
```

### Nuclear norm and spectral norm

```python
A = np.array([[1.0, 0.0],
              [0.0, 2.0]])

np.linalg.norm(A, ord=2)
# 2.0  (largest singular value)

np.linalg.norm(A, ord=-2)
# 1.0  (smallest singular value)

np.linalg.norm(A, ord='nuc')
# 3.0  (sum of singular values)
```

### Matrix norms over non-last axes

```python
x = np.arange(24.0).reshape(2, 3, 4)

# Treat axes 0 and 2 as the matrix axes
np.linalg.norm(x, ord='fro', axis=(0, 2))
```

### `keepdims=True` for broadcasting

```python
x = np.array([[3.0, 4.0],
              [0.0, 5.0]])

n = np.linalg.norm(x, axis=1, keepdims=True)
# shape (2, 1)

x / n
# rows scaled by their vector norms
```

### Invalid string order in vector mode

```python
x = np.array([1.0, 2.0, 3.0])

np.linalg.norm(x, ord='fro')
# raises ValueError
```

### Duplicate axes in matrix mode

```python
A = np.eye(3)
np.linalg.norm(A, ord='fro', axis=(0, 0))
# raises ValueError
```

---

## Notes

- `norm` covers both vector and matrix norms in one API.
- The meaning of `ord` depends on whether you are in vector mode or matrix mode.
- For higher-dimensional inputs, use `axis` explicitly when you want norms of vectors or matrices embedded inside a larger array.
- For matrix norms based on singular values (`ord=2`, `ord=-2`, `'nuc'`), results are computed per selected matrix in the stack.
