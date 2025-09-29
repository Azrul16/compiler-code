# Exercise 3.1.1:
# Write a Python program to divide a C++ snippet into lexemes
# and assign lexical categories (token types).

import re

# Define token patterns
token_specification = [
    ("KEYWORD",    r'\b(if|else|while|for|return|int|float|double|char|void)\b'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("NUMBER",     r'\b\d+(\.\d+)?\b'),
    ("OPERATOR",   r'==|!=|<=|>=|\+|\-|\*|/|=|<|>'),
    ("SEPARATOR",  r'[;,\(\)\{\}]'),
    ("WHITESPACE", r'\s+'),
    ("UNKNOWN",    r'.'),  # catch-all for unexpected symbols
]

# Build combined regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).finditer

def lexer(code):
    tokens = []
    for match in get_token(code):
        kind = match.lastgroup
        value = match.group()
        if kind == "WHITESPACE":
            continue
        tokens.append((value, kind))
    return tokens

# Example C++ snippet
cpp_code = """
int main() {
    int x = 10;
    if (x == 10) {
        return x;
    }
}
"""

tokens = lexer(cpp_code)

print("Lexemes and their Token Types:")
for lexeme, token_type in tokens:
    print(f"{lexeme:10} -> {token_type}")
