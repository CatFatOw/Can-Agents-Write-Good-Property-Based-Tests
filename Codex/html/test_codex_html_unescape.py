from hypothesis import given, strategies as st
import html
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


STANDARD_NAMED_REFERENCES = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&#x27;": "'",
}


# Summary: Generate bounded Unicode strings and valid Unicode code points.
# Exercise plain text, escape round trips, standard named references, decimal
# references, and hexadecimal references while respecting HTML5 behavior.
@given(st.data())
def test_unescape_property(data):
    value = data.draw(st.text(max_size=200))

    # Text without a character-reference marker is returned unchanged.
    plain_text = data.draw(st.text(alphabet=st.characters(blacklist_characters="&"), max_size=200))
    assert html.unescape(plain_text) == plain_text

    # Unescaping html.escape output recovers the original text in either mode.
    quote = data.draw(st.booleans())
    assert html.unescape(html.escape(value, quote=quote)) == value

    # Standard named references decode to their documented characters.
    reference, expected = data.draw(st.sampled_from(tuple(STANDARD_NAMED_REFERENCES.items())))
    assert html.unescape(reference) == expected

    # Decimal and hexadecimal references decode valid Unicode code points.
    expected_character = data.draw(
        st.characters(
            min_codepoint=0x20,
            exclude_categories=("Cc", "Cs", "Cn"),
        )
    )
    codepoint = ord(expected_character)
    assert html.unescape(f"&#{codepoint};") == expected_character
    assert html.unescape(f"&#x{codepoint:x};") == expected_character
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_unescape_property))
