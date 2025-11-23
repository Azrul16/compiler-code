import re

def lexical_analyzer(code):

    # Define token patterns
    keywords = {'int', 'float', 'char', 'double', 'if', 'else', 'while', 
                'for', 'return', 'void', 'main', 'printf', 'scanf'}
    
    # Token patterns (order matters!)
    token_patterns = [
        ('COMMENT_MULTI', r'/\*.*?\*/'),
        ('COMMENT_SINGLE', r'//.*'),
        ('KEYWORD', r'\b(' + '|'.join(keywords) + r')\b'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('CONSTANT', r'\d+\.?\d*'),
        ('STRING', r'"[^"]*"'),
        ('OPERATOR', r'[+\-*/%=<>!&|]+'),
        ('PUNCTUATION', r'[;,(){}[\]]'),
        ('WHITESPACE', r'[ \t]+'),
        ('NEWLINE', r'\n'),
    ]
    
    # Combine patterns
    master_pattern = '|'.join(f'(?P<{name}>{pattern})' 
                              for name, pattern in token_patterns)
    
    tokens = []
    for match in re.finditer(master_pattern, code):
        token_type = match.lastgroup
        token_value = match.group()
        
        # Skip whitespace and newlines in output (but we recognize them)
        if token_type not in ['WHITESPACE', 'NEWLINE']:
            tokens.append((token_type, token_value))
    
    return tokens


test_code = """

    int sum = a+b* 10;

"""

tokens = lexical_analyzer(test_code)
for token_type, token_value in tokens:
    print(f"{token_type:15} : {token_value}")

print()