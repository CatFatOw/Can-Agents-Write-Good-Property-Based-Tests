"""Mutation-test adapter for selected functions from the compiled zlib module."""

import zlib as _zlib


def compress(data, level=-1, wbits=_zlib.MAX_WBITS):
    return _zlib.compress(data, level=level, wbits=wbits)


def decompress(data, wbits=_zlib.MAX_WBITS, bufsize=_zlib.DEF_BUF_SIZE):
    return _zlib.decompress(data, wbits=wbits, bufsize=bufsize)


def adler32(data, value=1):
    return _zlib.adler32(data, value)
