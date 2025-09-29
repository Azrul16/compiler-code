# Exercise 3.3.2:
# Regex for binary numbers divisible by 2 (must end in 0).

import re

pattern = re.compile(r'^[01]*0$')

tests = ["0", "10", "110", "111", "10101", "1010"]

print("Binary Numbers Divisible by 2:")
for t in tests:
    print(f"{t:6} -> {'MATCH' if pattern.match(t) else 'NO MATCH'}")
