from hypothesis import given, assume, settings, Verbosity
from hypothesis.strategies import integers, floats, lists, booleans, text, composite, sampled_from
from pathlib import Path
import os, sys, random
import html
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Human written property based testing

# -------------------html.unescape()-----------------------------
# Converts the keyboard representation characters: &, <, > back into the original format (opposite of html.escape()) 


# Generate the data 
@composite 
def generate_html_chars(draw):
    """Function generates random string with html specific cahracters inserted"""
    characters = ["&lt;", "&amp;", "&gt;", "&quot;", "&#x27;"]
    # word that will get mixed with characters
    word = draw(text(min_size=1))
    random_indicies = set(draw(integers(min_value=1, max_value=len(word))) for _ in range(len(word)))

    for idx in random_indicies:
        word = word[:idx] + draw(sampled_from(characters)) + word[idx:]
    return word

    
# Invariant: length parsed <= len(original)
@given(generate_html_chars())
def test_length(html_text):
    parsed = html.unescape(html_text, )
    assert len(parsed) <= len(html_text)


# Invariant: Round circle 
@given(generate_html_chars())
def test_ideom(html_text):
    parsed = html.unescape(html_text)
    assert html.unescape(html.escape(parsed, quote=True)) == parsed


