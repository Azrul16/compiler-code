# Exercise 3.3.6:
# Regex for signed integers (+ or - optional).

import re
pattern = re.compile(r'^[+-]?[0-9]+$')

tests = ["123", "+456", "-789", "42a"]

print("Signed Integers:")
for t in tests:
    print(f"{t:6} -> {'MATCH' if pattern.match(t) else 'NO MATCH'}")
