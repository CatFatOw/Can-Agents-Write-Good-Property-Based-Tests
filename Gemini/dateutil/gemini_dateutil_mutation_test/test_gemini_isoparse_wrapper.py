from hypothesis import given, strategies as st
from dateutil.parser import isoparse
import dateutil.tz
import datetime
import sys, os
from pathlib import Path



PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))



# Summary: Dynamically generates structurally consistent basic or extended ISO-8601 strings to validate parsing invariants, precise component capturing, and UTC vs offset object classification.
@given(st.data())
def test_isoparse(data):
    # 1. Generate valid calendar components safely
    year = data.draw(st.integers(min_value=1, max_value=9999))
    month = data.draw(st.integers(min_value=1, max_value=12))
    day = data.draw(st.integers(min_value=1, max_value=28))  # Safe bound across all months
    
    date_style = data.draw(st.sampled_from(["YYYY", "YYYY-MM", "YYYY-MM-DD", "YYYYMMDD"]))
    
    if date_style == "YYYY":
        dt_str = f"{year:04d}"
    elif date_style == "YYYY-MM":
        dt_str = f"{year:04d}-{month:02d}"
    elif date_style == "YYYY-MM-DD":
        dt_str = f"{year:04d}-{month:02d}-{day:02d}"
    else:
        dt_str = f"{year:04d}{month:02d}{day:02d}"
        
    has_time = False
    has_tz = False
    is_utc = False
    time_style = None

    # 2. Append time components only to complete date specifications
    if date_style in ["YYYY-MM-DD", "YYYYMMDD"] and data.draw(st.booleans()):
        has_time = True
        hour = data.draw(st.integers(min_value=0, max_value=23))
        minute = data.draw(st.integers(min_value=0, max_value=59))
        second = data.draw(st.integers(min_value=0, max_value=59))
        microsecond = data.draw(st.integers(min_value=0, max_value=999999))
        
        # Guard against mixing basic and extended ISO formats
        if date_style == "YYYY-MM-DD":
            time_style = data.draw(st.sampled_from(["hh", "hh:mm", "hh:mm:ss", "hh:mm:ss.ssssss"]))
        else:
            time_style = data.draw(st.sampled_from(["hh", "hhmm", "hhmmss"]))
            
        dt_str += "T"
        if time_style == "hh":
            dt_str += f"{hour:02d}"
        elif time_style == "hh:mm":
            dt_str += f"{hour:02d}:{minute:02d}"
        elif time_style == "hhmm":
            dt_str += f"{hour:02d}{minute:02d}"
        elif time_style == "hh:mm:ss":
            dt_str += f"{hour:02d}:{minute:02d}:{second:02d}"
        elif time_style == "hhmmss":
            dt_str += f"{hour:02d}{minute:02d}{second:02d}"
        elif time_style == "hh:mm:ss.ssssss":
            sep = data.draw(st.sampled_from([".", ","]))
            dt_str += f"{hour:02d}:{minute:02d}:{second:02d}{sep}{microsecond:06d}"
            
        # 3. Append timezone specifications corresponding to structural choice
        if data.draw(st.booleans()):
            has_tz = True
            if date_style == "YYYY-MM-DD":
                tz_style = data.draw(st.sampled_from(["Z", "±HH", "±HH:MM"]))
            else:
                tz_style = data.draw(st.sampled_from(["Z", "±HH", "±HHMM"]))
                
            if tz_style == "Z":
                dt_str += "Z"
                is_utc = True
            else:
                sign = data.draw(st.sampled_from(["+", "-"]))
                tz_hour = data.draw(st.integers(min_value=0, max_value=23))
                tz_min = data.draw(st.integers(min_value=0, max_value=59))
                
                if tz_style == "±HH":
                    dt_str += f"{sign}{tz_hour:02d}"
                    is_utc = (tz_hour == 0)
                elif tz_style == "±HHMM":
                    dt_str += f"{sign}{tz_hour:02d}{tz_min:02d}"
                    is_utc = (tz_hour == 0 and tz_min == 0)
                elif tz_style == "±HH:MM":
                    dt_str += f"{sign}{tz_hour:02d}:{tz_min:02d}"
                    is_utc = (tz_hour == 0 and tz_min == 0)

    # Execution
    res = isoparse(dt_str)

    # Property 1: Type Invariant
    assert isinstance(res, datetime.datetime)
    assert res.year == year
    
    # Property 2 & 3: Calendar mapping and lowest-value defaults
    if date_style == "YYYY":
        assert res.month == 1
        assert res.day == 1
    elif date_style == "YYYY-MM":
        assert res.month == month
        assert res.day == 1
    else:
        assert res.month == month
        assert res.day == day
        
    # Property 3 (cont.): Time component defaults
    if not has_time:
        assert res.hour == 0
        assert res.minute == 0
        assert res.second == 0
        assert res.microsecond == 0
    else:
        assert res.hour == hour
        
        if time_style in ["hh:mm", "hhmm", "hh:mm:ss", "hhmmss", "hh:mm:ss.ssssss"]:
            assert res.minute == minute
        else:
            assert res.minute == 0
            
        if time_style in ["hh:mm:ss", "hhmmss", "hh:mm:ss.ssssss"]:
            assert res.second == second
        else:
            assert res.second == 0
            
        if time_style == "hh:mm:ss.ssssss":
            assert res.microsecond == microsecond
        else:
            assert res.microsecond == 0
            
    # Property 4: Accurate Timezone Classifications
    if has_tz:
        assert res.tzinfo is not None
        if is_utc:
            assert isinstance(res.tzinfo, dateutil.tz.tzutc)
        else:
            assert isinstance(res.tzinfo, dateutil.tz.tzoffset)
    else:
        assert res.tzinfo is None

# End program
