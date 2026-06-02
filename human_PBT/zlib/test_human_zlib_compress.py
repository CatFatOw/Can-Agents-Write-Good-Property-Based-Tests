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




# Evaulate Soundness /validity
map1 = evaluate_test(test_round_trip)
map2 = evaluate_test(test_deep_compression)
map3 = evaluate_test(test_same)
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