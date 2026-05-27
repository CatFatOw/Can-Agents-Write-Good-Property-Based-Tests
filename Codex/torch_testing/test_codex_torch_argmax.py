from hypothesis import given, strategies as st
import torch
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Properties used for torch.argmax:
# 1. The returned index tensor has dtype torch.long.
# 2. When dim is omitted, the result is a scalar index into the flattened input.
# 3. The selected value is equal to the maximum value of the searched tensor.
# 4. When there are ties, argmax returns the first maximal index.
# 5. When dim is provided, the output shape matches the reduced shape, respecting keepdim.


# Summary: Generate small non-empty tensors with one to three dimensions and
# bounded integer values.  Bounded shapes avoid memory blowups, while integers
# naturally create tie cases and avoid floating-point overflow or NaN behavior.
@given(st.data())
def test_argmax(data):
    rank = data.draw(st.integers(min_value=1, max_value=3))
    shape = tuple(
        data.draw(st.integers(min_value=1, max_value=5)) for _ in range(rank)
    )
    total_elements = 1
    for size in shape:
        total_elements *= size

    values = data.draw(
        st.lists(
            st.integers(min_value=-1000, max_value=1000),
            min_size=total_elements,
            max_size=total_elements,
        )
    )
    tensor = torch.tensor(values, dtype=torch.int64).reshape(shape)

    # Exercise both documented modes: flattened argmax and argmax along a
    # selected dimension.  keepdim only matters for the dimension-wise form.
    use_dim = data.draw(st.booleans())
    keepdim = data.draw(st.booleans())

    if not use_dim:
        result = torch.argmax(tensor)
        flattened = tensor.flatten()
        max_value = torch.max(flattened)

        # Without dim, PyTorch returns a scalar LongTensor containing a valid
        # flattened index.
        assert result.dtype == torch.long
        assert result.shape == torch.Size([])
        assert 0 <= result.item() < tensor.numel()

        # The chosen index must point at a maximum value.
        assert flattened[result].item() == max_value.item()

        # PyTorch documents that ties resolve to the first maximal value.
        first_max_index = (flattened == max_value).nonzero(as_tuple=False)[0].item()
        assert result.item() == first_max_index
        return

    dim = data.draw(st.integers(min_value=-rank, max_value=rank - 1))
    normalized_dim = dim % rank
    result = torch.argmax(tensor, dim=dim, keepdim=keepdim)
    max_values = torch.max(tensor, dim=dim, keepdim=keepdim).values

    # With dim, PyTorch returns one index for each slice along that dimension.
    expected_shape = list(shape)
    if keepdim:
        expected_shape[normalized_dim] = 1
    else:
        expected_shape.pop(normalized_dim)

    assert result.dtype == torch.long
    assert result.shape == torch.Size(expected_shape)
    assert torch.all((0 <= result) & (result < shape[normalized_dim]))

    # Gather the values selected by argmax and compare them to torch.max over
    # the same dimension.
    gather_index = result if keepdim else result.unsqueeze(normalized_dim)
    selected_values = torch.gather(tensor, normalized_dim, gather_index)
    if not keepdim:
        selected_values = selected_values.squeeze(normalized_dim)
    assert torch.equal(selected_values, max_values)

    # Check first-tie behavior by comparing to a simple scan over each slice.
    moved = tensor.movedim(normalized_dim, -1).reshape(-1, shape[normalized_dim])
    expected_first_indices = torch.tensor(
        [int(torch.argmax(row).item()) for row in moved],
        dtype=torch.long,
    ).reshape(expected_shape)
    assert torch.equal(result, expected_first_indices)
# End program


# ACCESS Validity/Soundness.
# Run this file directly to print a metrics hashmap for plotting.  Keeping it
# behind the main guard prevents pytest from spending time on metrics during
# normal test collection.

print(evaluate_test(test_argmax))
