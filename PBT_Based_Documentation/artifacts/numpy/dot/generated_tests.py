import numpy as np
import pytest
from hypothesis import given, strategies as st
from hypothesis.extra import numpy as hnp


# Small finite numeric strategies to keep computations stable and realistic.
real_scalar = st.one_of(
    st.integers(-10, 10),
    st.floats(-10, 10, allow_nan=False, allow_infinity=False),
)

complex_scalar = st.complex_numbers(
    min_magnitude=0,
    max_magnitude=10,
    allow_nan=False,
    allow_infinity=False,
)

scalar = st.one_of(real_scalar, complex_scalar)


@st.composite
def same_length_1d_arrays(draw, dtype=np.float64):
    n = draw(st.integers(min_value=0, max_value=8))
    elems = st.floats(-10, 10, allow_nan=False, allow_infinity=False)
    a = draw(hnp.arrays(dtype=dtype, shape=n, elements=elems))
    b = draw(hnp.arrays(dtype=dtype, shape=n, elements=elems))
    return a, b


@st.composite
def complex_same_length_1d_arrays(draw):
    n = draw(st.integers(min_value=0, max_value=8))
    elems = st.complex_numbers(
        min_magnitude=0,
        max_magnitude=10,
        allow_nan=False,
        allow_infinity=False,
    )
    a = draw(hnp.arrays(dtype=np.complex128, shape=n, elements=elems))
    b = draw(hnp.arrays(dtype=np.complex128, shape=n, elements=elems))
    return a, b


@st.composite
def scalar_or_vector_pair(draw):
    if draw(st.booleans()):
        return draw(scalar), draw(scalar)
    return draw(same_length_1d_arrays())


@st.composite
def scalar_array_or_scalar_cases(draw):
    # At least one operand is 0-D/scalar.
    arr_shape = draw(
        st.one_of(
            st.just(()),
            st.integers(1, 3).flatmap(
                lambda ndim: st.tuples(*[st.integers(0, 4) for _ in range(ndim)])
            ),
        )
    )
    arr = draw(
        hnp.arrays(
            dtype=np.float64,
            shape=arr_shape,
            elements=st.floats(-10, 10, allow_nan=False, allow_infinity=False),
        )
    )
    s = draw(real_scalar)
    if draw(st.booleans()):
        return s, arr
    return arr, s


@st.composite
def nd_and_md_compatible(draw):
    # a.ndim >= 1, b.ndim >= 2, and a.shape[-1] == b.shape[-2]
    a_ndim = draw(st.integers(min_value=1, max_value=4))
    b_ndim = draw(st.integers(min_value=2, max_value=4))
    k = draw(st.integers(min_value=0, max_value=4))

    a_prefix = [draw(st.integers(min_value=1, max_value=4)) for _ in range(a_ndim - 1)]
    b_prefix = [draw(st.integers(min_value=1, max_value=4)) for _ in range(max(0, b_ndim - 2))]
    b_last = draw(st.integers(min_value=1, max_value=4))

    a_shape = tuple(a_prefix + [k])
    b_shape = tuple(b_prefix + [k, b_last])

    elems = st.floats(-10, 10, allow_nan=False, allow_infinity=False)
    a = draw(hnp.arrays(dtype=np.float64, shape=a_shape, elements=elems))
    b = draw(hnp.arrays(dtype=np.float64, shape=b_shape, elements=elems))
    return a, b


