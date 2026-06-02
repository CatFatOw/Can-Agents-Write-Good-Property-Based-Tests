from hypothesis import given, strategies as st
import zlib
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Summary: Generate bounded binary payloads, including empty input and repeated
# bytes, together with every documented compression level and representative
# zlib, raw, and gzip window modes. Check that compression returns bytes,
# round-trips through decompression, and is deterministic.
@given(st.data())
def test_compress_property(data):
    value = data.draw(st.binary(max_size=1_000))
    level = data.draw(st.integers(min_value=-1, max_value=9))
    wbits = data.draw(
        st.sampled_from(
            [
                -15,
                -9,
                9,
                zlib.MAX_WBITS,
                25,
                31,
            ]
        )
    )

    compressed = zlib.compress(value, level=level, wbits=wbits)

    # Compression returns a byte string that can be restored with the matching
    # window mode.
    assert isinstance(compressed, bytes)
    assert zlib.decompress(compressed, wbits=wbits) == value

    # Compression is deterministic for the same input and options.
    assert zlib.compress(value, level=level, wbits=wbits) == compressed

    # The default invocation also round-trips and matches its explicit options.
    default_compressed = zlib.compress(value)
    assert zlib.decompress(default_compressed) == value
    assert default_compressed == zlib.compress(
        value,
        level=-1,
        wbits=zlib.MAX_WBITS,
    )
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_compress_property))
