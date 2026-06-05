1. **Property:** With `axis=None`, `norm(x)` has a flattened-default behavior: it returns the Euclidean norm of `x.ravel(order='K')` for any dimensionality, but `norm(x, ord='fro')` and `norm(x, ord=2)` are only accepted in the fast-path when `x.ndim == 2` and `x.ndim == 1` respectively; otherwise unsupported dimensions/orders eventually raise.
   - **Evidence from source:** Early branch:
     ```python
     if axis is None:
         ndim = x.ndim
         if ((ord is None) or
             (ord in ('f', 'fro') and ndim == 2) or
             (ord == 2 and ndim == 1)):
             x = x.ravel(order='K')
             ...
             return ret
     ```
     Then later:
     ```python
     if axis is None:
         axis = tuple(range(nd))
     ...
     else:
         raise ValueError("Improper number of dimensions to norm.")
     ```
   - **User-facing interpretation:** If you do not specify `axis`, the default `norm(x)` acts like a norm of the flattened array, even for arrays with more than 2 dimensions. But matrix-specific orders such as `'fro'` and vector-specific interpretations like `ord=2` are not generally accepted for arbitrary-rank arrays unless an explicit `axis` is provided.
   - **Preconditions / input domain:** Any array-like input; especially relevant for arrays with `ndim > 2`.
   - **Important edge cases:** 0-D arrays; arrays with `ndim > 2`; `ord=None`; `ord='fro'`; `ord=2`; `keepdims=True`.
   - **Why it matters:** This is a subtle but highly user-visible semantic distinction. It helps document why `norm(x)` may succeed on high-rank arrays while `norm(x, 'fro')` may fail unless matrix axes are specified.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

2. **Property:** For vector norms (`axis` resolves to exactly one axis), `ord=0` returns the count of nonzero entries along that axis, with result dtype based on `x.real.dtype`, not a boolean array.
   - **Evidence from source:**
     ```python
     elif ord == 0:
         return (
             (x != 0)
             .astype(x.real.dtype)
             .sum(axis=axis, keepdims=keepdims)
         )
     ```
   - **User-facing interpretation:** The “zero norm” is not a true norm; it counts how many entries are nonzero along the chosen vector axis. The output is numeric, not boolean.
   - **Preconditions / input domain:** Inputs where `axis` is a single axis, either explicit or normalized from an integer; any numeric or object-like array accepted by `asarray`.
   - **Important edge cases:** Complex arrays; integer arrays promoted to float earlier; all-zero vectors; vectors containing `nan` or `inf` still compare by `!= 0`; `keepdims=True`.
   - **Why it matters:** `ord=0` is special and easy to implement incorrectly as something involving powers, absolute values, or booleans. It is a strong semantic discriminator for vector-mode behavior.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

3. **Property:** String norm orders are split by mode: for vector norms, any string order (including `'fro'` and `'nuc'`) is invalid and raises `ValueError`; for matrix norms, `'fro'`, `'f'`, and `'nuc'` are accepted, while unsupported others raise `ValueError("Invalid norm order for matrices.")`.
   - **Evidence from source:**
     ```python
     if len(axis) == 1:
         ...
         elif isinstance(ord, str):
             raise ValueError(f"Invalid norm order '{ord}' for vectors")
     ```
     and
     ```python
     elif len(axis) == 2:
         ...
         elif ord in [None, 'fro', 'f']:
             ...
         elif ord == 'nuc':
             ...
         else:
             raise ValueError("Invalid norm order for matrices.")
     ```
   - **User-facing interpretation:** `'fro'` and `'nuc'` are matrix-only norm orders. They are rejected for vectors. The alias `'f'` is also accepted for matrix Frobenius norm.
   - **Preconditions / input domain:** Inputs where `axis` resolves to one axis (vector mode) or two axes (matrix mode).
   - **Important edge cases:** `axis=None` with 1-D vs 2-D input; `'f'` alias; 3-D+ arrays with explicit 2-axis matrix norm; unsupported strings like `'l1'`.
   - **Why it matters:** This is exactly the sort of API boundary users rely on and a common place for regressions or inconsistent documentation.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

4. **Property:** For matrix norms with a 2-axis `axis` tuple, duplicate axes are rejected, and when `keepdims=True` the result shape is the original shape with exactly those two axes replaced by size 1.
   - **Evidence from source:**
     ```python
     row_axis = normalize_axis_index(row_axis, nd)
     col_axis = normalize_axis_index(col_axis, nd)
     if row_axis == col_axis:
         raise ValueError('Duplicate axes given.')
     ...
     if keepdims:
         ret_shape = list(x.shape)
         ret_shape[axis[0]] = 1
         ret_shape[axis[1]] = 1
         ret = ret.reshape(ret_shape)
     ```
   - **User-facing interpretation:** Matrix norms require two distinct axes. If `keepdims=True`, those two matrix axes are preserved as singleton dimensions so the result broadcasts against the original array.
   - **Preconditions / input domain:** Inputs with explicit 2-tuple `axis`.
   - **Important edge cases:** Negative axes; axes in either order; stacked matrices; duplicate axes such as `(1,1)` or `(-1,-1)`; non-adjacent axes.
   - **Why it matters:** Shape semantics are crucial for downstream broadcasting and are easy to break when refactoring axis logic. Duplicate-axis rejection is a sharp behavioral guarantee.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending

5. **Property:** For matrix norms with `ord` in `{2, -2, 'nuc'}`, the computation is based on singular values of the matrices identified by the chosen two axes: largest singular value for `2`, smallest for `-2`, and sum for `'nuc'`.
   - **Evidence from source:**
     ```python
     def _multi_svd_norm(x, row_axis, col_axis, op):
         y = moveaxis(x, (row_axis, col_axis), (-2, -1))
         result = op(svd(y, compute_uv=False), axis=-1)
         return result
     ```
     and in `norm`:
     ```python
     if ord == 2:
         ret = _multi_svd_norm(x, row_axis, col_axis, amax)
     elif ord == -2:
         ret = _multi_svd_norm(x, row_axis, col_axis, amin)
     ...
     elif ord == 'nuc':
         ret = _multi_svd_norm(x, row_axis, col_axis, sum)
     ```
   - **User-facing interpretation:** Spectral norm, smallest-singular-value norm, and nuclear norm are defined via singular values of each matrix slice, regardless of where the matrix axes occur in the array.
   - **Preconditions / input domain:** Inputs in matrix mode (`axis` has length 2); shapes compatible with SVD.
   - **Important edge cases:** Rectangular matrices; stacked matrices with nontrivial leading dimensions; matrix axes not in the last two positions; degenerate matrices with zero singular values.
   - **Why it matters:** This is the core semantic meaning of several important matrix norms and strongly distinguishes them from row/column-sum norms. It also checks the axis-moving logic.
   - **Expected mutation-killing strength:** High
   - **Human decision:** Pending
