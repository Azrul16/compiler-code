# Exercise 3.3.3:
# Regex for identifiers (start with letter/underscore, followed by letters/digits/underscores).

import re


pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

tests = ["var", "_temp1", "2cool", "hello_world", "while"]

print("Identifier Matching:")
for t in tests:
    print(f"{t:12} -> {'MATCH' if pattern.match(t) else 'NO MATCH'}")
