from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import pytest,sys
from pathlib import Path
from dateutil import parser 
import random 

import dateutil
print(dateutil.__version__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------TEST: parser.isoparse()-----------------------------

# isoparse() converts ISO-8601 formatted date/time string into a Python datetime object.
# ISO-8601 format date/time: 2026-05-28, 2026-05-28T14:30:45, 2026-05-28T14:30:45-04:00 (w/timezone offset), 2026-05-28T14:30:45.123456(fractional time)
# General structure: YYYY-MM-DDTHH:MM:SS 
#YYYY = year, MM = month, DD = day, T separates date/time, HH = hour, MM = minute, SS = second#

# params: dt_str(string) a timetime string in the format of the general structure 


# Check if leap year
def is_leap_year(year):
    """Function checks if year is leap year
    
    PARAMS:
        year: (int)"""
    if year % 4 == 0 and year % 100 != 0:
        return True 

    elif year % 400 ==0 and year % 100 == 0:
        return True 
    else:
        return False


# General structure generator 
@composite 
def generate_date_time(draw):
    """This function generates time in the format of: YYYY-MM-DDTHH:MM:SS """

    # Year (0-9) x 4 so 10^4 combinations 
    year = "" 
    for _ in range(4):
        year += str(draw(integers(min_value=1, max_value=9)))
    
    # month is from 01-12
    month = str(draw(integers(min_value=1, max_value=11)))
    if month in set(map(str, range(0, 10))):
        month = "0" + month

    # day is more complicated due to leap year (accidently wrote a error here. keeping it for testing purposes)
    month_day_mapping = {"01": "31", "02": ["28", "29"], "03":"31", "04":"30", "05":"31", "06":"30", "07":"31", "08":"31", "09":"30", "10":"31", "11":"30", "12":"31"}

    if is_leap_year(int(year)) and month == "02":
        day = str(draw(sampled_from(list(range(1, 30))))).zfill(2)

    elif month == "02":
        day = str(draw(sampled_from(list(range(1, 29))))).zfill(2)

    else:
        day = str(draw(sampled_from(list(range(1, int(month_day_mapping[month]) + 1))))).zfill(2)

    date = year + "-" + month + "-" + day


    # now generate the Hours, minutes, and seconds, fractional, or nothing. To simulate randomness, we randomly choose which ones to generate
    to_generate = draw(integers(min_value=0, max_value=4))
    # Use switch/match (could have been more efficient)
    # HH:MM:SS 

    match to_generate:
        case 0:
            # We generate nothing
            time = "" 
    
        case 1:
            # We generate only hour
            time = ""
            hours = str(draw(integers(min_value=1, max_value=23)))
            if hours in set(map(str, range(0, 10))):
                hours = "0" + hours 
            time += hours 

        case 2:
            # Generate hour and minute 
            time = ""
            # Generate hours
            hours = str(draw(integers(min_value=1, max_value=23)))
            if hours in set(map(str, range(0, 10))):
                hours = "0" + hours 
            time += hours + ":" 
            # Generate minutes (0-60)
            minutes = str(draw(integers(min_value=1, max_value=59)))
            if minutes in set(map(str, range(1, 10))):
                minutes = "0" + minutes 
            time += minutes 

        case 3:
            # Generate hour, minue, and second
            time = ""
            # Generate hours
            hours = str(draw(integers(min_value=1, max_value=23)))
            if hours in set(map(str, range(0, 10))):
                hours = "0" + hours 
            time += hours + ":" 
            # Generate minutes (0-60)
            minutes = str(draw(integers(min_value=1, max_value=59)))
            if minutes in set(map(str, range(0, 10))):
                minutes = "0" + minutes 
            time += minutes + ":" 
            # Generate seconds 
            seconds = str(draw(integers(min_value=1, max_value=59)))
            if seconds in set(map(str, range(0, 10))):
                seconds = "0" + seconds 
            time += seconds

        case 4:
            # Generate hour, minue, and second, and microseconds
            time = ""
            # Generate hours
            hours = str(draw(integers(min_value=1, max_value=23)))
            if hours in set(map(str, range(0, 10))):
                hours = "0" + hours 
            time += hours + ":" 
            # Generate minutes (0-60)
            minutes = str(draw(integers(min_value=1, max_value=59)))
            if minutes in set(map(str, range(0, 10))):
                minutes = "0" + minutes 
            time += minutes + ":" 
            # Generate seconds 
            seconds = str(draw(integers(min_value=1, max_value=59)))
            if seconds in set(map(str, range(0, 10))):
                seconds = "0" + seconds 
            time += seconds
            # Generate microseconds 
            length = random.randint(1, 10)
            fractional_second = "."
            for _ in range(length):
                fractional_second += str(draw(integers(min_value=1, max_value=9)))
            time += fractional_second
            
    # End of matching

    # Combine together
    if time:
        return date + "T" + time 
    else:
        return date 

    

    
# -------------------------
# 2. Test for invariants
# -------------------------

# Invariant 1: parsed values matcn inputs
@given(generate_date_time())
@settings(print_blob=True, verbosity=Verbosity.verbose)
def test_split_len(date_str):
    dt = parser.isoparse(date_str)
    date_arr = date_str.split("T")
    date = date_arr[0]
    year, month, day = date.split("-")

    assert int(year) == dt.year 
    assert int(month) == dt.month
    assert int(day) == dt.day


# Invariant 2: if no datetiem is provided it defaults to midnight
@given(generate_date_time())
@settings(print_blob=True, verbosity=Verbosity.verbose)
def test_midnight(date_str):
    dt = parser.isoparse(date_str)
    date_arr = date_str.split("T")
    if len(date_arr) == 1:
        assert int(dt.hour) == 00
        assert int(dt.minute) == 00
        assert int(dt.second) == 00
    

# Invariant: if time included, parsed outputs must match 
@given(generate_date_time())
@settings(print_blob=True, verbosity=Verbosity.verbose)
def test_h_m_s(date_str):
    dt = parser.isoparse(date_str)
    date_arr = date_str.split("T")

    if len(date_arr) == 2:
        time_part = date_arr[-1]
        parts = time_part.split(":")

        # HH
        assert int(parts[0]) == dt.hour

        # HH:MM or HH:MM:SS
        if len(parts) >= 2:
            assert int(parts[1]) == dt.minute
        else:
            assert dt.minute == 0

        # HH:MM:SS or HH:MM:SS.microsecond
        if len(parts) >= 3:
            second_part = parts[2]

            if "." in second_part:
                second, micro_second = second_part.split(".")
                expected_micro = int(micro_second[:6].ljust(6, "0"))
            else:
                second = second_part
                expected_micro = 0

            assert int(second) == dt.second
            assert expected_micro == dt.microsecond
        else:
            assert dt.second == 0
            assert dt.microsecond == 0

# Evaulate Soundness /validity
map1 = evaluate_test(test_split_len)
map2 = evaluate_test(test_midnight)
map3 = evaluate_test(test_h_m_s)

results = [map1, map2, map3]

# Keep a single plotting-friendly dictionary:
# numeric fields are averaged across tests, and error fields are flattened.

total = {
    "validity": sum(result["validity"] for result in results) / len(results),
    "soundness": sum(result["soundness"] for result in results) / len(results),

    "validity_errors": set(
        error
        for result in results
        for error in result["validity_errors"]
    ),

    "soundness_errors": set(
        error
        for result in results
        for error in result["soundness_errors"]
    ),
}

print(total)