from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from, binary,text
import numpy as np
import pytest,sys
from pathlib import Path
import zlib
import math
import random, string

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------zlib.adler32()-----------------------------
# computes an Adler-32 checksum of some data.
# The value that adler 32 returns can be used to determine if the compressed data was modified/changed

def insert_random(text, draw):
    """Function inserts a random character in text"""
    random_idx = draw(integers(0, len(text)))
    char = chr(draw(integers(32, 32+32)))
    return  text[:random_idx] + char + text[random_idx:]

def delete_random(text, draw):
    """Function deletes a random character in text"""
    random_idx = draw(integers(0, len(text)-1))
    return text[:random_idx] + text[random_idx+1:]

def flip_random_char(text, draw):
    """Function flips a random character in the txt """
    idx = draw(integers(0, len(text) - 1))

    # choose a different character
    new_char = draw(sampled_from(string.ascii_letters))
    while new_char == text[idx]:
        new_char = draw(sampled_from((string.ascii_letters)))

    return text[:idx] + new_char + text[idx + 1:]



@composite
def generate_data(draw):
    original_data = draw(text(min_size=1))
    mutations = [insert_random, delete_random, flip_random_char]
    mutator = draw(sampled_from(mutations))
    new_data = mutator(original_data, draw)
    # Make them into bytes
    return original_data.encode(), new_data.encode()

# Invariant: the same data should be the same adler32
@given(generate_data())
def test_same_data(params):
    original, new = params
    assert zlib.adler32(original) == zlib.adler32(original)

# Invariant: different data should have different adler
@given(generate_data())
def test_different_data(params):
    original, new = params
    assert zlib.adler32(original) != zlib.adler32(new)

# Invariant: check sum property
@given(binary(), binary())
def test_check_sum(a, b):
    assert zlib.adler32(a+b) == zlib.adler32(b, zlib.adler32(a))




# Evaulate Soundness /validity
map1 = evaluate_test(test_check_sum)
map2 = evaluate_test(test_different_data)
map3 = evaluate_test(test_same_data)
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