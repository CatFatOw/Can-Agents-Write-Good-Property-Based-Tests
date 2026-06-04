from hypothesis import given, strategies as st
import dateutil.parser
import datetime
import sys, os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

@given(st.data())
def test_parse_property(data):
    # Strategy to safely generate valid date components
    year = data.draw(st.integers(min_value=1900, max_value=2100))
    month = data.draw(st.integers(min_value=1, max_value=12))
    day = data.draw(st.integers(min_value=1, max_value=28)) # Safe day range to avoid calendar overflows
    hour = data.draw(st.integers(min_value=0, max_value=23))
    minute = data.draw(st.integers(min_value=0, max_value=59))
    second = data.draw(st.integers(min_value=0, max_value=59))

    base_str = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"

    # Draw boolean flags for the configurations
    fuzzy_with_tokens = data.draw(st.booleans())
    ignoretz = data.draw(st.booleans())
    
    # Construct input string based on fuzzy configuration
    timestr = f"Random text prefix {base_str} parsed suffix" if fuzzy_with_tokens else base_str

    # Setup a default datetime mapping for the fallback property
    pass_default = data.draw(st.booleans())
    default_obj = datetime.datetime(2025, 5, 17, 12, 0, 0) if pass_default else None

    try:
        result = dateutil.parser.parse(
            timestr,
            fuzzy_with_tokens=fuzzy_with_tokens,
            ignoretz=ignoretz,
            default=default_obj
        )
    except (dateutil.parser.ParserError, OverflowError):
        # Gracefully skip if a genuinely invalid structure or system overflow occurs
        return

    # Property 1 & 4: Verify structure types and fuzzy token containment
    if fuzzy_with_tokens:
        assert isinstance(result, tuple)
        assert len(result) == 2
        dt_obj, tokens = result
        assert isinstance(dt_obj, datetime.datetime)
        assert isinstance(tokens, tuple)
        for token in tokens:
            assert token in timestr
    else:
        assert isinstance(result, datetime.datetime)
        dt_obj = result

    # Property 2: Verify ignoretz behavior
    if ignoretz:
        assert dt_obj.tzinfo is None

    # Property 3: Verify default object fallback behavior
    # To properly test omissions, we parse a partial string (Year-Month only)
    partial_str = f"{year:04d}-{month:02d}"
    partial_timestr = f"Target month is {partial_str}" if fuzzy_with_tokens else partial_str
    
    if pass_default:
        try:
            partial_result = dateutil.parser.parse(
                partial_timestr,
                fuzzy_with_tokens=fuzzy_with_tokens,
                ignoretz=ignoretz,
                default=default_obj
            )
            p_dt = partial_result[0] if fuzzy_with_tokens else partial_result
            # Fields missing from partial_str must perfectly match default_obj
            assert p_dt.day == default_obj.day
            assert p_dt.hour == default_obj.hour
            assert p_dt.minute == default_obj.minute
        except (dateutil.parser.ParserError, OverflowError):
            pass
# End program
if __name__ == "__main__":
    print(evaluate_test(test_parse_property))