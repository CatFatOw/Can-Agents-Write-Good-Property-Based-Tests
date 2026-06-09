# numpy.linspace

## Overview

`numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None)`

Return evenly spaced samples over a specified interval.

`numpy.linspace` generates exactly `num` samples between `start` and `stop`. By default, the interval is closed and includes `stop`. If `endpoint=False`, `stop` is excluded and the spacing is computed over a half-open interval.

If `start` or `stop` is array-like, samples are generated for each broadcasted pair of start and stop values, with the sample dimension placed on `axis`.

## Parameters

- `start : array_like`
  Starting value of the sequence.

- `stop : array_like`
  End value of the sequence when `endpoint=True`.

  When `endpoint=False`, `stop` is not included. Instead, the result contains the first `num` samples from a partition of the interval into `num + 1` evenly spaced points, so the spacing changes.

- `num : int, optional`
  Number of samples to generate. Default is `50`.

  `num` is converted using `operator.index`, so integer-like objects implementing `__index__` are accepted. The value must be non-negative.

- `endpoint : bool, optional`
  If `True`, `stop` is included as the last sample when `num > 1`. Default is `True`.

  If `False`, `stop` is excluded.

- `retstep : bool, optional`
  If `True`, return a tuple `(samples, step)`, where `step` is the spacing between samples.

  Default is `False`.

- `dtype : dtype, optional`
  Output dtype.

  If omitted, the dtype is inferred from `start` and `stop`, but the inferred dtype is always inexact: integer inputs produce a floating-point result rather than an integer result.

  If an integer dtype is explicitly requested, values are floored toward negative infinity before being cast to that dtype.

- `axis : int, optional`
  Axis in the result along which the samples are stored. Relevant when `start` or `stop` is array-like.

  By default, `axis=0`, so the sample dimension is inserted at the beginning. Use `axis=-1` to place the sample dimension at the end.

- `device : str, optional`
  Device on which to place the created array. Default is `None`.

  This parameter is for Array API interoperability. If provided, it must be `"cpu"`.

## Returns

- `samples : ndarray`
  Array containing `num` evenly spaced samples.

  If `endpoint=True`, samples lie in the closed interval `[start, stop]`.

  If `endpoint=False`, samples lie in the half-open interval `[start, stop)`.

  For broadcastable `start` and `stop`, before axis movement the result shape is:

  ```python
  (num,) + broadcast_shape(start, stop)
  ```

  If `axis != 0`, that leading sample dimension is moved to `axis`.

- `step : float or ndarray, optional`
  Returned only when `retstep=True`.

  The spacing between samples. For scalar `start` and `stop`, this is a scalar. For array-like `start` or `stop`, it follows the broadcasted shape of `start` and `stop` when the spacing is defined.

  Let:

  ```python
  div = num - 1 if endpoint else num
  ```

  If `div > 0`, then:

  ```python
  step = (stop - start) / div
  ```

  If `div <= 0`, then `step` is `nan`.

When `retstep=False`, only `samples` is returned. When `retstep=True`, the return value is exactly:

```python
(samples, step)
```

## Raises

- `ValueError`
  Raised if `num` is negative.

- `TypeError`
  Raised if `num` cannot be converted by `operator.index`.

- `ValueError` or `TypeError`
  May be raised if `start` and `stop` cannot be converted to compatible arrays, cannot be broadcast together, or cannot be cast to the requested `dtype`.

- `numpy.exceptions.AxisError`
  May be raised if `axis` is outside the valid range for the result dimensions.

- `ValueError`
  May be raised if `device` is provided with a value other than `"cpu"`.

## Semantic Guarantees

- `num` is converted with `operator.index`.
- If the converted `num` is negative, `linspace` raises `ValueError` before producing samples.
- If inputs are valid and `retstep=False`, the return value is the samples array.
- If inputs are valid and `retstep=True`, the return value is a 2-tuple: `(samples, step)`.
- Let `div = num - 1 if endpoint else num`. If `retstep=True`, the returned `step` is `(stop - start) / div` when `div > 0`, and `nan` when `div <= 0`.
- For broadcastable `start` and `stop`, the sample dimension has length exactly `num`.
- Before axis movement, the shape is `(num,) + broadcast_shape(start, stop)`.
- If `axis != 0`, the sample dimension is moved from axis `0` to the requested `axis`.
- If `num > 0`, the first generated sample is `start` after normal dtype conversion.
- If `endpoint=True` and `num > 1`, the last generated sample is explicitly set to `stop` before any integer-dtype flooring.
- If `endpoint=False` and `num > 0`, `stop` is not forced into the output.
- If `dtype` is omitted, the inferred output dtype is inexact and is never an integer dtype.
- If an integer `dtype` is explicitly requested, samples are floored toward negative infinity before being cast to that integer dtype.

## Edge Cases

- `num=0` returns an empty samples array. With `retstep=True`, the returned `step` is `nan`.
- `num=1` and `endpoint=True` returns a single sample equal to `start` after dtype conversion. With `retstep=True`, the returned `step` is `nan`.
- `num=1` and `endpoint=False` returns a single sample equal to `start` after dtype conversion. In this case, with `retstep=True`, the returned step is `stop - start`.
- Since NumPy 1.20, explicitly requested integer dtypes use flooring toward negative infinity rather than truncation toward zero.
- If `start` and `stop` are arrays, they must be broadcastable.
- If `axis=-1`, the sample dimension is placed at the end of the result.

## Examples

Basic closed interval:

```python
import numpy as np

np.linspace(2.0, 3.0, num=5)
```

```python
array([2.  , 2.25, 2.5 , 2.75, 3.  ])
```

Exclude the endpoint:

```python
np.linspace(2.0, 3.0, num=5, endpoint=False)
```

```python
array([2. , 2.2, 2.4, 2.6, 2.8])
```

Return the spacing:

```python
np.linspace(2.0, 3.0, num=5, retstep=True)
```

```python
(array([2.  , 2.25, 2.5 , 2.75, 3.  ]), 0.25)
```

Integer inputs still infer a floating-point dtype:

```python
np.linspace(1, 5, num=5)
```

```python
array([1., 2., 3., 4., 5.])
```

Explicit integer dtype floors toward negative infinity:

```python
np.linspace(-1.5, 1.5, num=4, dtype=int)
```

```python
array([-2, -1,  0,  1])
```

Use array-like endpoints:

```python
np.linspace([0, 10], [4, 20], num=3)
```

```python
array([[ 0., 10.],
       [ 2., 15.],
       [ 4., 20.]])
```

Place the sample axis at the end:

```python
np.linspace([0, 10], [4, 20], num=3, axis=-1)
```

```python
array([[ 0.,  2.,  4.],
       [10., 15., 20.]])
```

Empty output:

```python
np.linspace(0, 1, num=0)
```

```python
array([], dtype=float64)
```

## Notes

`numpy.linspace` differs from `numpy.arange` in how the sequence is specified. `linspace` uses a requested number of samples, while `arange` uses a step size.

Related functions:

- `numpy.arange`: generate values using a step size.
- `numpy.geomspace`: generate values evenly spaced on a logarithmic scale.
- `numpy.logspace`: generate logarithmically spaced values with endpoints specified as powers.
