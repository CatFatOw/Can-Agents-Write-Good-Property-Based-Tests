from hypothesis import given, strategies as st
import html
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


def expected_escape(value, quote):
    escaped = value.replace("&", "&amp;")
    escaped = escaped.replace("<", "&lt;")
    escaped = escaped.replace(">", "&gt;")
    if quote:
        escaped = escaped.replace('"', "&quot;")
        escaped = escaped.replace("'", "&#x27;")
    return escaped


# Summary: Generate bounded Unicode strings, including empty text and strings
# containing HTML-sensitive characters. Draw both quote modes and compare the
# output with the documented replacement rules while checking round trips.
@given(st.data())
def test_escape_property(data):
    value = data.draw(st.text(max_size=200))
    quote = data.draw(st.booleans())
    result = html.escape(value, quote=quote)

    # The output follows the documented replacements in their required order.
    assert result == expected_escape(value, quote)

    # Characters that are always HTML-sensitive are escaped in either mode.
    assert result.count("&lt;") == value.count("<")
    assert result.count("&gt;") == value.count(">")
    assert result.count("&amp;") >= value.count("&")

    # Quote characters are escaped only when quote=True.
    if quote:
        assert result.count("&quot;") == value.count('"')
        assert result.count("&#x27;") == value.count("'")
    else:
        assert result.count('"') == value.count('"')
        assert result.count("'") == value.count("'")

    # Unescaping an escaped string recovers the original input.
    assert html.unescape(result) == value

    # Every replacement preserves or increases the string length.
    assert len(result) >= len(value)
# End program


# ACCESS Validity/Soundness
print(evaluate_test(test_escape_property))
