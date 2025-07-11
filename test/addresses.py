import re

def extract_addresses(itinerary_text):
    day_addrs = {}
    pattern = re.compile(r'^#?Day\s+(\d+):.*\|\s*Addresses:\s*(.+)$')
    for line in itinerary_text.splitlines():
        m = pattern.match(line)
        if not m:
            continue
        day = int(m.group(1))
        addrs = [a.strip() for a in m.group(2).split(';') if a.strip()]
        day_addrs[day] = addrs
    return day_addrs

text = """
#Day 1: Morning museum tour | Addresses: 100 Museum Way, Cityville; 200 Art St, Cityville
#Day 2: Hiking the hills | Addresses: 45 Trail Rd, Cityville
"""
print(extract_addresses(text))
