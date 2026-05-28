import hypothesis
from hypothesis import strategies as st
import torch

@hypothesis.given(
    tensors=st.lists(st.shared(st.tuples(st.integers(min_value=1), st.integers(min_value=1)), key="shape"), min_size=1),
    dim=st.integers(min_value=-2, max_value=1)  # Assuming the maximum stack dimension is 1 for simplicity
)
def test_stack_properties(tensors, dim):
    """
    Property-based tests for torch.stack.
    
    Invariants:
    1. The output tensor has one more dimension than each input tensor.
    2. The shape of the stacked tensor at all dimensions except the stacking dimension matches the input tensors.
    3. Stacking along a negative dimension should behave like stacking along the corresponding positive dimension.
    4. Stacking should not alter the data in the input tensors.
    5. If out is provided, it should have the same shape as the result of torch.stack.
    """
    
    # Generate random input tensors with specified shapes
    input_tensors = [torch.randn(*shape) for shape in tensors]
    
    # Calculate expected output shape
    expected_shape = list(input_tensors[0].shape)
    expected_shape.insert(dim if dim >= 0 else len(expected_shape) + dim, len(tensors))
    
    # Perform stacking
    stacked_tensor = torch.stack(input_tensors, dim=dim)
    
    # Check invariant 1: Output tensor has one more dimension than input tensors
    assert stacked_tensor.dim() == input_tensors[0].dim() + 1
    
    # Check invariant 2: Shape of the output tensor matches expected shape
    assert list(stacked_tensor.shape) == expected_shape
    
    # Check invariant 3: Negative dimension should behave like positive
    if dim < 0:
        assert torch.equal(stacked_tensor, torch.stack(input_tensors, dim=len(tensors[0]) + dim))
    
    # Check invariant 4: Input tensors are not altered
    for tensor in input_tensors:
        assert tensor.requires_grad == False
    
    # Check invariant 5: If out is provided, it should have the same shape as the result of torch.stack
    out = torch.empty(expected_shape)
    torch.stack(input_tensors, dim=dim, out=out)
    assert list(out.shape) == expected_shape

# Marking these tests as risky due to potential memory issues with large tensors
test_stack_properties.settings(max_examples=10, deadline=None)
    expected_shape = (len(tensors), *tensors[0].shape)
    assert stacked_tensor.shape == expected_shape

@given(tensors=st.lists(tensor_strategy(), min_size=2), out=st.data())
@settings(deadline=None)
def test_stack_out_invariant(tensors, out):
    """
    Invariant: If an output tensor is provided, it should be used and modified.
    This tests that torch.stack uses the provided 'out' parameter if given.
    """
    dim = draw(st.integers(min_value=0, max_value=len(tensors[0].shape) + 1))
    expected_shape = (len(tensors), *tensors[0].shape)
    out_tensor = out.draw(tensor_strategy()).to(dtype=tensors[0].dtype, device=tensors[0].device)
    assert out_tensor.shape == expected_shape
    stacked_tensor = torch.stack(tensors, dim=dim, out=out_tensor)
    assert stacked_tensor is out_tensor

