from hypothesis import given, settings, Verbosity, note, assume
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import numpy as np
import pytest,sys
from pathlib import Path
from decimal import Decimal
import math



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Human written property based testing

# -------------------Decimal().fma()-----------------------------
# fma = fuse multiply add = x * y + z. Instead of doing (x * y) + z. it does it in one operation
# Improves speed and accuracy.(less rounding)

# Invariant: fma = x * y + z
@given(
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
)
def test_fma(x, y, z):
    x_val = Decimal(str(x))
    y_val = Decimal(str(y))
    z_val = Decimal(str(z))
    assert x_val.fma(y_val, z_val) == x_val * y_val + z_val

# Invariant: Commutivity
@given(
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
)
def test_commutivity(x, y, z):
    x_val = Decimal(str(x))
    y_val = Decimal(str(y))
    z_val = Decimal(str(z))

    assert x_val.fma(y_val, z_val) == y_val.fma(x_val, z_val)


# Invariant: coefficeints 
@given(
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
    integers(min_value=-50, max_value=50),
)
def test_coefficients(x, y, z):
    x_val = Decimal(str(x))
    y_val = Decimal(str(y))
    z_val = Decimal(str(z))

    # test if x_val = 0 or y_val = 0 the nthe answer is just z 
    new_x_val = Decimal("0")
    new_y_val = Decimal("0")
    assert new_x_val.fma(y_val, z_val) == z_val

    # if z = 0, then its xy which is also communitive 
    new_z_val = Decimal("0")
    assert x_val.fma(y_val, new_z_val) == Decimal(str(x*y))


