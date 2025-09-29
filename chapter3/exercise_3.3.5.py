# Exercise 3.3.5:
# Regex for C-style comments /* ... */
import re
pattern = re.compile(r'^/\*.*?\*/$', re.DOTALL)

tests = ["/* hello */", "/* multi\nline */", "notacomment"]

print("C-style Comment Matching:")
for t in tests:
    print(f"{t:20} -> {'MATCH' if pattern.match(t) else 'NO MATCH'}")
