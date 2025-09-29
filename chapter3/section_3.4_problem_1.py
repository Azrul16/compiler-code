# Problem: Write a program that reads an input string and identifies 
# whether each token is an identifier, a number, or invalid.
# (Identifiers start with a letter and can contain letters/digits/underscores.
# Numbers are sequences of digits.)

import re

def recognize_tokens(text):
    tokens = text.split()
    for token in tokens:
        if re.fullmatch(r"[a-zA-Z_]\w*", token):
            print(f"{token} --> Identifier")
        elif re.fullmatch(r"\d+", token):
            print(f"{token} --> Number")
        else:
            print(f"{token} --> Invalid token")

# Example usage:
input_str = "count x1 123 9abc _var"
recognize_tokens(input_str)
