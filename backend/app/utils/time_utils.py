# backend/app/utils/time_utils.py

from datetime import datetime
import pytz

def convert_to_timezone(dt: datetime, timezone: str) -> datetime:
    """
    Converts a datetime object to the specified timezone.
    """
    local_timezone = pytz.timezone(timezone)
    return dt.astimezone(local_timezone)

def str_to_datetime(date_str: str) -> datetime:
    """
    Converts a string to a datetime object.
    """
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
