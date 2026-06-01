import functools
import warnings
import operator
import types

import numpy as np
from . import numeric as _nx
from .numeric import result_type, nan, asanyarray, ndim
from numpy._core.multiarray import add_docstring
from numpy._core._multiarray_umath import _array_converter
from numpy._core import overrides

__all__ = ['logspace', 'linspace', 'geomspace']


array_function_dispatch = functools.partial(
    overrides.array_function_dispatch, module='numpy')
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def _linspace_dispatcher(start, stop, num=None, endpoint=None, retstep=None,
                         dtype=None, axis=None, *, device=None):
    return (start, stop)


def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    args = [start, stop, num, endpoint, retstep, dtype, axis]# type: ignore
    kwargs = {'device': device}# type: ignore
    return _mutmut_trampoline(x_linspace__mutmut_orig, x_linspace__mutmut_mutants, args, kwargs, None)


def x_linspace__mutmut_orig(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_1(start, stop, num=51, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_2(start, stop, num=50, endpoint=False, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_3(start, stop, num=50, endpoint=True, retstep=True, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_4(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=1, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_5(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = None
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_6(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(None)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_7(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.rindex(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_8(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num <= 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_9(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 1:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_10(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = None

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_11(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num + 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_12(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 2) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_13(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = None
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_14(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(None, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_15(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, None)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_16(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_17(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, )
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_18(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = None
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_19(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = None

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_20(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=None)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_21(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=False)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_22(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is not None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_23(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = None
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_24(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = None
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_25(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = True
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_26(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = None
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_27(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(None, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_28(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, None, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_29(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=None)
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_30(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_31(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_32(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, )
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_33(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(None))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_34(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = None

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_35(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape(None)

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_36(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        None, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_37(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, None, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_38(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=None, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_39(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=None
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_40(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_41(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_42(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_43(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_44(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        1, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_45(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) - (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_46(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((+1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_47(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-2,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_48(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) / ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_49(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (2,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_50(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(None))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_51(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div >= 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_52(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 1:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_53(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = None
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_54(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(None)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_55(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = None
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_56(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta * div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_57(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = None
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_58(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step != 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_59(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 1 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_60(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(None).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_61(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step != 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_62(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 1).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_63(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y = div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_64(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y *= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_65(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y = delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_66(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y /= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_67(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y = step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_68(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y /= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_69(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = None
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_70(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = None

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_71(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y / delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_72(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y = start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_73(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y -= start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_74(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint or num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_75(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num >= 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_76(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 2:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_77(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = None

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_78(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[+1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_79(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-2, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_80(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis == 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_81(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 1:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_82(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = None
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_83(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(None)
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_84(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(None, copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_85(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=None))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_86(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(copy=False))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_87(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, ))
    if retstep:
        return y, step
    else:
        return y


def x_linspace__mutmut_88(start, stop, num=50, endpoint=True, retstep=False, dtype=None,
             axis=0, *, device=None):
    """
    Return evenly spaced numbers over a specified interval.

    Returns `num` evenly spaced samples, calculated over the
    interval [`start`, `stop`].

    The endpoint of the interval can optionally be excluded.

    .. versionchanged:: 1.20.0
        Values are rounded towards ``-inf`` instead of ``0`` when an
        integer ``dtype`` is specified. The old behavior can
        still be obtained with ``np.linspace(start, stop, num).astype(int)``

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The end value of the sequence, unless `endpoint` is set to False.
        In that case, the sequence consists of all but the last of ``num + 1``
        evenly spaced samples, so that `stop` is excluded.  Note that the step
        size changes when `endpoint` is False.
    num : int, optional
        Number of samples to generate. Default is 50. Must be non-negative.
    endpoint : bool, optional
        If True, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    retstep : bool, optional
        If True, return (`samples`, `step`), where `step` is the spacing
        between samples.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.
    device : str, optional
        The device on which to place the created array. Default: None.
        For Array-API interoperability only, so must be ``"cpu"`` if passed.

        .. versionadded:: 2.0.0

    Returns
    -------
    samples : ndarray
        There are `num` equally spaced samples in the closed interval
        ``[start, stop]`` or the half-open interval ``[start, stop)``
        (depending on whether `endpoint` is True or False).
    step : float, optional
        Only returned if `retstep` is True

        Size of spacing between samples.


    See Also
    --------
    arange : Similar to `linspace`, but uses a step size (instead of the
             number of samples).
    geomspace : Similar to `linspace`, but with numbers spaced evenly on a log
                scale (a geometric progression).
    logspace : Similar to `geomspace`, but with the end points specified as
               logarithms.
    :ref:`how-to-partition`

    Examples
    --------
    >>> import numpy as np
    >>> np.linspace(2.0, 3.0, num=5)
    array([2.  , 2.25, 2.5 , 2.75, 3.  ])
    >>> np.linspace(2.0, 3.0, num=5, endpoint=False)
    array([2. ,  2.2,  2.4,  2.6,  2.8])
    >>> np.linspace(2.0, 3.0, num=5, retstep=True)
    (array([2.  ,  2.25,  2.5 ,  2.75,  3.  ]), 0.25)

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 8
    >>> y = np.zeros(N)
    >>> x1 = np.linspace(0, 10, N, endpoint=True)
    >>> x2 = np.linspace(0, 10, N, endpoint=False)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    num = operator.index(num)
    if num < 0:
        raise ValueError(
            "Number of samples, %s, must be non-negative." % num
        )
    div = (num - 1) if endpoint else num

    conv = _array_converter(start, stop)
    start, stop = conv.as_arrays()
    dt = conv.result_type(ensure_inexact=True)

    if dtype is None:
        dtype = dt
        integer_dtype = False
    else:
        integer_dtype = _nx.issubdtype(dtype, _nx.integer)

    # Use `dtype=type(dt)` to enforce a floating point evaluation:
    delta = np.subtract(stop, start, dtype=type(dt))
    y = _nx.arange(
        0, num, dtype=dt, device=device
    ).reshape((-1,) + (1,) * ndim(delta))

    # In-place multiplication y *= delta/div is faster, but prevents
    # the multiplicant from overriding what class is produced, and thus
    # prevents, e.g. use of Quantities, see gh-7142. Hence, we multiply
    # in place only for standard scalar types.
    if div > 0:
        _mult_inplace = _nx.isscalar(delta)
        step = delta / div
        any_step_zero = (
            step == 0 if _mult_inplace else _nx.asanyarray(step == 0).any())
        if any_step_zero:
            # Special handling for denormal numbers, gh-5437
            y /= div
            if _mult_inplace:
                y *= delta
            else:
                y = y * delta
        else:
            if _mult_inplace:
                y *= step
            else:
                y = y * step
    else:
        # sequences with 0 items or 1 item with endpoint=True (i.e. div <= 0)
        # have an undefined step
        step = nan
        # Multiply with delta to allow possible override of output class.
        y = y * delta

    y += start

    if endpoint and num > 1:
        y[-1, ...] = stop

    if axis != 0:
        y = _nx.moveaxis(y, 0, axis)

    if integer_dtype:
        _nx.floor(y, out=y)

    y = conv.wrap(y.astype(dtype, copy=True))
    if retstep:
        return y, step
    else:
        return y

x_linspace__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_linspace__mutmut_1': x_linspace__mutmut_1, 
    'x_linspace__mutmut_2': x_linspace__mutmut_2, 
    'x_linspace__mutmut_3': x_linspace__mutmut_3, 
    'x_linspace__mutmut_4': x_linspace__mutmut_4, 
    'x_linspace__mutmut_5': x_linspace__mutmut_5, 
    'x_linspace__mutmut_6': x_linspace__mutmut_6, 
    'x_linspace__mutmut_7': x_linspace__mutmut_7, 
    'x_linspace__mutmut_8': x_linspace__mutmut_8, 
    'x_linspace__mutmut_9': x_linspace__mutmut_9, 
    'x_linspace__mutmut_10': x_linspace__mutmut_10, 
    'x_linspace__mutmut_11': x_linspace__mutmut_11, 
    'x_linspace__mutmut_12': x_linspace__mutmut_12, 
    'x_linspace__mutmut_13': x_linspace__mutmut_13, 
    'x_linspace__mutmut_14': x_linspace__mutmut_14, 
    'x_linspace__mutmut_15': x_linspace__mutmut_15, 
    'x_linspace__mutmut_16': x_linspace__mutmut_16, 
    'x_linspace__mutmut_17': x_linspace__mutmut_17, 
    'x_linspace__mutmut_18': x_linspace__mutmut_18, 
    'x_linspace__mutmut_19': x_linspace__mutmut_19, 
    'x_linspace__mutmut_20': x_linspace__mutmut_20, 
    'x_linspace__mutmut_21': x_linspace__mutmut_21, 
    'x_linspace__mutmut_22': x_linspace__mutmut_22, 
    'x_linspace__mutmut_23': x_linspace__mutmut_23, 
    'x_linspace__mutmut_24': x_linspace__mutmut_24, 
    'x_linspace__mutmut_25': x_linspace__mutmut_25, 
    'x_linspace__mutmut_26': x_linspace__mutmut_26, 
    'x_linspace__mutmut_27': x_linspace__mutmut_27, 
    'x_linspace__mutmut_28': x_linspace__mutmut_28, 
    'x_linspace__mutmut_29': x_linspace__mutmut_29, 
    'x_linspace__mutmut_30': x_linspace__mutmut_30, 
    'x_linspace__mutmut_31': x_linspace__mutmut_31, 
    'x_linspace__mutmut_32': x_linspace__mutmut_32, 
    'x_linspace__mutmut_33': x_linspace__mutmut_33, 
    'x_linspace__mutmut_34': x_linspace__mutmut_34, 
    'x_linspace__mutmut_35': x_linspace__mutmut_35, 
    'x_linspace__mutmut_36': x_linspace__mutmut_36, 
    'x_linspace__mutmut_37': x_linspace__mutmut_37, 
    'x_linspace__mutmut_38': x_linspace__mutmut_38, 
    'x_linspace__mutmut_39': x_linspace__mutmut_39, 
    'x_linspace__mutmut_40': x_linspace__mutmut_40, 
    'x_linspace__mutmut_41': x_linspace__mutmut_41, 
    'x_linspace__mutmut_42': x_linspace__mutmut_42, 
    'x_linspace__mutmut_43': x_linspace__mutmut_43, 
    'x_linspace__mutmut_44': x_linspace__mutmut_44, 
    'x_linspace__mutmut_45': x_linspace__mutmut_45, 
    'x_linspace__mutmut_46': x_linspace__mutmut_46, 
    'x_linspace__mutmut_47': x_linspace__mutmut_47, 
    'x_linspace__mutmut_48': x_linspace__mutmut_48, 
    'x_linspace__mutmut_49': x_linspace__mutmut_49, 
    'x_linspace__mutmut_50': x_linspace__mutmut_50, 
    'x_linspace__mutmut_51': x_linspace__mutmut_51, 
    'x_linspace__mutmut_52': x_linspace__mutmut_52, 
    'x_linspace__mutmut_53': x_linspace__mutmut_53, 
    'x_linspace__mutmut_54': x_linspace__mutmut_54, 
    'x_linspace__mutmut_55': x_linspace__mutmut_55, 
    'x_linspace__mutmut_56': x_linspace__mutmut_56, 
    'x_linspace__mutmut_57': x_linspace__mutmut_57, 
    'x_linspace__mutmut_58': x_linspace__mutmut_58, 
    'x_linspace__mutmut_59': x_linspace__mutmut_59, 
    'x_linspace__mutmut_60': x_linspace__mutmut_60, 
    'x_linspace__mutmut_61': x_linspace__mutmut_61, 
    'x_linspace__mutmut_62': x_linspace__mutmut_62, 
    'x_linspace__mutmut_63': x_linspace__mutmut_63, 
    'x_linspace__mutmut_64': x_linspace__mutmut_64, 
    'x_linspace__mutmut_65': x_linspace__mutmut_65, 
    'x_linspace__mutmut_66': x_linspace__mutmut_66, 
    'x_linspace__mutmut_67': x_linspace__mutmut_67, 
    'x_linspace__mutmut_68': x_linspace__mutmut_68, 
    'x_linspace__mutmut_69': x_linspace__mutmut_69, 
    'x_linspace__mutmut_70': x_linspace__mutmut_70, 
    'x_linspace__mutmut_71': x_linspace__mutmut_71, 
    'x_linspace__mutmut_72': x_linspace__mutmut_72, 
    'x_linspace__mutmut_73': x_linspace__mutmut_73, 
    'x_linspace__mutmut_74': x_linspace__mutmut_74, 
    'x_linspace__mutmut_75': x_linspace__mutmut_75, 
    'x_linspace__mutmut_76': x_linspace__mutmut_76, 
    'x_linspace__mutmut_77': x_linspace__mutmut_77, 
    'x_linspace__mutmut_78': x_linspace__mutmut_78, 
    'x_linspace__mutmut_79': x_linspace__mutmut_79, 
    'x_linspace__mutmut_80': x_linspace__mutmut_80, 
    'x_linspace__mutmut_81': x_linspace__mutmut_81, 
    'x_linspace__mutmut_82': x_linspace__mutmut_82, 
    'x_linspace__mutmut_83': x_linspace__mutmut_83, 
    'x_linspace__mutmut_84': x_linspace__mutmut_84, 
    'x_linspace__mutmut_85': x_linspace__mutmut_85, 
    'x_linspace__mutmut_86': x_linspace__mutmut_86, 
    'x_linspace__mutmut_87': x_linspace__mutmut_87, 
    'x_linspace__mutmut_88': x_linspace__mutmut_88
}
x_linspace__mutmut_orig.__name__ = 'x_linspace'


def _logspace_dispatcher(start, stop, num=None, endpoint=None, base=None,
                         dtype=None, axis=None):
    return (start, stop, base)


@array_function_dispatch(_logspace_dispatcher)
def logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None,
             axis=0):
    """
    Return numbers spaced evenly on a log scale.

    In linear space, the sequence starts at ``base ** start``
    (`base` to the power of `start`) and ends with ``base ** stop``
    (see `endpoint` below).

    .. versionchanged:: 1.25.0
        Non-scalar 'base` is now supported

    Parameters
    ----------
    start : array_like
        ``base ** start`` is the starting value of the sequence.
    stop : array_like
        ``base ** stop`` is the final value of the sequence, unless `endpoint`
        is False.  In that case, ``num + 1`` values are spaced over the
        interval in log-space, of which all but the last (a sequence of
        length `num`) are returned.
    num : integer, optional
        Number of samples to generate.  Default is 50.
    endpoint : boolean, optional
        If true, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    base : array_like, optional
        The base of the log space. The step size between the elements in
        ``ln(samples) / ln(base)`` (or ``log_base(samples)``) is uniform.
        Default is 10.0.
    dtype : dtype
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred type will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start,
        stop, or base are array-like.  By default (0), the samples will be
        along a new axis inserted at the beginning. Use -1 to get an axis at
        the end.

    Returns
    -------
    samples : ndarray
        `num` samples, equally spaced on a log scale.

    See Also
    --------
    arange : Similar to linspace, with the step size specified instead of the
             number of samples. Note that, when used with a float endpoint, the
             endpoint may or may not be included.
    linspace : Similar to logspace, but with the samples uniformly distributed
               in linear space, instead of log space.
    geomspace : Similar to logspace, but with endpoints specified directly.
    :ref:`how-to-partition`

    Notes
    -----
    If base is a scalar, logspace is equivalent to the code

    >>> y = np.linspace(start, stop, num=num, endpoint=endpoint)
    ... # doctest: +SKIP
    >>> power(base, y).astype(dtype)
    ... # doctest: +SKIP

    Examples
    --------
    >>> import numpy as np
    >>> np.logspace(2.0, 3.0, num=4)
    array([ 100.        ,  215.443469  ,  464.15888336, 1000.        ])
    >>> np.logspace(2.0, 3.0, num=4, endpoint=False)
    array([100.        ,  177.827941  ,  316.22776602,  562.34132519])
    >>> np.logspace(2.0, 3.0, num=4, base=2.0)
    array([4.        ,  5.0396842 ,  6.34960421,  8.        ])
    >>> np.logspace(2.0, 3.0, num=4, base=[2.0, 3.0], axis=-1)
    array([[ 4.        ,  5.0396842 ,  6.34960421,  8.        ],
           [ 9.        , 12.98024613, 18.72075441, 27.        ]])

    Graphical illustration:

    >>> import matplotlib.pyplot as plt
    >>> N = 10
    >>> x1 = np.logspace(0.1, 1, N, endpoint=True)
    >>> x2 = np.logspace(0.1, 1, N, endpoint=False)
    >>> y = np.zeros(N)
    >>> plt.plot(x1, y, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(x2, y + 0.5, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.ylim([-0.5, 1])
    (-0.5, 1)
    >>> plt.show()

    """
    if not isinstance(base, (float, int)) and np.ndim(base):
        # If base is non-scalar, broadcast it with the others, since it
        # may influence how axis is interpreted.
        ndmax = np.broadcast(start, stop, base).ndim
        start, stop, base = (
            np.array(a, copy=None, subok=True, ndmin=ndmax)
            for a in (start, stop, base)
        )
        base = np.expand_dims(base, axis=axis)
    y = linspace(start, stop, num=num, endpoint=endpoint, axis=axis)
    if dtype is None:
        return _nx.power(base, y)
    return _nx.power(base, y).astype(dtype, copy=False)


def _geomspace_dispatcher(start, stop, num=None, endpoint=None, dtype=None,
                          axis=None):
    return (start, stop)


@array_function_dispatch(_geomspace_dispatcher)
def geomspace(start, stop, num=50, endpoint=True, dtype=None, axis=0):
    """
    Return numbers spaced evenly on a log scale (a geometric progression).

    This is similar to `logspace`, but with endpoints specified directly.
    Each output sample is a constant multiple of the previous.

    Parameters
    ----------
    start : array_like
        The starting value of the sequence.
    stop : array_like
        The final value of the sequence, unless `endpoint` is False.
        In that case, ``num + 1`` values are spaced over the
        interval in log-space, of which all but the last (a sequence of
        length `num`) are returned.
    num : integer, optional
        Number of samples to generate.  Default is 50.
    endpoint : boolean, optional
        If true, `stop` is the last sample. Otherwise, it is not included.
        Default is True.
    dtype : dtype
        The type of the output array.  If `dtype` is not given, the data type
        is inferred from `start` and `stop`. The inferred dtype will never be
        an integer; `float` is chosen even if the arguments would produce an
        array of integers.
    axis : int, optional
        The axis in the result to store the samples.  Relevant only if start
        or stop are array-like.  By default (0), the samples will be along a
        new axis inserted at the beginning. Use -1 to get an axis at the end.

    Returns
    -------
    samples : ndarray
        `num` samples, equally spaced on a log scale.

    See Also
    --------
    logspace : Similar to geomspace, but with endpoints specified using log
               and base.
    linspace : Similar to geomspace, but with arithmetic instead of geometric
               progression.
    arange : Similar to linspace, with the step size specified instead of the
             number of samples.
    :ref:`how-to-partition`

    Notes
    -----
    If the inputs or dtype are complex, the output will follow a logarithmic
    spiral in the complex plane.  (There are an infinite number of spirals
    passing through two points; the output will follow the shortest such path.)

    Examples
    --------
    >>> import numpy as np
    >>> np.geomspace(1, 1000, num=4)
    array([    1.,    10.,   100.,  1000.])
    >>> np.geomspace(1, 1000, num=3, endpoint=False)
    array([   1.,   10.,  100.])
    >>> np.geomspace(1, 1000, num=4, endpoint=False)
    array([   1.        ,    5.62341325,   31.6227766 ,  177.827941  ])
    >>> np.geomspace(1, 256, num=9)
    array([   1.,    2.,    4.,    8.,   16.,   32.,   64.,  128.,  256.])

    Note that the above may not produce exact integers:

    >>> np.geomspace(1, 256, num=9, dtype=int)
    array([  1,   2,   4,   7,  16,  32,  63, 127, 256])
    >>> np.around(np.geomspace(1, 256, num=9)).astype(int)
    array([  1,   2,   4,   8,  16,  32,  64, 128, 256])

    Negative, decreasing, and complex inputs are allowed:

    >>> np.geomspace(1000, 1, num=4)
    array([1000.,  100.,   10.,    1.])
    >>> np.geomspace(-1000, -1, num=4)
    array([-1000.,  -100.,   -10.,    -1.])
    >>> np.geomspace(1j, 1000j, num=4)  # Straight line
    array([0.   +1.j, 0.  +10.j, 0. +100.j, 0.+1000.j])
    >>> np.geomspace(-1+0j, 1+0j, num=5)  # Circle
    array([-1.00000000e+00+1.22464680e-16j, -7.07106781e-01+7.07106781e-01j,
            6.12323400e-17+1.00000000e+00j,  7.07106781e-01+7.07106781e-01j,
            1.00000000e+00+0.00000000e+00j])

    Graphical illustration of `endpoint` parameter:

    >>> import matplotlib.pyplot as plt
    >>> N = 10
    >>> y = np.zeros(N)
    >>> plt.semilogx(np.geomspace(1, 1000, N, endpoint=True), y + 1, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.semilogx(np.geomspace(1, 1000, N, endpoint=False), y + 2, 'o')
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.axis([0.5, 2000, 0, 3])
    [0.5, 2000, 0, 3]
    >>> plt.grid(True, color='0.7', linestyle='-', which='both', axis='both')
    >>> plt.show()

    """
    start = asanyarray(start)
    stop = asanyarray(stop)
    if _nx.any(start == 0) or _nx.any(stop == 0):
        raise ValueError('Geometric sequence cannot include zero')

    dt = result_type(start, stop, float(num), _nx.zeros((), dtype))
    if dtype is None:
        dtype = dt
    else:
        # complex to dtype('complex128'), for instance
        dtype = _nx.dtype(dtype)

    # Promote both arguments to the same dtype in case, for instance, one is
    # complex and another is negative and log would produce NaN otherwise.
    # Copy since we may change things in-place further down.
    start = start.astype(dt, copy=True)
    stop = stop.astype(dt, copy=True)

    # Allow negative real values and ensure a consistent result for complex
    # (including avoiding negligible real or imaginary parts in output) by
    # rotating start to positive real, calculating, then undoing rotation.
    out_sign = _nx.sign(start)
    start /= out_sign
    stop = stop / out_sign

    log_start = _nx.log10(start)
    log_stop = _nx.log10(stop)
    result = logspace(log_start, log_stop, num=num,
                      endpoint=endpoint, base=10.0, dtype=dt)

    # Make sure the endpoints match the start and stop arguments. This is
    # necessary because np.exp(np.log(x)) is not necessarily equal to x.
    if num > 0:
        result[0] = start
        if num > 1 and endpoint:
            result[-1] = stop

    result *= out_sign

    if axis != 0:
        result = _nx.moveaxis(result, 0, axis)

    return result.astype(dtype, copy=False)


def _needs_add_docstring(obj):
    args = [obj]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__needs_add_docstring__mutmut_orig, x__needs_add_docstring__mutmut_mutants, args, kwargs, None)


def x__needs_add_docstring__mutmut_orig(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_1(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = None

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_2(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 >> 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_3(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 2 << 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_4(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 10

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_5(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) or obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_6(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ | Py_TPFLAGS_HEAPTYPE:
        return False

    return True


def x__needs_add_docstring__mutmut_7(obj):
    """
    Returns true if the only way to set the docstring of `obj` from python is
    via add_docstring.

    This function errs on the side of being overly conservative.
    """
    Py_TPFLAGS_HEAPTYPE = 1 << 9

    if isinstance(obj, (types.FunctionType, types.MethodType, property)):
        return False

    if isinstance(obj, type) and obj.__flags__ & Py_TPFLAGS_HEAPTYPE:
        return False

    return False

x__needs_add_docstring__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__needs_add_docstring__mutmut_1': x__needs_add_docstring__mutmut_1, 
    'x__needs_add_docstring__mutmut_2': x__needs_add_docstring__mutmut_2, 
    'x__needs_add_docstring__mutmut_3': x__needs_add_docstring__mutmut_3, 
    'x__needs_add_docstring__mutmut_4': x__needs_add_docstring__mutmut_4, 
    'x__needs_add_docstring__mutmut_5': x__needs_add_docstring__mutmut_5, 
    'x__needs_add_docstring__mutmut_6': x__needs_add_docstring__mutmut_6, 
    'x__needs_add_docstring__mutmut_7': x__needs_add_docstring__mutmut_7
}
x__needs_add_docstring__mutmut_orig.__name__ = 'x__needs_add_docstring'


def _add_docstring(obj, doc, warn_on_python):
    args = [obj, doc, warn_on_python]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x__add_docstring__mutmut_orig, x__add_docstring__mutmut_mutants, args, kwargs, None)


def x__add_docstring__mutmut_orig(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, doc)
    except Exception:
        pass


def x__add_docstring__mutmut_1(obj, doc, warn_on_python):
    if warn_on_python or not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, doc)
    except Exception:
        pass


def x__add_docstring__mutmut_2(obj, doc, warn_on_python):
    if warn_on_python and _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, doc)
    except Exception:
        pass


def x__add_docstring__mutmut_3(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(None):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, doc)
    except Exception:
        pass


def x__add_docstring__mutmut_4(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(None, doc)
    except Exception:
        pass


def x__add_docstring__mutmut_5(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, None)
    except Exception:
        pass


def x__add_docstring__mutmut_6(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(doc)
    except Exception:
        pass


def x__add_docstring__mutmut_7(obj, doc, warn_on_python):
    if warn_on_python and not _needs_add_docstring(obj):
        warnings.warn(
            "add_newdoc was used on a pure-python object {}. "
            "Prefer to attach it directly to the source."
            .format(obj),
            UserWarning,
            stacklevel=3)
    try:
        add_docstring(obj, )
    except Exception:
        pass

x__add_docstring__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x__add_docstring__mutmut_1': x__add_docstring__mutmut_1, 
    'x__add_docstring__mutmut_2': x__add_docstring__mutmut_2, 
    'x__add_docstring__mutmut_3': x__add_docstring__mutmut_3, 
    'x__add_docstring__mutmut_4': x__add_docstring__mutmut_4, 
    'x__add_docstring__mutmut_5': x__add_docstring__mutmut_5, 
    'x__add_docstring__mutmut_6': x__add_docstring__mutmut_6, 
    'x__add_docstring__mutmut_7': x__add_docstring__mutmut_7
}
x__add_docstring__mutmut_orig.__name__ = 'x__add_docstring'


def add_newdoc(place, obj, doc, warn_on_python=True):
    args = [place, obj, doc, warn_on_python]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_add_newdoc__mutmut_orig, x_add_newdoc__mutmut_mutants, args, kwargs, None)


def x_add_newdoc__mutmut_orig(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_1(place, obj, doc, warn_on_python=False):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_2(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = None
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_3(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(None, obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_4(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), None)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_5(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_6(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), )
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_7(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(None, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_8(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, None, {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_9(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), None, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_10(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, None), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_11(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_12(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_13(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_14(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, ), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_15(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "XX${ARRAY_FUNCTION_LIKE}XX" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_16(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${array_function_like}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_17(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" not in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_18(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = None
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_19(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(None, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_20(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, None)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_21(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_22(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, )
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_23(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(None, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_24(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, None, warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_25(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), None)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_26(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_27(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_28(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), )
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_29(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = None
        _add_docstring(getattr(new, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_30(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(None, docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_31(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), None, warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_32(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), None)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_33(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_34(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_35(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, attr), docstring.strip(), )
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_36(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(None, attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_37(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, None), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_38(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(attr), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )


def x_add_newdoc__mutmut_39(place, obj, doc, warn_on_python=True):
    """
    Add documentation to an existing object, typically one defined in C

    The purpose is to allow easier editing of the docstrings without requiring
    a re-compile. This exists primarily for internal use within numpy itself.

    Parameters
    ----------
    place : str
        The absolute name of the module to import from
    obj : str or None
        The name of the object to add documentation to, typically a class or
        function name.
    doc : {str, Tuple[str, str], List[Tuple[str, str]]}
        If a string, the documentation to apply to `obj`

        If a tuple, then the first element is interpreted as an attribute
        of `obj` and the second as the docstring to apply -
        ``(method, docstring)``

        If a list, then each element of the list should be a tuple of length
        two - ``[(method1, docstring1), (method2, docstring2), ...]``
    warn_on_python : bool
        If True, the default, emit `UserWarning` if this is used to attach
        documentation to a pure-python object.

    Notes
    -----
    This routine never raises an error if the docstring can't be written, but
    will raise an error if the object being documented does not exist.

    This routine cannot modify read-only docstrings, as appear
    in new-style classes or built-in functions. Because this
    routine never raises an error the caller must check manually
    that the docstrings were changed.

    Since this function grabs the ``char *`` from a c-level str object and puts
    it into the ``tp_doc`` slot of the type of `obj`, it violates a number of
    C-API best-practices, by:

    - modifying a `PyTypeObject` after calling `PyType_Ready`
    - calling `Py_INCREF` on the str and losing the reference, so the str
      will never be released

    If possible it should be avoided.
    """
    new = getattr(__import__(place, globals(), {}, [obj]), obj)
    if isinstance(doc, str):
        if "${ARRAY_FUNCTION_LIKE}" in doc:
            doc = overrides.get_array_function_like_doc(new, doc)
        _add_docstring(new, doc.strip(), warn_on_python)
    elif isinstance(doc, tuple):
        attr, docstring = doc
        _add_docstring(getattr(new, ), docstring.strip(), warn_on_python)
    elif isinstance(doc, list):
        for attr, docstring in doc:
            _add_docstring(
                getattr(new, attr), docstring.strip(), warn_on_python
            )

x_add_newdoc__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_add_newdoc__mutmut_1': x_add_newdoc__mutmut_1, 
    'x_add_newdoc__mutmut_2': x_add_newdoc__mutmut_2, 
    'x_add_newdoc__mutmut_3': x_add_newdoc__mutmut_3, 
    'x_add_newdoc__mutmut_4': x_add_newdoc__mutmut_4, 
    'x_add_newdoc__mutmut_5': x_add_newdoc__mutmut_5, 
    'x_add_newdoc__mutmut_6': x_add_newdoc__mutmut_6, 
    'x_add_newdoc__mutmut_7': x_add_newdoc__mutmut_7, 
    'x_add_newdoc__mutmut_8': x_add_newdoc__mutmut_8, 
    'x_add_newdoc__mutmut_9': x_add_newdoc__mutmut_9, 
    'x_add_newdoc__mutmut_10': x_add_newdoc__mutmut_10, 
    'x_add_newdoc__mutmut_11': x_add_newdoc__mutmut_11, 
    'x_add_newdoc__mutmut_12': x_add_newdoc__mutmut_12, 
    'x_add_newdoc__mutmut_13': x_add_newdoc__mutmut_13, 
    'x_add_newdoc__mutmut_14': x_add_newdoc__mutmut_14, 
    'x_add_newdoc__mutmut_15': x_add_newdoc__mutmut_15, 
    'x_add_newdoc__mutmut_16': x_add_newdoc__mutmut_16, 
    'x_add_newdoc__mutmut_17': x_add_newdoc__mutmut_17, 
    'x_add_newdoc__mutmut_18': x_add_newdoc__mutmut_18, 
    'x_add_newdoc__mutmut_19': x_add_newdoc__mutmut_19, 
    'x_add_newdoc__mutmut_20': x_add_newdoc__mutmut_20, 
    'x_add_newdoc__mutmut_21': x_add_newdoc__mutmut_21, 
    'x_add_newdoc__mutmut_22': x_add_newdoc__mutmut_22, 
    'x_add_newdoc__mutmut_23': x_add_newdoc__mutmut_23, 
    'x_add_newdoc__mutmut_24': x_add_newdoc__mutmut_24, 
    'x_add_newdoc__mutmut_25': x_add_newdoc__mutmut_25, 
    'x_add_newdoc__mutmut_26': x_add_newdoc__mutmut_26, 
    'x_add_newdoc__mutmut_27': x_add_newdoc__mutmut_27, 
    'x_add_newdoc__mutmut_28': x_add_newdoc__mutmut_28, 
    'x_add_newdoc__mutmut_29': x_add_newdoc__mutmut_29, 
    'x_add_newdoc__mutmut_30': x_add_newdoc__mutmut_30, 
    'x_add_newdoc__mutmut_31': x_add_newdoc__mutmut_31, 
    'x_add_newdoc__mutmut_32': x_add_newdoc__mutmut_32, 
    'x_add_newdoc__mutmut_33': x_add_newdoc__mutmut_33, 
    'x_add_newdoc__mutmut_34': x_add_newdoc__mutmut_34, 
    'x_add_newdoc__mutmut_35': x_add_newdoc__mutmut_35, 
    'x_add_newdoc__mutmut_36': x_add_newdoc__mutmut_36, 
    'x_add_newdoc__mutmut_37': x_add_newdoc__mutmut_37, 
    'x_add_newdoc__mutmut_38': x_add_newdoc__mutmut_38, 
    'x_add_newdoc__mutmut_39': x_add_newdoc__mutmut_39
}
x_add_newdoc__mutmut_orig.__name__ = 'x_add_newdoc'
