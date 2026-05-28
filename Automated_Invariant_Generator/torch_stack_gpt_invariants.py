import math
from typing import List

import pytest
import torch
from hypothesis import assume, given, strategies as st
from hypothesis.extra.numpy import arrays


def _tensor_strategy():
    # Small dense tensors with consistent shape/dtype for sound stack properties.
    dtype = st.sampled_from([torch.float32, torch.float64, torch.int64])
    shape = st.tuples(st.integers(0, 3), st.integers(0, 3))

    @st.composite
    def _draw_tensor(draw):
        dt = draw(dtype)
        sh = draw(shape)
        if dt.is_floating_point:
            elem = st.floats(
                min_value=-10,
                max_value=10,
                allow_nan=False,
                allow_infinity=False,
                width=32 if dt == torch.float32 else 64,
            )
        else:
            elem = st.integers(-10, 10)
        data = draw(arrays(dtype="float64" if dt.is_floating_point else "int64", shape=sh, elements=elem))
        return torch.tensor(data, dtype=dt)

    return _draw_tensor()


def _tensor_list_strategy():
    # Need at least one tensor; all tensors same shape and dtype.
    @st.composite
    def _draw_list(draw):
        base = draw(_tensor_strategy())
        n = draw(st.integers(min_value=1, max_value=5))
        tensors = [base]
        for _ in range(n - 1):
            tensors.append(base.clone())
        return tensors

    return _draw_list()


def _valid_dim_strategy():
    return st.integers(min_value=0, max_value=3)


# 1) Shape invariant: stacking n equal-shaped tensors inserts a new dimension of size n.
@given(tensors=_tensor_list_strategy(), dim=_valid_dim_strategy())
def test_stack_shape_invariant(tensors: List[torch.Tensor], dim: int):
    base = tensors[0]
    assume(dim <= base.dim())
    result = torch.stack(tensors, dim=dim)
    expected_shape = list(base.shape)
    expected_shape.insert(dim, len(tensors))
    assert tuple(result.shape) == tuple(expected_shape)


# 2) Relationship to cat: stack == unsqueeze each tensor then cat along the inserted dim.
@given(tensors=_tensor_list_strategy(), dim=_valid_dim_strategy())
def test_stack_equivalent_to_unsqueeze_then_cat(tensors: List[torch.Tensor], dim: int):
    base = tensors[0]
    assume(dim <= base.dim())
    stacked = torch.stack(tensors, dim=dim)
    expanded = [t.unsqueeze(dim) for t in tensors]
    catted = torch.cat(expanded, dim=dim)
    assert torch.equal(stacked, catted)


# 3) Indexing invariant: selecting along the new dimension recovers the original tensors.
@given(tensors=_tensor_list_strategy(), dim=_valid_dim_strategy())
def test_stack_recovers_inputs_by_index(tensors: List[torch.Tensor], dim: int):
    base = tensors[0]
    assume(dim <= base.dim())
    stacked = torch.stack(tensors, dim=dim)
    for i, t in enumerate(tensors):
        recovered = stacked.select(dim, i)
        assert torch.equal(recovered, t)


# 4) Permutation invariant: moving the stacked dimension to the front preserves a simple slice structure.
#    This is a sound structural property for any valid dim.
@given(tensors=_tensor_list_strategy(), dim=_valid_dim_strategy())
def test_stack_move_new_axis_to_front_and_slice(tensors: List[torch.Tensor], dim: int):
    base = tensors[0]
    assume(dim <= base.dim())
    stacked = torch.stack(tensors, dim=dim)
    moved = stacked.movedim(dim, 0)
    assert moved.shape[0] == len(tensors)
    for i, t in enumerate(tensors):
        assert torch.equal(moved[i], t)


# 5) Out tensor invariant: if provided with correct shape/dtype/device, out is used and matches result.
#    Risky/conditional: requires exact output shape and a compatible dtype/device.
@given(tensors=_tensor_list_strategy(), dim=_valid_dim_strategy())
def test_stack_out_parameter_soundness(tensors: List[torch.Tensor], dim: int):
    base = tensors[0]
    assume(dim <= base.dim())
    expected = torch.stack(tensors, dim=dim)
    out = torch.empty_like(expected)
    returned = torch.stack(tensors, dim=dim, out=out)
    assert returned is out
    assert torch.equal(out, expected)