@st.composite
def mismatched_contracting_dims(draw):
    # Non-scalar cases where contracted dimensions are defined and unequal.
    case = draw(st.sampled_from(["1d_1d", "nd_1d", "nd_md"]))

    elems = st.floats(-10, 10, allow_nan=False, allow_infinity=False)

    if case == "1d_1d":
        n = draw(st.integers(min_value=0, max_value=5))
        m = draw(st.integers(min_value=0, max_value=5).filter(lambda x: x != n))
        a = draw(hnp.arrays(dtype=np.float64, shape=(n,), elements=elems))
        b = draw(hnp.arrays(dtype=np.float64, shape=(m,), elements=elems))
        return a, b

    if case == "nd_1d":
        ndim = draw(st.integers(min_value=1, max_value=4))
        k = draw(st.integers(min_value=0, max_value=5))
        m = draw(st.integers(min_value=0, max_value=5).filter(lambda x: x != k))
        prefix = [draw(st.integers(min_value=1, max_value=4)) for _ in range(ndim - 1)]
        a_shape = tuple(prefix + [k])
        b_shape = (m,)
        a = draw(hnp.arrays(dtype=np.float64, shape=a_shape, elements=elems))
        b = draw(hnp.arrays(dtype=np.float64, shape=b_shape, elements=elems))
        return a, b

    a_ndim = draw(st.integers(min_value=1, max_value=4))
    b_ndim = draw(st.integers(min_value=2, max_value=4))
    k = draw(st.integers(min_value=0, max_value=5))
    m = draw(st.integers(min_value=0, max_value=5).filter(lambda x: x != k))

    a_prefix = [draw(st.integers(min_value=1, max_value=4)) for _ in range(a_ndim - 1)]
    b_prefix = [draw(st.integers(min_value=1, max_value=4)) for _ in range(max(0, b_ndim - 2))]
    b_last = draw(st.integers(min_value=1, max_value=4))

    a_shape = tuple(a_prefix + [k])
    b_shape = tuple(b_prefix + [m, b_last])

    a = draw(hnp.arrays(dtype=np.float64, shape=a_shape, elements=elems))
    b = draw(hnp.arrays(dtype=np.float64, shape=b_shape, elements=elems))
    return a, b


# Property 1:
# dot returns a scalar when both inputs are scalars or both are 1-D arrays.
@given(pair=scalar_or_vector_pair())
def test_dot_scalar_output_for_scalars_and_1d_inputs(pair):
    a, b = pair
    result = np.dot(a, b)
    assert np.isscalar(result)


# Property 2:
# When either argument is 0-D/scalar, dot is equivalent to multiplication.
@given(pair=scalar_array_or_scalar_cases())
def test_dot_scalar_cases_equal_multiply(pair):
    a, b = pair
    result = np.dot(a, b)
    expected = np.multiply(a, b)
    np.testing.assert_allclose(result, expected, rtol=1e-7, atol=1e-7)


# Property 3:
# For 1-D complex inputs, dot is non-conjugating and differs from vdot
# by exactly the absence of conjugation of the first argument.
@given(pair=complex_same_length_1d_arrays())
def test_dot_1d_complex_is_nonconjugating(pair):
    a, b = pair
    result = np.dot(a, b)
    expected = np.sum(a * b)
    np.testing.assert_allclose(result, expected, rtol=1e-7, atol=1e-7)

    vdot_expected = np.sum(np.conjugate(a) * b)
    np.testing.assert_allclose(np.vdot(a, b), vdot_expected, rtol=1e-7, atol=1e-7)


# Property 4:
# For a.ndim >= 1 and b.ndim >= 2, dot contracts a's last axis with b's
# second-to-last axis, giving the documented output shape and values.
@given(pair=nd_and_md_compatible())
def test_dot_contracts_last_of_a_with_second_to_last_of_b(pair):
    a, b = pair
    result = np.dot(a, b)
    expected = np.tensordot(a, b, axes=([-1], [-2]))

    assert result.shape == a.shape[:-1] + b.shape[:-2] + b.shape[-1:]
    np.testing.assert_allclose(result, expected, rtol=1e-7, atol=1e-7)


# Property 5:
# dot raises ValueError when contracting dimensions are incompatible.
@given(pair=mismatched_contracting_dims())
def test_dot_raises_valueerror_on_mismatched_contracting_dimensions(pair):
    a, b = pair
    with pytest.raises(ValueError):
        np.dot(a, b)
