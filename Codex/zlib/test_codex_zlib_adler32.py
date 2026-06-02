from hypothesis import given, strategies as st
import zlib
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


ADLER_MODULUS = 65_521


def expected_adler32(value, checksum=1):
    first_sum = checksum & 0xFFFF
    second_sum = (checksum >> 16) & 0xFFFF

    for byte in value:
        first_sum = (first_sum + byte) % ADLER_MODULUS
        second_sum = (second_sum + first_sum) % ADLER_MODULUS

    return (second_sum << 16) | first_sum


# Summary: Generate bounded binary chunks, including empty input and repeated
# bytes, together with a prefix used to produce a valid rolling checksum.
# Compare zlib.adler32 with a direct Adler-32 implementation and verify
# deterministic and incremental use.
@given(st.data())
def test_adler32_property(data):
    prefix = data.draw(st.binary(max_size=1_000))
    first = data.draw(st.binary(max_size=1_000))
    second = data.draw(st.binary(max_size=1_000))
    checksum = zlib.adler32(prefix)

    result = zlib.adler32(first, checksum)

    # Adler-32 returns an unsigned 32-bit integer matching the documented
    # rolling checksum algorithm.
    assert isinstance(result, int)
    assert 0 <= result <= 2**32 - 1
    assert result == expected_adler32(first, checksum)

    # Checksums are deterministic, and omitting the starting value is
    # equivalent to using the documented default value of 1.
    assert zlib.adler32(first, checksum) == result
    assert zlib.adler32(first) == zlib.adler32(first, 1)

    # A checksum can be computed incrementally by passing the checksum of the
    # first chunk as the starting value for the second chunk.
    assert zlib.adler32(prefix + first + second) == zlib.adler32(
        second,
        result,
    )
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_adler32_property))
