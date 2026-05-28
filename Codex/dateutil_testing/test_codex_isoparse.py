from datetime import date, datetime, timedelta
from pathlib import Path
import sys

from dateutil import parser, tz
from hypothesis import given, strategies as st


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test


# Properties used for dateutil.parser.isoparse:
# 1. The return value is a datetime.datetime.
# 2. Unspecified date and time components default to their lowest values.
# 3. Calendar and ISO week dates parse to the corresponding Gregorian date.
# 4. Provided time fields, including fractional seconds, are reflected in the output.
# 5. UTC offsets produce the documented tzinfo, with zero offsets normalized to tzutc.


def _max_iso_week(year):
    return date(year, 12, 28).isocalendar().week


def _format_offset(hours, minutes, style):
    sign = "+" if hours >= 0 else "-"
    abs_hours = abs(hours)
    if style == "hh":
        return f"{sign}{abs_hours:02d}"
    if style == "hhmm":
        return f"{sign}{abs_hours:02d}{minutes:02d}"
    return f"{sign}{abs_hours:02d}:{minutes:02d}"


# Summary: Generate valid ISO-8601 date strings across documented calendar and
# week formats, optionally adding documented time and timezone forms only when
# the date is complete. Bounded years and fixed-width numeric fields avoid
# oversized inputs while still covering edge cases like 24:00, comma fractions,
# compact dates, UTC aliases, and non-zero offsets.
@given(st.data())
def test_isoparse(data):
    year = data.draw(st.integers(min_value=1, max_value=9998))
    date_style = data.draw(
        st.sampled_from(
            [
                "year",
                "year_month",
                "calendar_extended",
                "calendar_compact",
                "week_extended",
                "week_compact",
            ]
        )
    )

    can_have_time = False
    expected_year = year
    expected_month = 1
    expected_day = 1

    if date_style == "year":
        date_string = f"{year:04d}"
    elif date_style == "year_month":
        expected_month = data.draw(st.integers(min_value=1, max_value=12))
        date_string = f"{year:04d}-{expected_month:02d}"
    elif date_style in {"calendar_extended", "calendar_compact"}:
        start = date(year, 1, 1)
        selected_date = start + timedelta(
            days=data.draw(st.integers(min_value=0, max_value=364 + int(_is_leap(year))))
        )
        expected_year = selected_date.year
        expected_month = selected_date.month
        expected_day = selected_date.day
        if date_style == "calendar_extended":
            date_string = selected_date.isoformat()
        else:
            date_string = selected_date.strftime("%Y%m%d")
        can_have_time = True
    else:
        week = data.draw(st.integers(min_value=1, max_value=_max_iso_week(year)))
        day = data.draw(st.integers(min_value=1, max_value=7))
        selected_date = date.fromisocalendar(year, week, day)
        expected_year = selected_date.year
        expected_month = selected_date.month
        expected_day = selected_date.day
        if date_style == "week_extended":
            date_string = f"{year:04d}-W{week:02d}-{day}"
        else:
            date_string = f"{year:04d}W{week:02d}{day}"
        can_have_time = True

    expected_hour = 0
    expected_minute = 0
    expected_second = 0
    expected_microsecond = 0
    expected_tzinfo = None

    datetime_string = date_string
    add_time = can_have_time and data.draw(st.booleans())
    if add_time:
        hour = data.draw(st.integers(min_value=0, max_value=24))
        if hour == 24:
            minute = 0
            second = 0
            fraction_digits = ""
            time_style = data.draw(st.sampled_from(["hour", "hour_minute"]))
        else:
            minute = data.draw(st.integers(min_value=0, max_value=59))
            second = data.draw(st.integers(min_value=0, max_value=59))
            fraction_digits = data.draw(
                st.text(
                    alphabet=st.characters(min_codepoint=48, max_codepoint=57),
                    min_size=0,
                    max_size=6,
                )
            )
            time_style = data.draw(
                st.sampled_from(
                    [
                        "hour",
                        "hour_minute",
                        "hour_minute_compact",
                        "second",
                        "second_compact",
                        "fraction_dot",
                        "fraction_comma",
                    ]
                )
            )

        if time_style == "hour":
            time_string = f"{hour:02d}"
        elif time_style == "hour_minute":
            time_string = f"{hour:02d}:{minute:02d}"
        elif time_style == "hour_minute_compact":
            time_string = f"{hour:02d}{minute:02d}"
        elif time_style == "second":
            time_string = f"{hour:02d}:{minute:02d}:{second:02d}"
        elif time_style == "second_compact":
            time_string = f"{hour:02d}{minute:02d}{second:02d}"
        else:
            separator = "." if time_style == "fraction_dot" else ","
            if not fraction_digits:
                fraction_digits = "0"
            time_string = f"{hour:02d}:{minute:02d}:{second:02d}{separator}{fraction_digits}"
            expected_microsecond = int(fraction_digits.ljust(6, "0"))

        datetime_string = f"{date_string}T{time_string}"

        if hour == 24:
            expected_date = date(expected_year, expected_month, expected_day) + timedelta(days=1)
            expected_year = expected_date.year
            expected_month = expected_date.month
            expected_day = expected_date.day
        else:
            expected_hour = hour
            if time_style not in {"hour"}:
                expected_minute = minute
            if time_style in {"second", "second_compact", "fraction_dot", "fraction_comma"}:
                expected_second = second

        if data.draw(st.booleans()):
            offset_style = data.draw(st.sampled_from(["Z", "zero", "nonzero"]))
            if offset_style == "Z":
                datetime_string += "Z"
                expected_tzinfo = tz.tzutc()
            elif offset_style == "zero":
                zero_form = data.draw(st.sampled_from(["+00", "+0000", "+00:00", "-00", "-0000", "-00:00"]))
                datetime_string += zero_form
                expected_tzinfo = tz.tzutc()
            else:
                offset_hour = data.draw(
                    st.integers(min_value=-23, max_value=23).filter(lambda value: value != 0)
                )
                offset_minute = data.draw(st.integers(min_value=0, max_value=59))
                style = data.draw(st.sampled_from(["hh", "hhmm", "hh:mm"]))
                datetime_string += _format_offset(offset_hour, offset_minute, style)
                parsed_offset_minute = 0 if style == "hh" else offset_minute
                total_seconds = (1 if offset_hour > 0 else -1) * (
                    abs(offset_hour) * 3600 + parsed_offset_minute * 60
                )
                expected_tzinfo = tz.tzoffset(None, total_seconds)

    result = parser.isoparse(datetime_string)

    assert isinstance(result, datetime)
    assert result.year == expected_year
    assert result.month == expected_month
    assert result.day == expected_day
    assert result.hour == expected_hour
    assert result.minute == expected_minute
    assert result.second == expected_second
    assert result.microsecond == expected_microsecond

    if expected_tzinfo is None:
        assert result.tzinfo is None
    else:
        assert result.tzinfo == expected_tzinfo
        assert result.utcoffset() == expected_tzinfo.utcoffset(result)
# End program


def _is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


if __name__ == "__main__":
    print(evaluate_test(test_isoparse))
