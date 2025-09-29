# Exercise 3.1.4:
# Implement panic-mode lexical error recovery.
# Illegal characters are reported, replaced with an ERROR token, and scanning continues.

import re

# Token patterns
token_specification = [
    ("KEYWORD",    r'\b(if|else|while|for|return|int|float|double|char|void)\b'),
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("NUMBER",     r'\b\d+(\.\d+)?\b'),
    ("OPERATOR",   r'==|!=|<=|>=|\+|\-|\*|/|=|<|>'),
    ("SEPARATOR",  r'[;,\(\)\{\}]'),
    ("WHITESPACE", r'\s+'),
]

# Combined regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).finditer

def panic_mode_lexer(code):
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
            # Panic-mode recovery: skip one char, mark error
            tokens.append((code[index], "ERROR"))
            index += 1
    return tokens

# Example with lexical errors
cpp_code = """
int main() {
    int x = 10;
    if (x == 10) {
        return x@ + $y;  // '@' and '$' invalid
    }
}
"""

tokens = panic_mode_lexer(cpp_code)

print("Tokens (with error recovery):")
for lexeme, token_type in tokens:
    print(f"{lexeme:10} -> {token_type}")
