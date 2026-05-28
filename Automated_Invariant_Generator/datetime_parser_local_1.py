from hypothesis import given, strategies as st
from dateutil.parser import parse
import datetime

# Helper function to generate valid timestrings
def gen_timestr():
    return st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd", "-", "/", ".", " ", ":")))

# Helper function to generate valid tzinfos
def gen_tzinfos():
    return st.dictionaries(
        keys=st.text(),
        values=st.one_of(st.integers(), st.sampled_from([datetime.timezone.utc]))
    )

@given(timestr=gen_timestr())
def test_parse_validity(timestr):
    # Check that parse does not raise an exception for valid timestrings
    try:
        result = parse(timestr)
        assert isinstance(result, datetime.datetime) or (isinstance(result, tuple) and len(result) == 2)
    except Exception as e:
        assert False, f"Failed to parse {timestr}: {e}"

@given(timestr=gen_timestr(), default=st.datetimes())
def test_default_behavior(timestr, default):
    # Check that the parsed datetime replaces elements from the default object
    result = parse(timestr, default=default)
    if isinstance(result, tuple):
        result = result[0]
    assert result.year != default.year or result.month != default.month or result.day != default.day or \
           result.hour != default.hour or result.minute != default.minute or result.second != default.second

@given(timestr=gen_timestr(), ignoretz=st.booleans())
def test_ignoretz_behavior(timestr, ignoretz):
    # Check that time zones in parsed strings are ignored if ignoretz is True
    result = parse(timestr, ignoretz=ignoretz)
    assert (result.tzinfo is None) == ignoretz

@given(timestr=gen_timestr(), tzinfos=gen_tzinfos())
def test_tzinfos_behavior(timestr, tzinfos):
    # Check that the parsed datetime object has the correct timezone info
    result = parse(timestr, tzinfos=tzinfos)
    if isinstance(result, tuple):
        result = result[0]
    assert result.tzinfo in tzinfos.values() or (result.tzinfo is None)

@given(timestr=gen_timestr(), dayfirst=st.booleans())
def test_dayfirst_behavior(timestr, dayfirst):
    # Check that the parsed datetime correctly interprets ambiguous 3-integer dates
    try:
        result = parse(timestr, dayfirst=dayfirst)
        assert isinstance(result, datetime.datetime)
    except Exception as e:
        assert False, f"Failed to parse {timestr} with dayfirst={dayfirst}: {e}"

@given(timestr=gen_timestr(), yearfirst=st.booleans())
def test_yearfirst_behavior(timestr, yearfirst):
    # Check that the parsed datetime correctly interprets ambiguous 3-integer dates
    try:
        result = parse(timestr, yearfirst=yearfirst)
        assert isinstance(result, datetime.datetime)
    except Exception as e:
        assert False, f"Failed to parse {timestr} with yearfirst={yearfirst}: {e}"

@given(timestr=gen_timestr(), fuzzy=st.booleans())
def test_fuzzy_behavior(timestr, fuzzy):
    # Check that fuzzy parsing works correctly
    try:
        result = parse(timestr, fuzzy=fuzzy)
        assert isinstance(result, datetime.datetime) or (isinstance(result, tuple) and len(result) == 2)
    except Exception as e:
        assert False, f"Failed to parse {timestr} with fuzzy={fuzzy}: {e}"

@given(timestr=gen_timestr(), fuzzy_with_tokens=st.booleans())
def test_fuzzy_with_tokens_behavior(timestr, fuzzy_with_tokens):
    # Check that fuzzy parsing with tokens returns a tuple
    if fuzzy_with_tokens:
        result = parse(timestr, fuzzy_with_tokens=fuzzy_with_tokens)
        assert isinstance(result, tuple) and len(result) == 2
        assert isinstance(result[0], datetime.datetime)
        assert isinstance(result[1], tuple)
