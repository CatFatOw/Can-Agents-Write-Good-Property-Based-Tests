from hypothesis import given, settings, Verbosity, note
from hypothesis.strategies import integers, composite, lists, floats, booleans, sampled_from
import pytest,sys
from pathlib import Path
from dateutil import parser
from dateutil.parser import parse, ParserError
import random 
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from metrics import evaluate_test

# Human written property based testing

# -------------------TEST: dateutil.parser.parse()-----------------------------

# parser() accepts a huge variety of human-readable date/time formats. 
# parser.parse(parserinfo=None, **kwargs)
# The PBT generator will focus on: ISO style, Slash separated, natural lanauge, and weird spacings 

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
    

# Generate Slash separated dates 
@composite
def generate_slash_dates(draw):
    """Function generates dates in the format of month/day/year"""
    month = str(draw(integers(min_value=1, max_value=12))).zfill(2)
    
    year = "" 
    for _ in range(4):
        year += str(draw(integers(min_value=0, max_value=9)))
    
    if is_leap_year(int(year)) and month == "02":
        day = str(draw(integers(min_value=1, max_value=29))).zfill(2)
    else:
        month_day_mapping = {"01": "31", "02": "28", "03":"31", "04":"30", "05":"31", "06":"30", "07":"31", "08":"31", "09":"30", "10":"31", "11":"30", "12":"31"}
        day = str(draw(integers(min_value=1, max_value=int(month_day_mapping[month])))).zfill(2)

    # Induce some randomness (by adding spaces/text/etc)
    date = month + "/" + day + "/" + year
    #20% change
    induce_randomness = draw(integers(min_value=1, max_value=5))
    if induce_randomness == 1:
        # Add a random mutation character to random idx
        random_idx = draw(integers(min_value=0, max_value=len(date)-1))
        random_char = chr(draw(integers(min_value=32, max_value=32+32)))
        return date[:random_idx] + random_char + date[random_idx:]
    else:
        return date


# General structure generator for ISO format
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
        # Induce some randomness (by adding spaces/text/etc)
    date_time = date + "T" + time if time else date

    # 20% chance
    induce_randomness = draw(integers(min_value=1, max_value=5))

    if induce_randomness == 1:
        random_idx = draw(integers(min_value=0, max_value=len(date_time)))
        random_char = chr(draw(integers(min_value=32, max_value=64)))
        return date_time[:random_idx] + random_char + date_time[random_idx:]

    else:
        return date_time
    


# Generate natural language (only month)
@composite 
def generate_language_date(draw):
    """Function generates date that has month as human langauge form"""

    month_candidates = ["Jan", "January", "Feb", "February", "March", "Mar", "April", "Apr", "May", "June", "Jun", "July", "Jul", "August", "Aug", "September", "Sep", "October", "Oct", "November", "Nov", "December", "Dec"]
    month = draw(sampled_from(month_candidates))

    year = ""
    for _ in range(4):
        year += str(draw(integers(min_value=0, max_value=9)))

    # February depends on leap year
    if is_leap_year(int(year)) and month in ["Feb", "February"]:
        day = str(draw(integers(min_value=1, max_value=29))).zfill(2)

    else:
        month_day_mapping = {
            "Jan": "31", "January": "31",
            "Feb": "28", "February": "28",
            "March":"31", "Mar":"31",
            "April":"30", "Apr":"30",
            "May":"31",
            "June":"30", "Jun":"30",
            "July":"31", "Jul":"31",
            "August":"31", "Aug":"31",
            "September":"30", "Sep":"30",
            "October":"31", "Oct":"31",
            "November":"30", "Nov":"30",
            "December":"31", "Dec":"31"
        }

        day = str(
            draw(
                integers(
                    min_value=1,
                    max_value=int(month_day_mapping[month])
                )
            )
        ).zfill(2)

   
    # Choose which format to display the text in
    format_type = draw(sampled_from([
        "MDY",
        "DMY",
        "YMD"
    ]))

    if format_type == "MDY":
        date = month + "/" + day + "/" + year

    elif format_type == "DMY":
        date = day + "/" + month + "/" + year

    else:
        date = year + "/" + month + "/" + day
    
    # Induce 20% chance of extra char/mutation
    chance = draw(integers(min_value=1, max_value=5))

    if chance == 1:
        random_idx = draw(integers(min_value=0, max_value=len(date)))

        # ASCII printable-ish chars
        random_char = chr(
            draw(integers(min_value=32, max_value=64))
        )

        return (
            date[:random_idx]
            + random_char
            + date[random_idx:]
        )

    else:
        return date

        

# Combine then and random choose 
@composite 
def choose_generator(draw):
    """randomly picks a given strategy to generate data of datetime when called"""
    generators = [generate_slash_dates(), generate_date_time(), generate_language_date()]
    chosen_generator = draw(sampled_from(generators))
    output = draw(chosen_generator)
    return output



# -------------------------
# 2. Test for invariants
# -------------------------

# invariant 1: The parsed object is datetime object 


@given(choose_generator())
def test_datetime_obj(date_str):
    try:
        dt = parse(date_str)
        assert isinstance(dt, datetime)

    except ParserError:
        # Acceptable: parser rejected malformed input
        pass

# invariant 2: parse the same string twice should get same result
@given(choose_generator())
def test_deterministic(date_str):
    try:
        assert parse(date_str) == parse(date_str)
    except ParserError:
        # Parser rejected
        pass 

# Invariant 3:iso representation should stay the same  
@given(choose_generator())
def test_round_trip(date_str):
    # error here should be pt under try, but this counts
    dt = parse(date_str)
    try:

        reparsed = parse(dt.isoformat())

        assert reparsed == dt
    except ParserError:
        pass 




# Evaulate Soundness /validity
map1 = evaluate_test(test_datetime_obj)
map2 = evaluate_test(test_deterministic)
map3 = evaluate_test(test_round_trip)

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