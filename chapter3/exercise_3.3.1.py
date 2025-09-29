# Exercise 3.3.1:
# Write Python regex patterns for common token classes
# and test them on sample strings.

import re

token_specification = [
    ("KEYWORD",    r'^(if|else|while|for|return|int|float|double|char|void)$'),
    ("IDENTIFIER", r'^[a-zA-Z_][a-zA-Z0-9_]*$'),
    ("INTEGER",    r'^[0-9]+$'),
    ("FLOAT",      r'^[0-9]+\.[0-9]+$'),
    ("OPERATOR",   r'^(==|!=|<=|>=|\+|\-|\*|/|=|<|>)$'),
    ("SEPARATOR",  r'^[;,\(\)\{\}]$')
]

def classify_lexeme(lexeme):
    for token, pattern in token_specification:
        if re.match(pattern, lexeme):
            return token
    return "UNKNOWN"

# Test cases
test_lexemes = ["if", "counter", "123", "45.67", "==", ";", "9abc"]

print("Lexeme Classification:")
for lex in test_lexemes:
    print(f"{lex:10} -> {classify_lexeme(lex)}")
