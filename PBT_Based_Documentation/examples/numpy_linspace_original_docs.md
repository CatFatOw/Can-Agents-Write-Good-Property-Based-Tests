# numpy.linspace

Source: [NumPy reference documentation](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html)

## Signature

```python
numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0, *, device=None)
```

## Description

Return evenly spaced numbers over a specified interval.

The public reference documentation states that `numpy.linspace` returns `num` evenly spaced samples calculated over `[start, stop]`. The endpoint can optionally be excluded with `endpoint=False`.

## Parameters From Public Docs

### `start`

Starting value of the sequence.

### `stop`

End value of the sequence unless `endpoint=False`. When `endpoint=False`, the returned sequence excludes `stop`, and the step size changes.

### `num`

Number of samples to generate. Default is `50`. Must be non-negative.

### `endpoint`

If `True`, `stop` is the last sample. Otherwise, it is not included.

### `retstep`

If `True`, return `(samples, step)`, where `step` is the spacing between samples.

### `dtype`

Output dtype. If omitted, dtype is inferred from `start` and `stop`, but the inferred dtype is never integer.

### `axis`

Axis in the result that stores samples when `start` or `stop` is array-like.

### `device`

Array API interoperability parameter. If provided, it must be `"cpu"`.

## Returns

### `samples`

An `ndarray` containing `num` equally spaced samples in the closed interval `[start, stop]` or half-open interval `[start, stop)`.

### `step`

Returned only when `retstep=True`. This is the spacing between generated samples.

## See Also

- `numpy.arange`
- `numpy.geomspace`
- `numpy.logspace`
- How to create arrays with regularly-spaced values

## Examples

```python
import numpy as np

np.linspace(2.0, 3.0, num=5)
```

```python
array([2.  , 2.25, 2.5 , 2.75, 3.  ])
```

```python
np.linspace(2.0, 3.0, num=5, endpoint=False)
```

```python
array([2. , 2.2, 2.4, 2.6, 2.8])
```

```python
np.linspace(2.0, 3.0, num=5, retstep=True)
```

```python
(array([2.  , 2.25, 2.5 , 2.75, 3.  ]), 0.25)
```

Graphical illustration from the public docs:

```python
import matplotlib.pyplot as plt

N = 8
y = np.zeros(N)
x1 = np.linspace(0, 10, N, endpoint=True)
x2 = np.linspace(0, 10, N, endpoint=False)
plt.plot(x1, y, 'o')
plt.plot(x2, y + 0.5, 'o')
plt.ylim([-0.5, 1])
plt.show()
```
