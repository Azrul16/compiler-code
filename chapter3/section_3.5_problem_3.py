# Problem: Simulate Lex lookahead to differentiate "if" as a keyword 
# only when followed by space or symbol, not inside identifiers like "ifelse".

import re

rules = [
    ("IF",       r"if(?=\s|[^a-zA-Z0-9_])"),  # lookahead ensures "if" is whole word
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("NUMBER",   r"\d+"),
    ("OP",       r"[+\-*/=]"),
    ("WHITESPACE", r"[ \t\n]+"),
    ("MISMATCH", r".")
]

def lex_with_lookahead(code):
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
lex_with_lookahead("if else ifelse x=5")
