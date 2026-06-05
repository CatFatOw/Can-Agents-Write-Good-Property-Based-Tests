from hypothesis import given, strategies as st
import html


@given(s=st.text(max_size=1000), quote=st.booleans())
def test_output_length_not_shorter(s, quote):
    # Property 5: output length >= input length.
    out = html.escape(s, quote=quote)
    assert len(out) >= len(s)
# End program