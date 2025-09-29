# Exercise 3.3.4:
# Regex for floating-point numbers (with optional exponent).
import re
pattern = re.compile(r'^[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?$')

tests = ["3.14", "0.001", "2.5e10", "4.5E-3", "42", "abc"]

print("Floating-Point Numbers:")
for t in tests:
    print(f"{t:10} -> {'MATCH' if pattern.match(t) else 'NO MATCH'}")
