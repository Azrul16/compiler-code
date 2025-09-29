# Problem: Extend the recognizer so that reserved words ("if", "else", "while") 
# are recognized separately from identifiers.

import re

KEYWORDS = {"if", "else", "while", "for", "return"}

def recognize_keywords(text):
    tokens = text.split()
    for token in tokens:
        if token in KEYWORDS:
            print(f"{token} --> Keyword")
        elif re.fullmatch(r"[a-zA-Z_]\w*", token):
            print(f"{token} --> Identifier")
        elif re.fullmatch(r"\d+", token):
            print(f"{token} --> Number")
        else:
            print(f"{token} --> Invalid")

# Example usage:
input_str = "if x else count 42 while return"
recognize_keywords(input_str)
