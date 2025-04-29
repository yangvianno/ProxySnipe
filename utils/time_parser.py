# time_parser.py

import re

def parse_time_left(time_text):
    """Extract total seconds from strings like '2h 5m 30s left'."""
    hours = minutes = seconds = 0

    # Match digits before optional whitespace and 'h', 'm', or 's'
    match_hours = re.search(r"(\d+)\s*h", time_text, re.IGNORECASE) # (\d+) get digit+ ;; \s* remove whitespace
    match_minutes = re.search(r"(\d+)\s*m", time_text, re.IGNORECASE) # re.IGNORECASE makes case-sensitive search matches both H & h
    match_seconds = re.search(r"(\d+)\s*s", time_text, re.IGNORECASE)
    
    # print("Full match:", match.group(0))  # ➜ '12h'
    # print("Captured digits:", match.group(1))  # ➜ '12'
    if match_hours: hours = int(match_hours.group(1)) # .group(..) is regex (regular expression) - data extractor
    if match_minutes: minutes = int(match_minutes.group(1))
    if match_seconds: seconds = int(match_seconds.group(1))

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return hours, minutes, seconds

# if (m := re.search(r"(\d+)\s*h", time_text, re.IGNORECASE)):
#       hours = int(m.group(1))