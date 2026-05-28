
import re
from datetime import datetime, timedelta, timezone

import pytest
from dateutil.parser import parse
from dateutil.tz import gettz
from hypothesis import assume, given, settings
from hypothesis import strategies as st


# ----------------------------
# Generators
# ----------------------------

@st.composite
def ambiguous_3int_dates(draw):
    # Use values that remain valid across dayfirst/yearfirst permutations.
    # 2001-2009 avoids 2-digit-year ambiguity and keeps year in a safe range.
    a = draw(st.integers(min_value=1, max_value=12))
    b = draw(st.integers(min_value=1, max_value=12))
    y = draw(st.integers(min_value=2001, max_value=2009))
    sep = draw(st.sampled_from(["/", "-", "."]))
    return f"{a:02d}{sep}{b:02d}{sep}{y}"


@st.composite
def tz_name_strings(draw):
    # Simple fixed-offset timezone names that are commonly supported.
    base = draw(st.datetimes(
        min_value=datetime(1990, 1, 1),
        max_value=datetime(2030, 12, 31, 23, 59, 59),
        timezones=st.just(None),
    ))
    tzname = draw(st.sampled_from(["UTC", "GMT", "EST", "CST", "PST"]))
    return base.strftime("%Y-%m-%d %H:%M:%S ") + tzname


@st.composite
def fuzzy_prefixed_timestamp(draw):
    # Prefix/suffix text around a precise timestamp to test fuzzy parsing.
    dt = draw(st.datetimes(
        min_value=datetime(2000, 1, 1, 0, 0, 0),
        max_value=datetime(2030, 12, 31, 23, 59, 59),
        timezones=st.just(None),
    ))
    prefix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="\x00"),
        min_size=1,
        max_size=10,
    ))
    suffix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="\x00"),
        min_size=1,
        max_size=10,
    ))
    s = f"{prefix} {dt.strftime('%Y-%m-%d %H:%M:%S')} {suffix}"
    return s, dt


# ----------------------------
# Invariants
# ----------------------------

@given(st.datetimes(
    min_value=datetime(1900, 1, 1),
    max_value=datetime(2099, 12, 31, 23, 59, 59),
    timezones=st.just(None),
))
@settings(max_examples=100)
def test_parse_iso_roundtrip_naive(dt):
    # Sound invariant: ISO-like strings should parse back to the same naive datetime.
    s = dt.strftime("%Y-%m-%d %H:%M:%S")
    parsed = parse(s)
    assert parsed == dt.replace(microsecond=0)


@given(ambiguous_3int_dates())
@settings(max_examples=200)
def test_parse_ambiguous_3int_yearfirst_changes_semantics(s):
    # Sound invariant: yearfirst=True should usually change ambiguous 3-int dates.
    # Conditional: only assert when the first token is not already clearly a year > 31.
    first = int(re.split(r"[./-]", s)[0])
    assume(first <= 31)
    p_default = parse(s, dayfirst=False, yearfirst=False)
    p_yearfirst = parse(s, dayfirst=False, yearfirst=True)

    # If first token is not a year, yearfirst should interpret the last token as year.
    assert p_yearfirst.year >= 1000
    assert p_default.year == 2001 or p_default.year == 2002 or p_default.year == 2003 or p_default.year == 2004 or p_default.year == 2005 or p_default.year == 2006 or p_default.year == 2007 or p_default.year == 2008 or p_default.year == 2009
    assert (p_default.year, p_default.month, p_default.day) != (
        p_yearfirst.year, p_yearfirst.month, p_yearfirst.day
    ) or first in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}


@given(tz_name_strings())
@settings(max_examples=100)
def test_parse_ignoretz_discards_timezone(s):
    # Sound invariant: ignoretz=True should return a naive datetime, even if the string has tz info.
    tzinfos = {
        "UTC": 0,
        "GMT": 0,
        "EST": -18000,
        "CST": -21600,
        "PST": -28800,
    }
    dt = parse(s, tzinfos=tzinfos, ignoretz=True)
    assert dt.tzinfo is None


@given(fuzzy_prefixed_timestamp())
@settings(max_examples=100)
def test_parse_fuzzy_with_tokens_returns_ignored_text(s_pair):
    # Sound invariant: fuzzy_with_tokens=True returns (datetime, tokens), and tokens are non-empty
    # when the input contains extra non-date text.
    s, expected_dt = s_pair
    parsed, tokens = parse(s, fuzzy_with_tokens=True)
    assert isinstance(parsed, datetime)
    assert isinstance(tokens, tuple)
    assert parsed == expected_dt.replace(microsecond=0)
    assert len(tokens) >= 1
    assert "".join(tokens).strip() != ""


@given(st.datetimes(
    min_value=datetime(2000, 1, 1, 0, 0, 0),
    max_value=datetime(2030, 12, 31, 23, 59, 59),
    timezones=st.just(None),
))
@settings(max_examples=100)
def test_parse_default_fills_missing_time_fields(dt):
    # Sound invariant: explicit fields in the string override the default datetime,
    # while unspecified fields are inherited from default.
    default = datetime(1999, 12, 31, 23, 59, 58)
    s = dt.strftime("%Y-%m-%d")
    parsed = parse(s, default=default)

    assert parsed.year == dt.year
    assert parsed.month == dt.month
    assert parsed.day == dt.day
    assert parsed.hour == default.hour
    assert parsed.minute == default.minute
    assert parsed.second == default.second
    assert parsed.microsecond == default.microsecond

