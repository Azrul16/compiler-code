# Problem: Simulate NFA-based pattern matching for token recognition.
# (Simplified example for identifiers and numbers)
import re
def match_identifier(s):
    return re.fullmatch(r"[a-zA-Z_]\w*", s) is not None

def match_number(s):
    return re.fullmatch(r"\d+", s) is not None

tokens = ["count", "x1", "123", "9abc", "_var"]
for t in tokens:
    if match_identifier(t):
        print(f"{t} --> IDENT")
    elif match_number(t):
        print(f"{t} --> NUMBER")
    else:
        print(f"{t} --> INVALID")
