"""Mutation-test adapter for selected functions from the compiled zlib module."""

import zlib as _zlib


MAX_WBITS = _zlib.MAX_WBITS
DEF_BUF_SIZE = _zlib.DEF_BUF_SIZE
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


def compress(data, level=-1, wbits=_zlib.MAX_WBITS):
    args = [data, level, wbits]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_compress__mutmut_orig, x_compress__mutmut_mutants, args, kwargs, None)


def x_compress__mutmut_orig(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, level=level, wbits=wbits)


def x_compress__mutmut_1(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(None, level=level, wbits=wbits)


def x_compress__mutmut_2(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, level=None, wbits=wbits)


def x_compress__mutmut_3(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, level=level, wbits=None)


def x_compress__mutmut_4(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(level=level, wbits=wbits)


def x_compress__mutmut_5(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, wbits=wbits)


def x_compress__mutmut_6(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, level=level, )

x_compress__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_compress__mutmut_1': x_compress__mutmut_1, 
    'x_compress__mutmut_2': x_compress__mutmut_2, 
    'x_compress__mutmut_3': x_compress__mutmut_3, 
    'x_compress__mutmut_4': x_compress__mutmut_4, 
    'x_compress__mutmut_5': x_compress__mutmut_5, 
    'x_compress__mutmut_6': x_compress__mutmut_6
}
x_compress__mutmut_orig.__name__ = 'x_compress'


def decompress(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    args = [data, wbits, bufsize]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_decompress__mutmut_orig, x_decompress__mutmut_mutants, args, kwargs, None)


def x_decompress__mutmut_orig(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, wbits=wbits, bufsize=bufsize)


def x_decompress__mutmut_1(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(None, wbits=wbits, bufsize=bufsize)


def x_decompress__mutmut_2(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, wbits=None, bufsize=bufsize)


def x_decompress__mutmut_3(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, wbits=wbits, bufsize=None)


def x_decompress__mutmut_4(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(wbits=wbits, bufsize=bufsize)


def x_decompress__mutmut_5(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, bufsize=bufsize)


def x_decompress__mutmut_6(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, wbits=wbits, )

x_decompress__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_decompress__mutmut_1': x_decompress__mutmut_1, 
    'x_decompress__mutmut_2': x_decompress__mutmut_2, 
    'x_decompress__mutmut_3': x_decompress__mutmut_3, 
    'x_decompress__mutmut_4': x_decompress__mutmut_4, 
    'x_decompress__mutmut_5': x_decompress__mutmut_5, 
    'x_decompress__mutmut_6': x_decompress__mutmut_6
}
x_decompress__mutmut_orig.__name__ = 'x_decompress'


def adler32(data, value=1):
    args = [data, value]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_adler32__mutmut_orig, x_adler32__mutmut_mutants, args, kwargs, None)


def x_adler32__mutmut_orig(data, value=1):
    return _zlib.adler32(data, value)


def x_adler32__mutmut_1(data, value=2):
    return _zlib.adler32(data, value)


def x_adler32__mutmut_2(data, value=1):
    return _zlib.adler32(None, value)


def x_adler32__mutmut_3(data, value=1):
    return _zlib.adler32(data, None)


def x_adler32__mutmut_4(data, value=1):
    return _zlib.adler32(value)


def x_adler32__mutmut_5(data, value=1):
    return _zlib.adler32(data, )

x_adler32__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_adler32__mutmut_1': x_adler32__mutmut_1, 
    'x_adler32__mutmut_2': x_adler32__mutmut_2, 
    'x_adler32__mutmut_3': x_adler32__mutmut_3, 
    'x_adler32__mutmut_4': x_adler32__mutmut_4, 
    'x_adler32__mutmut_5': x_adler32__mutmut_5
}
x_adler32__mutmut_orig.__name__ = 'x_adler32'
