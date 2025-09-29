# Problem: Simulate Lex by defining token rules and generating a scanner.
# The scanner should recognize identifiers, numbers, operators, and whitespace.

import re

rules = [
    ("NUMBER",   r"\d+"),
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("OP",       r"[+\-*/=]"),
    ("WHITESPACE", r"[ \t\n]+"),
    ("MISMATCH", r".")
]

def lex_scanner(code):
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in rules)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "WHITESPACE":
            continue
        elif kind == "MISMATCH":
            print(f"Error: Unexpected token {value}")
        else:
            print(f"{value} --> {kind}")

# Example usage:
lex_scanner("sum = a1 + 25 * x")
