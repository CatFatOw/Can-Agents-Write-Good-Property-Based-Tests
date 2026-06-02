from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from, binary
import numpy as np
import pytest
import zlib_target as zlib
import math



# Human written property based testing

# -------------------zlib.decompress()-----------------------------
# takes in compressed bytes and reconstruct the data completely

@composite
def generate_compressed_data(draw):
    data = draw(binary())
    # Compress the data
    compressed = zlib.compress(data)
    return data, compressed

# Invariant: The decompressed data == original data
@given(generate_compressed_data())
def test_same_data(params):
    data, compressed = params
    assert zlib.decompress(compressed) == data

# Invariant: multiple levels of compression with same decompression should have same data
@given(generate_compressed_data())
def test_compression(params):
    data, compressed = params
    c2 = zlib.compress(compressed)
    assert zlib.decompress(zlib.decompress(c2)) == data

# Invariant: same result
@given(generate_compressed_data())
def test_deterministic(params):
    data, compressed = params
    assert zlib.decompress(compressed) == zlib.decompress(compressed)
