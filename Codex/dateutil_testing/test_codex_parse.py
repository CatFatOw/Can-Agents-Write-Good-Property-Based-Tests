from datetime import datetime, timedelta
from pathlib import Path
import sys

from dateutil import parser
from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Properties used for dateutil.parser.parse:
# 1. Successfully parsed strings return a datetime.datetime object.
# 2. Explicit date and time components in unambiguous strings are preserved.
# 3. Missing components are copied from the supplied default datetime.
# 4. dayfirst and yearfirst control how ambiguous three-integer dates are read.
# 5. fuzzy_with_tokens returns the parsed datetime plus the ignored text tokens.


MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def _format_offset(hours, minutes, separator):
    sign = "+" if hours >= 0 else "-"
    return f"{sign}{abs(hours):02d}{separator}{minutes:02d}"


# Summary: Generate bounded, valid date strings in several documented parse
# styles: explicit numeric and month-name datetimes, strings with omitted fields
# and a fixed default, ambiguous numeric dates with dayfirst/yearfirst flags,
# fuzzy text with ignored tokens, and numeric timezone offsets. The strategy
# avoids huge values by keeping years inside datetime's normal range and by
# drawing valid datetimes directly.
@given(st.data())
def test_parse(data):
    scenario = data.draw(
        st.sampled_from(
            [
                "complete_datetime",
                "missing_default_fields",
                "ambiguous_flags",
                "fuzzy_with_tokens",
                "numeric_timezone",
            ]
        )
    )

    if scenario == "complete_datetime":
        value = data.draw(
            st.datetimes(
                min_value=datetime(1000, 1, 1),
                max_value=datetime(9999, 12, 31, 23, 59, 59, 999999),
                timezones=st.none(),
            )
        )
        style = data.draw(st.sampled_from(["iso", "slash", "month_name"]))

        if style == "iso":
            date_string = value.strftime("%Y-%m-%d %H:%M:%S")
        elif style == "slash":
            date_string = value.strftime("%m/%d/%Y %H:%M:%S")
        else:
            month = MONTH_NAMES[value.month - 1]
            date_string = f"{month} {value.day}, {value.year} {value:%H:%M:%S}"

        if value.microsecond:
            date_string += f".{value.microsecond:06d}"

        result = parser.parse(date_string)

        assert isinstance(result, datetime)
        assert result == value

    elif scenario == "missing_default_fields":
        default = data.draw(
            st.datetimes(
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2099, 12, 28, 23, 59, 59, 999999),
                timezones=st.none(),
            )
        )
        month = data.draw(st.integers(min_value=1, max_value=12))
        day = data.draw(st.integers(min_value=1, max_value=28))
        hour = data.draw(st.integers(min_value=0, max_value=23))
        minute = data.draw(st.integers(min_value=0, max_value=59))
        variant = data.draw(st.sampled_from(["month_day", "time_only"]))

        if variant == "month_day":
            date_string = f"{MONTH_NAMES[month - 1]} {day}"
            result = parser.parse(date_string, default=default)

            assert isinstance(result, datetime)
            assert result.year == default.year
            assert result.month == month
            assert result.day == day
            assert result.hour == default.hour
            assert result.minute == default.minute
            assert result.second == default.second
            assert result.microsecond == default.microsecond
        else:
            date_string = f"{hour:02d}:{minute:02d}"
            result = parser.parse(date_string, default=default)

            assert isinstance(result, datetime)
            assert result.year == default.year
            assert result.month == default.month
            assert result.day == default.day
            assert result.hour == hour
            assert result.minute == minute
            assert result.second == default.second
            assert result.microsecond == default.microsecond

    elif scenario == "ambiguous_flags":
        first = data.draw(st.integers(min_value=1, max_value=12))
        second = data.draw(st.integers(min_value=1, max_value=12))
        year = data.draw(st.integers(min_value=1900, max_value=2099))
        default = datetime(2000, 1, 1)
        date_string = f"{first:02d}/{second:02d}/{year:04d}"

        result_month_first = parser.parse(
            date_string,
            dayfirst=False,
            yearfirst=False,
            default=default,
        )
        result_day_first = parser.parse(
            date_string,
            dayfirst=True,
            yearfirst=False,
            default=default,
        )
        yearfirst_day = data.draw(st.integers(min_value=1, max_value=28))
        yearfirst_string = f"{year:04d}/{first:02d}/{yearfirst_day:02d}"
        result_year_first = parser.parse(
            yearfirst_string,
            dayfirst=False,
            yearfirst=True,
            default=default,
        )

        assert isinstance(result_month_first, datetime)
        assert result_month_first.month == first
        assert result_month_first.day == second
        assert result_month_first.year == year

        assert isinstance(result_day_first, datetime)
        assert result_day_first.month == second
        assert result_day_first.day == first
        assert result_day_first.year == year

        assert isinstance(result_year_first, datetime)
        assert result_year_first.year == year
        assert result_year_first.month == first
        assert result_year_first.day == yearfirst_day

    elif scenario == "fuzzy_with_tokens":
        value = data.draw(
            st.datetimes(
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2099, 12, 31, 23, 59, 59),
                timezones=st.none(),
            )
        ).replace(microsecond=0)
        prefix = data.draw(st.sampled_from(["abc ", "recorded ", "note "]))
        suffix = data.draw(st.sampled_from([" xyz", " done", " approx"]))
        date_string = f"{prefix}{value:%Y-%m-%d %H:%M:%S}{suffix}"

        result, tokens = parser.parse(date_string, fuzzy_with_tokens=True)

        assert isinstance(result, datetime)
        assert result == value
        assert prefix in tokens
        assert suffix in tokens

    else:
        value = data.draw(
            st.datetimes(
                min_value=datetime(1900, 1, 1),
                max_value=datetime(2099, 12, 31, 23, 59, 59),
                timezones=st.none(),
            )
        ).replace(microsecond=0)
        offset_hour = data.draw(
            st.integers(min_value=-23, max_value=23).filter(lambda hour: hour != 0)
        )
        offset_minute = data.draw(st.integers(min_value=0, max_value=59))
        separator = data.draw(st.sampled_from(["", ":"]))
        offset = _format_offset(offset_hour, offset_minute, separator)
        date_string = f"{value:%Y-%m-%d %H:%M:%S} {offset}"

        result = parser.parse(date_string)
        expected_offset = timedelta(
            hours=offset_hour,
            minutes=offset_minute if offset_hour > 0 else -offset_minute,
        )

        assert isinstance(result, datetime)
        assert result.replace(tzinfo=None) == value
        assert result.utcoffset() == expected_offset
# End program


if __name__ == "__main__":
    print(evaluate_test(test_parse))
