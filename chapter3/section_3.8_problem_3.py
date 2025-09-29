# Problem: Implement a DFA-based scanner for simple arithmetic expressions.
# DFA states are simulated by regex matching in this simplified version.
import re
def dfa_scanner(code):
    token_spec = [
        ("NUMBER",   r"\d+"),
        ("IDENT",    r"[a-zA-Z_]\w*"),
        ("OP",       r"[+\-*/=]"),
        ("LPAREN",   r"\("),
        ("RPAREN",   r"\)"),
        ("SKIP",     r"[ \t\n]+"),
        ("MISMATCH", r".")
    ]
    
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
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
dfa_scanner("result = a1 + 42 / (b - 3)")
