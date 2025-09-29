# Exercise 3.1.3:
# Write a Python program to detect lexical errors in an input string.
# Allowed tokens: identifiers, numbers, operators, separators, keywords.
# Any character outside this set is considered a lexical error.

import re

# Define allowed token patterns
token_specification = [
    ("KEYWORD",    r'\b(if|else|while|for|return|int|float|double|char|void)\b'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("NUMBER",     r'\b\d+(\.\d+)?\b'),
    ("OPERATOR",   r'==|!=|<=|>=|\+|\-|\*|/|=|<|>'),
    ("SEPARATOR",  r'[;,\(\)\{\}]'),
    ("WHITESPACE", r'\s+'),
]

# Build combined regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).finditer

def detect_lexical_errors(code):
    errors = []
    tokens = []
    index = 0
    while index < len(code):
        match = re.match(tok_regex, code[index:])
        if match:
            kind = match.lastgroup
            value = match.group()
            if kind != "WHITESPACE":
                tokens.append((value, kind))
            index += len(value)
        else:
            # Unknown/illegal character
            errors.append((code[index], index))
            index += 1
    return tokens, errors

# Example input (contains @ and $ which are invalid)
cpp_code = """
int main() {
    int x = 10;
    if (x == 10) {
        return x@ + $y;
    }
}
"""

tokens, errors = detect_lexical_errors(cpp_code)

print("Valid Tokens:")
for lexeme, token_type in tokens:
    print(f"{lexeme:10} -> {token_type}")

print("\nLexical Errors Found:")
for err, pos in errors:
    print(f"Illegal character '{err}' at position {pos}")
