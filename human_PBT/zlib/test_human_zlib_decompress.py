from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from, binary
import numpy as np
import pytest,sys
from pathlib import Path
import zlib
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

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




# Evaulate Soundness /validity
map1 = evaluate_test(test_compression)
map2 = evaluate_test(test_same_data)
map3 = evaluate_test(test_deterministic)
results = [map1, map2, map3]

# Keep a single plotting-friendly dictionary:
# numeric fields are averaged across tests, and error fields are flattened.
total = {
    "validity": sum(result["validity"] for result in results) / len(results),
    "soundness": sum(result["soundness"] for result in results) / len(results),

    "validity_errors": set(
        error
        for result in results
        for error in result["validity_errors"]
    ),

    "soundness_errors": set(
        error
        for result in results
        for error in result["soundness_errors"]
    ),
}

print(total)