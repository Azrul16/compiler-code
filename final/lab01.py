import re

def lexical_analyzer(source_code):
    token_specification = [
        ('COMMENT',    r'//.*|/\*[\s\S]*?\*/'),
        ('WHITESPACE', r'[ \t]+'),
        ('NEWLINE',    r'\n'),
        ('IDENTIFIER', r'[A-Za-z_][A-Za-z_0-9]*'),
        ('CONSTANT',   r'\b\d+(\.\d+)?\b'),
        ('OPERATOR',   r'==|!=|<=|>=|&&|\|\||[\+\-\*/%=<>!]'),
        ('DELIMITER',  r'[;,{}()\[\]]'),
        ('STRING',     r'"[^"\n]*"'),
        ('CHAR',       r"'.'"),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).finditer

    for match in get_token(source_code):
        kind = match.lastgroup
        value = match.group()
        if kind == "WHITESPACE" or kind == "NEWLINE":
            continue
        print(f"{kind}: {value}")

# Example usage
source_code = '''
int main() {
    // Comment
    int a = 10;
    float b = 3.14;
    /* Multiline
       comment */
    if (a > b) a = a + 1;
    printf("Value: %d", a);
}
'''
print("Lab01: Lexical Analyzer Output")
lexical_analyzer(source_code)
print()
