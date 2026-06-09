# np.pad

## Overview

`np.pad(array, pad_width, mode='constant', **kwargs)` pads an array along one or more axes and returns a new `ndarray`.

The input is first converted with `np.asarray(array)`. The padding specification is normalized to one `(before, after)` pair for each axis. The returned array has the same rank as the converted input, with each dimension enlarged by the corresponding before- and after-padding widths.

Supported built-in modes are:

| Mode | Behavior |
|---|---|
| `constant` | Pads with constant values. This is the default. |
| `edge` | Pads with the edge values of the array. |
| `linear_ramp` | Pads with a linear ramp between an end value and the array edge value. |
| `maximum` | Pads with the maximum value of all or part of each vector along an axis. |
| `mean` | Pads with the mean value of all or part of each vector along an axis. |
| `median` | Pads with the median value of all or part of each vector along an axis. |
| `minimum` | Pads with the minimum value of all or part of each vector along an axis. |
| `reflect` | Pads with a reflection of the vector mirrored on the first and last values along an axis. |
| `symmetric` | Pads with a reflection of the vector mirrored along the edge of the array. |
| `wrap` | Pads by wrapping values from the opposite edge of the vector. |
| `empty` | Pads with undefined values. |

`mode` may also be a callable. In that case, `np.pad` creates a zero-padded array and calls the supplied function in-place on one-dimensional slices.

## Parameters

### `array` : array_like of rank N

The array to pad. The value is converted using `np.asarray(array)` before padding is applied.

### `pad_width` : sequence, array_like, or int

Number of values to pad at the beginning and end of each axis.

Accepted forms are normalized to one `(before, after)` pair per axis:

- `int`: pads before and after every axis by the same amount.
- `(pad,)`: equivalent to `int`.
- `(before, after)`: applies the same before- and after-padding to every axis.
- `((before, after),)`: equivalent to `(before, after)` for every axis.
- `((before_1, after_1), ..., (before_N, after_N))`: specifies unique before- and after-padding widths for each axis.

`pad_width` must have an integral dtype after `np.asarray(pad_width)`. Invalid padding specifications, including those that cannot be broadcast to one pair per axis, are rejected.

### `mode` : str or callable, optional

Padding mode. Default is `constant`.

If `mode` is a string, it must be one of the supported built-in modes listed in the overview.

If `mode` is callable, it must have the signature:

```python
padding_func(vector, iaxis_pad_width, iaxis, kwargs)
```

The callable must modify `vector` in-place.

## Returns

### `pad` : ndarray

The padded array.

The result has the same rank as `np.asarray(array)`. If the normalized padding for axis `i` is `(before_i, after_i)`, then:

```python
result.shape[i] == array.shape[i] + before_i + after_i
```

For built-in string modes, the original input values are preserved in the central unpadded region of the result.

## Raises

### `TypeError`

Raised when `pad_width` does not have an integral dtype after conversion with `np.asarray(pad_width)`.

### `ValueError`

Raised when:

- `mode` is a non-callable value that is not one of the supported mode strings.
- A keyword argument is supplied that is not supported by the selected built-in mode.
- `array.size == 0`, the selected built-in mode is not `constant` or `empty`, and padding would extend an axis whose original length is `0`.
- `pad_width` or a mode-specific width/length argument cannot be normalized to the required per-axis pair form.
- A padding width or index-like mode-specific argument is otherwise invalid, such as a negative padding width.

## Semantic Guarantees

- On every successful call, the result is an `ndarray` with the same rank as `np.asarray(array)`.
- After `pad_width` is normalized to one `(before, after)` pair per axis, `result.shape[i] == array.shape[i] + before_i + after_i` for every axis `i`.
- For built-in string modes, the original input values are preserved in the central unpadded region.
- `pad_width` must have an integral dtype after `np.asarray(pad_width)`.
- For non-callable modes, `mode` must be one of the supported strings.
- For non-callable modes, passing a keyword argument not allowed for the selected mode raises `ValueError`.
- In `constant` mode, padded cells are filled from `constant_values`, defaulting to `0`.
- If `array.size == 0`, only `constant` and `empty` may extend an empty axis.
- Callable modes receive `(vector, pad_width_for_axis, axis, kwargs)` and must modify the vector in-place.

## Edge Cases

### Empty arrays

For empty input arrays, only `constant` and `empty` may extend an axis of length `0`.

```python
np.pad([], 2, mode='constant')
```

Modes such as `edge`, `mean`, `reflect`, and `wrap` require existing values from the input and cannot extend an empty axis.

### `empty` mode

`empty` creates the padded output shape but does not initialize the padded area. Values in the padded region are undefined and must not be relied on.

### Multidimensional padding order

For arrays with rank greater than one, padding of later axes can be computed from padding already applied to earlier axes.

### Reflection and wrapping larger than the input length

For `reflect`, `symmetric`, and `wrap`, padding may be larger than the original axis length. The implementation fills such regions iteratively until the full requested padding width has been produced.

## Examples

### Constant padding

```python
import numpy as np

a = [1, 2, 3, 4, 5]
np.pad(a, (2, 3), mode='constant', constant_values=(4, 6))
```

Result:

```python
array([4, 4, 1, 2, 3, 4, 5, 6, 6, 6])
```

### Reflect padding

```python
np.pad(a, (2, 3), mode='reflect')
```

Result:

```python
array([3, 2, 1, 2, 3, 4, 5, 4, 3, 2])
```

### Callable padding function

```python
def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value

a = np.arange(6).reshape((2, 3))
np.pad(a, 2, pad_with)
```

## Notes

`np.pad` was added in NumPy 1.7.0. The `empty` mode was added in NumPy 1.17.

For built-in modes, `np.pad` validates mode-specific keyword arguments before applying padding. For callable modes, `np.pad` delegates padding behavior to the supplied function after creating a zero-padded working array.
