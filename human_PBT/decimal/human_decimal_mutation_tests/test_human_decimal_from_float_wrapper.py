from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
from decimal import Decimal, getcontext
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Human written property based testing

# -------------------Decimal.from_float()-----------------------------
# converts a float ito a Decimal while preserving current decimal context


# Invariant: nan, inf, -inf get Preserved 
def test_preserved():
    nan_value = float("nan")
    inf_value = float("inf")
    neg_inf_value = float("-inf")

    assert Decimal.from_float(nan_value).is_nan()
    assert Decimal.from_float(inf_value) == Decimal("Infinity")
    assert Decimal.from_float(neg_inf_value) == Decimal("-Infinity")


# Invariant: Sign is preserved
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False))
def test_sign(x):
    x_val = Decimal.from_float(x)
    if x > 0:
        assert x_val > Decimal("0")
    elif x < 0:
        assert x_val < Decimal("0")
    else:
        assert x_val == Decimal("0")

# Invairant: round trip
@given(floats(min_value=-50, max_value=50, allow_nan=False, allow_infinity=False))
def test_round_trip(x):
    assert float(Decimal.from_float(x)) == x



