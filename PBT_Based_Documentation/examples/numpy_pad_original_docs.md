# numpy.pad

Source: [NumPy reference documentation](https://numpy.org/doc/stable/reference/generated/numpy.pad.html)

## Signature

```python
numpy.pad(array, pad_width, mode='constant', **kwargs)
```

## Description

Pad an array.

The public reference documentation describes the accepted parameters, built-in modes, callable mode behavior, return value, notes, and examples for padding one-dimensional and multidimensional arrays.

## Parameters From Public Docs

### `array`

Array-like input of rank N. This is the array to pad.

### `pad_width`

Number of values padded to the edges of each axis. The public docs describe sequence, array-like, int, and dict forms.

Accepted forms include:

- `((before_1, after_1), ... (before_N, after_N))`: unique pad widths for each axis.
- `(before, after)` or `((before, after),)`: same before and after padding for each axis.
- `(pad,)` or `int`: shortcut for `before = after = pad` on every axis.
- `dict`: each key is an axis and each value is an int or `(before, after)` pair for that axis.

### `mode`

String mode or user-supplied function.

| Mode | Public-doc behavior |
|---|---|
| `constant` | Pads with a constant value. |
| `edge` | Pads with edge values of the array. |
| `linear_ramp` | Pads with a linear ramp between an end value and the array edge. |
| `maximum` | Pads with the maximum of all or part of each vector. |
| `mean` | Pads with the mean of all or part of each vector. |
| `median` | Pads with the median of all or part of each vector. |
| `minimum` | Pads with the minimum of all or part of each vector. |
| `reflect` | Pads with a reflection mirrored on the first and last values. |
| `symmetric` | Pads with a reflection mirrored along the edge. |
| `wrap` | Pads by wrapping values from the opposite edge. |
| `empty` | Pads with undefined values. |

## Mode-Specific Keyword Parameters

- `stat_length` applies to `maximum`, `mean`, `median`, and `minimum`.
- `constant_values` applies to `constant`.
- `end_values` applies to `linear_ramp`.
- `reflect_type` applies to `reflect` and `symmetric`.

## Returns

The result is an `ndarray` with rank equal to `array` and shape increased according to `pad_width`.

## Notes

For rank greater than one, padding of later axes may be calculated from padding already applied to previous axes. Callable padding functions operate in-place on rank-1 slices with this signature:

```python
padding_func(vector, iaxis_pad_width, iaxis, kwargs)
```

## Examples

```python
import numpy as np

a = [1, 2, 3, 4, 5]
np.pad(a, (2, 3), 'constant', constant_values=(4, 6))
```

```python
array([4, 4, 1, ..., 6, 6, 6])
```

```python
np.pad(a, (2, 3), 'edge')
```

```python
array([1, 1, 1, ..., 5, 5, 5])
```

```python
np.pad(a, (2, 3), 'linear_ramp', end_values=(5, -4))
```

```python
array([ 5,  3,  1,  2,  3,  4,  5,  2, -1, -4])
```

```python
np.pad(a, (2,), 'maximum')
```

```python
array([5, 5, 1, 2, 3, 4, 5, 5, 5])
```

```python
np.pad(a, (2,), 'mean')
```

```python
array([3, 3, 1, 2, 3, 4, 5, 3, 3])
```

```python
a = [[1, 2], [3, 4]]
np.pad(a, ((3, 2), (2, 3)), 'minimum')
```

```python
array([[1, 1, 1, 2, 1, 1, 1],
       [1, 1, 1, 2, 1, 1, 1],
       [1, 1, 1, 2, 1, 1, 1],
       [1, 1, 1, 2, 1, 1, 1],
       [3, 3, 3, 4, 3, 3, 3],
       [1, 1, 1, 2, 1, 1, 1],
       [1, 1, 1, 2, 1, 1, 1]])
```

```python
a = [1, 2, 3, 4, 5]
np.pad(a, (2, 3), 'reflect')
```

```python
array([3, 2, 1, 2, 3, 4, 5, 4, 3, 2])
```

```python
np.pad(a, (2, 3), 'reflect', reflect_type='odd')
```

```python
array([-1,  0,  1,  2,  3,  4,  5,  6,  7,  8])
```

```python
np.pad(a, (2, 3), 'wrap')
```

```python
array([4, 5, 1, 2, 3, 4, 5, 1, 2, 3])
```

Dictionary padding examples from the public docs:

```python
a = np.arange(1, 7).reshape(2, 3)
np.pad(a, {1: (1, 2)})
```

```python
array([[0, 1, 2, 3, 0, 0],
       [0, 4, 5, 6, 0, 0]])
```

```python
np.pad(a, {-1: 2})
```

```python
array([[0, 0, 1, 2, 3, 0, 0],
       [0, 0, 4, 5, 6, 0, 0]])
```
