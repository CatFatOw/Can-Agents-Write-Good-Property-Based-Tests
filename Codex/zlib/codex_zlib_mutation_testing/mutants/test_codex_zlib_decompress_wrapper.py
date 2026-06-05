from hypothesis import given, strategies as st
import zlib_target as zlib
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Summary: Generate bounded binary payloads, including empty input and repeated
# bytes, then compress them into representative zlib, raw, and gzip streams.
# Draw small and default-sized initial output buffers to exercise resizing while
# checking that decompression restores the original bytes deterministically.
@given(st.data())
def test_decompress_property(data):
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
    bufsize = data.draw(
        st.sampled_from(
            [
                1,
                16,
                1_024,
                zlib.DEF_BUF_SIZE,
            ]
        )
    )

    compressed = zlib.compress(value, level=level, wbits=wbits)
    result = zlib.decompress(compressed, wbits=wbits, bufsize=bufsize)

    # Decompression returns the original byte string regardless of the stream
    # format or initial output buffer size.
    assert isinstance(result, bytes)
    assert result == value

    # Decompression is deterministic for the same input and options.
    assert zlib.decompress(compressed, wbits=wbits, bufsize=bufsize) == result

    # The default invocation handles the default compression format and agrees
    # with its explicit argument values.
    default_compressed = zlib.compress(value)
    assert zlib.decompress(default_compressed) == value
    assert zlib.decompress(
        default_compressed,
        wbits=zlib.MAX_WBITS,
        bufsize=zlib.DEF_BUF_SIZE,
    ) == value
# End program
