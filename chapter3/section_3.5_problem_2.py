# Problem: Simulate Lex's "longest match" behavior
# Example: "==" should be recognized as one operator, not two "=".
import re
rules = [
    ("EQ",       r"=="),
    ("ASSIGN",   r"="),
    ("PLUS",     r"\+"),
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("NUMBER",   r"\d+"),
    ("WHITESPACE", r"[ \t\n]+"),
    ("MISMATCH", r".")
]

def lex_longest_match(code):
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
lex_longest_match("x==10")
