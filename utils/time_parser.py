# time_parser.py

import re

def parse_time_left(time_text):
    """
    Parses eBay's 'Ends in 3d 14h 5m 10s' into (d, h, m, s, total_seconds).
    Supports any mix of d/h/m/s.
    """
    days = hours = minutes = seconds = 0

    # Match digits before optional whitespace and 'd', 'h', 'm', or 's'
    match_days = re.search(r"(\d+)\s*d", time_text, re.IGNORECASE)
    match_hours = re.search(r"(\d+)\s*h", time_text, re.IGNORECASE) # (\d+) get digit+ ;; \s* remove whitespace
    match_minutes = re.search(r"(\d+)\s*m", time_text, re.IGNORECASE) # re.IGNORECASE makes case-sensitive search matches both H & h
    match_seconds = re.search(r"(\d+)\s*s", time_text, re.IGNORECASE)
    
    # print("Full match:", match.group(0))  # ➜ '12h'
    # print("Captured digits:", match.group(1))  # ➜ '12'
    if match_days: days = int(match_days.group(1))
    if match_hours: hours = int(match_hours.group(1)) # .group(..) is regex (regular expression) - data extractor
    if match_minutes: minutes = int(match_minutes.group(1))
    if match_seconds: seconds = int(match_seconds.group(1))

    total_seconds = days * 86400+ hours * 3600 + minutes * 60 + seconds
    return days, hours, minutes, seconds, total_seconds

# if (m := re.search(r"(\d+)\s*h", time_text, re.IGNORECASE)):
#       hours = int(m.group(1))