import re

def parse_time_left(time_text):
    """Extract total seconds from strings like '2h 5m 30s left'."""
    hours = minutes = seconds = 0

    # Match digits before optional whitespace and 'h', 'm', or 's'
    match_hours = re.search(r"(\d+)\s*h", time_text, re.IGNORECASE)
    match_minutes = re.search(r"(\d+)\s*m", time_text, re.IGNORECASE)
    match_seconds = re.search(r"(\d+)\s*s", time_text, re.IGNORECASE)

    if match_hours:
        hours = int(match_hours.group(1))
    if match_minutes:
        minutes = int(match_minutes.group(1))
    if match_seconds:
        seconds = int(match_seconds.group(1))

    return hours, minutes, seconds