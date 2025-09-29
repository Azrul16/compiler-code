# Exercise 3.1.2:
# Write a Python program to divide an HTML snippet into lexemes
# and assign lexical categories (token types).

import re

# Define token patterns
token_specification = [
    ("TAG_CLOSE",      r'</[a-zA-Z][a-zA-Z0-9]*\s*>'),  # e.g. </div>
    ("TAG_OPEN",       r'<[a-zA-Z][a-zA-Z0-9]*\s*>'),   # e.g. <div>
    ("TAG_OPEN_ATTR",  r'<[a-zA-Z][a-zA-Z0-9]*'),       # start of tag with attributes
    ("TAG_END",        r'>'),                           # end of a tag
    ("ATTRIBUTE_NAME", r'\s+[a-zA-Z_:][a-zA-Z0-9_:.-]*'),
    ("EQUALS",         r'='),
    ("ATTRIBUTE_VALUE",r'"[^"]*"'),
    ("TEXT",           r'[^<>]+'),                      # text between tags
    ("WHITESPACE",     r'\s+'),                         # skip whitespace
]

# Build combined regex
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).finditer

def html_lexer(code):
    tokens = []
    for match in get_token(code):
        kind = match.lastgroup
        value = match.group().strip()
        if not value or kind == "WHITESPACE":
            continue
        tokens.append((value, kind))
    return tokens

# Example HTML snippet
html_code = """
<div class="header">
   Hello World!
   <p id="intro">Welcome</p>
</div>
"""

tokens = html_lexer(html_code)

print("Lexemes and their Token Types:")
for lexeme, token_type in tokens:
    print(f"{lexeme:15} -> {token_type}")
