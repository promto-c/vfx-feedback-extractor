import re

s = "SHT010_101_123_comp_service_any_key_v001"
pattern = r"([A-Za-z0-9_]+?)_(.*?)(v\d+)$"
match = re.search(pattern, s)

if match:
    print("Shot: ", match.group(1))
    print("Service: ", match.group(2).rstrip('_'))
    print("Version: ", match.group(3))
else:
    print("No match found.")
