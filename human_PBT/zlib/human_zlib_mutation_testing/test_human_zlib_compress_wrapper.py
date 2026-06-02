from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from, binary
import numpy as np
import pytest
import zlib_target as zlib
import math



# Human written property based testing

# -------------------zlib.compress()-----------------------------

# Invariant: The decompressed of the compressed is the original data
@given(binary())
def test_round_trip(data):
    assert zlib.decompress(zlib.compress(data)) == data

# Invariant: The same input gives the same result
@given(binary())
def test_same(data):
    assert zlib.compress(data) == zlib.compress(data)

# Invariant: Multiple levels of compression should result in same data when uncompressed
@given(binary())
def test_deep_compression(data):
    c1 = zlib.compress(data)
    c2 = zlib.compress(c1)

    assert zlib.decompress(zlib.decompress(c2)) == data
