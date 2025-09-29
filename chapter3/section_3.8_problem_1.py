# Problem: Define token rules for identifiers, numbers, operators, and keywords.
# The program should generate a scanner using regex patterns.

import re

rules = [
    ("NUMBER",   r"\d+"),
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("MUL",      r"\*"),
    ("DIV",      r"/"),
    ("ASSIGN",   r"="),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("SKIP",     r"[ \t\n]+"),
    ("MISMATCH", r".")
]

def lex_generator(code):
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in rules)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            print(f"Error: Unexpected token {value}")
        else:
            print(f"{value} --> {kind}")

# Example usage:
lex_generator("x = 25 + (y - 3) * z")
