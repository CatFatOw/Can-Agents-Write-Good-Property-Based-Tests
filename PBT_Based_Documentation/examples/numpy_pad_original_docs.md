# numpy.pad

Source: [NumPy reference documentation](https://numpy.org/doc/stable/reference/generated/numpy.pad.html)

## Signature

```python
numpy.pad(array, pad_width, mode='constant', **kwargs)
```

## Description

Pad an array.

The public reference documentation describes the accepted parameters, built-in modes, callable mode behavior, return value, notes, and examples for padding one-dimensional and multidimensional arrays.

## Parameters

### `array`

Array-like input of rank N. This is the array to pad.

### `pad_width`

Number of values padded to the edges of each axis.

Accepted forms include a single integer, one pair applied to all axes, or one `(before, after)` pair per axis.

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

## Keyword Parameters

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

## Example

```python
import numpy as np

a = [1, 2, 3, 4, 5]
np.pad(a, (2, 3), mode='reflect')
```

Result:

```python
array([3, 2, 1, 2, 3, 4, 5, 4, 3, 2])
```

