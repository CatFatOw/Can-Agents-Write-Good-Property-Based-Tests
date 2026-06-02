from hypothesis import given, assume, settings, Verbosity
from hypothesis.strategies import integers, floats, lists, booleans, text, composite, sampled_from
from pathlib import Path
import os, sys, random
import html
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


# Human written property based testing

# -------------------html.escape()-----------------------------
# Converts characters: &, <, > into html safe representations. 
# if quote=True, then "" and ' will also be converted

# Generate the data 
@composite 
def generate_html_chars(draw):
    """Function generates random string with html specific cahracters inserted"""
    characters = ["<", ">", "&", "\"", "'"]
    # word that will get mixed with characters
    word = draw(text(min_size=1))
    times = draw(integers(min_value=0, max_value=len(word)))
    random_idx_set = set(draw(integers(min_value=1, max_value=len(word))) for _ in range(times))

    for position in random_idx_set:
        # Each time in the iteration, get random cahracter in cahracters 
        random_char = draw(sampled_from(characters))
        # Add the random character intothe word
        word = word[:position] + random_char + word[position:]
    return word 


# Invariant: Once processed and we split by ;,within each ; there should be a keyword
@given(generate_html_chars())
def test_keyword(html_text):
    # Assuming parsed parameter = False

    parsed = html.escape(html_text)
    assert parsed.count("&lt;") == html_text.count("<")
    assert parsed.count("&gt;") == html_text.count(">")
    assert parsed.count("&amp;") == html_text.count("&")

    

# Invariant: len(parsed) >= len(original)
@given(generate_html_chars())
def test_length(html_text):
    parsed = html.escape(html_text)
    assert len(parsed) >= len(html_text)


# Invariant: html.unescape should bring it back to original form
@given(generate_html_chars())
def test_ideom(html_text):
    parsed = html.escape(html_text)
    assert html_text == html.unescape(parsed)

# Invariant: if quote = True, then "", ' are also convereted 
@given(generate_html_chars())
def test_quote(html_text):
    parsed = html.escape(html_text, quote=True)

    assert parsed.count("&quot;") == html_text.count("\"")
    assert parsed.count("&#x27;") == html_text.count("'")


