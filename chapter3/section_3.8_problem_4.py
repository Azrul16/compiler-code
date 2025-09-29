# Problem: Write a mini "Lex" generator in Python.
# Given a list of (token_name, regex) rules, produce a function that scans input.
import re
def generate_scanner(rules):
    regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in rules)
    
    def scanner(code):
        for match in re.finditer(regex, code):
            kind = match.lastgroup
            value = match.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                print(f"Error: Unexpected token {value}")
            else:
                print(f"{value} --> {kind}")
    return scanner

# Define rules
rules = [
    ("NUMBER",   r"\d+"),
    ("IDENT",    r"[a-zA-Z_]\w*"),
    ("PLUS",     r"\+"),
    ("MINUS",    r"-"),
    ("ASSIGN",   r"="),
    ("SKIP",     r"[ \t\n]+"),
    ("MISMATCH", r".")
]

# Generate scanner
my_scanner = generate_scanner(rules)

# Example usage:
my_scanner("x = 10 + y - 5")
