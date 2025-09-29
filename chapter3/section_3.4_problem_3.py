# Problem: Write a lexical analyzer that splits an arithmetic expression 
# into tokens (numbers, identifiers, operators, parentheses).

import re

token_spec = [
    ("NUMBER",   r"\d+"),
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("OP",       r"[+\-*/=]"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("SKIP",     r"[ \t]+"),   # Skip spaces/tabs
    ("MISMATCH", r".")         # Any other character
]

def tokenize(code):
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            print(f"{value} --> Invalid")
        else:
            print(f"{value} --> {kind}")

# Example usage:
expr = "count + 42 * (x - y)"
tokenize(expr)
