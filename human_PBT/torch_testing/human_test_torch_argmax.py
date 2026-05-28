import torch
from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
import random

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------SECOND TEST: torch.argmax()-----------------------------

# argmax() finds the index of the largest element in a PyTorch tensor 
# torch.argmax(input, dim)
# Where input is a torch.Tensor, dim (the dimention to reduce dim=0 (row), dim=1 (col)), keepDim


# Parameter Generation
@composite 
def generate_argmax_params(draw):
    row_size = draw(integers(1, 50))
    col_size = draw(integers(1, 50))
    random_tensor = torch.rand([row_size, col_size])

    return random_tensor



# Test invariant: test if the given index corresponds with the correct value
@given(generate_argmax_params())
def test_correct_value(tensor):
    max_idx = torch.argmax(tensor)
    flattened = torch.flatten(tensor)

    assert flattened[max_idx] == torch.max(tensor)


# Test invariant: (valid index range and scaling doesn't impact)
@given(generate_argmax_params())
def test_correct_index_and_scaling(tensor):
    max_idx = torch.argmax(tensor)

    assert 0 <= max_idx.item() < tensor.numel()

    c = 5
    assert max_idx.item() == torch.argmax(tensor * c).item()


map1 = evaluate_test(test_correct_index_and_scaling)
map2 = evaluate_test(test_correct_value)

results = [map1, map2]

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
