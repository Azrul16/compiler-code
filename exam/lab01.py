"""
Predictive Parser Implementation
Grammar:
    stmt    → expr ; | if ( expr ) stmt | for ( optexpr ; optexpr ) stmt | others
    expr    → (simplified for demonstration)
    optexpr → expr | ε (epsilon/empty)
"""

class ParserError(Exception):
    pass

class LexerStub:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.indent_level = 0
        
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
        
    def next(self):
        tok = self.peek()
        if tok is not None:
            self.pos += 1
        return tok
    
    def get_position(self):
        return f"position {self.pos}/{len(self.tokens)}"

class PredictiveParser:
    def __init__(self, lexer, debug=True):
        self.lexer = lexer
        self.debug = debug
        self.indent = 0
    
    def log(self, message):
        if self.debug:
            indent = "  " * self.indent
            print(f"{indent}{message}")
    
    def parse_stmt(self):
        tok = self.lexer.peek()
        self.log(f"Parsing statement at {self.lexer.get_position()}, next token: {tok}")
        self.indent += 1
        
        if tok == 'if':
            self.log("Found 'if' statement")
            self.lexer.next()  # consume 'if'
            self._expect('(')
            self.log("Parsing if condition expression:")
            self.parse_expr()
            self._expect(')')
            self.log("Parsing if body statement:")
            self.parse_stmt()
            
        elif tok == 'for':
            self.log("Found 'for' statement")
            self.lexer.next()  # consume 'for'
            self._expect('(')
            self.log("Parsing for initialization:")
            self.parse_optexpr()
            self._expect(';')
            self.log("Parsing for condition:")
            self.parse_optexpr()
            self._expect(')')
            self.log("Parsing for body statement:")
            self.parse_stmt()
            
        elif tok == 'others':
            self.log("Found 'others' statement")
            self.lexer.next()  # consume 'others'
            
        else:
            self.log("Found expression statement")
            self.parse_expr()
            self._expect(';')
        
        self.indent -= 1
        self.log("Statement completed")

    def parse_expr(self):
        tok = self.lexer.next()
        if tok is None or tok in {';', ')'}:
            raise ParserError(f'Expected expression, got {tok}')
        self.log(f"Parsed expression token: {tok}")

    def parse_optexpr(self):
        tok = self.lexer.peek()
        if tok != ';' and tok != ')':
            self.log("Found non-empty optional expression")
            self.parse_expr()
        else:
            self.log(f"Found empty optional expression (ε) at {tok}")

    def _expect(self, expected):
        tok = self.lexer.next()
        if tok != expected:
            raise ParserError(f'Expected {expected}, got {tok}')
        self.log(f"Matched expected token: {expected}")

def test_parser(tokens, description):
    print("\n" + "="*60)
    print(f"Test Case: {description}")
    print("Tokens:", tokens)
    print("-"*60)
    
    lexer = LexerStub(tokens)
    parser = PredictiveParser(lexer)
    try:
        parser.parse_stmt()
        print("\nParse Result: Success!")
    except ParserError as e:
        print(f"\nParse Result: Error - {e}")

if __name__ == '__main__':
    print("Predictive Parser Demonstration")
    print("Grammar:")
    print("  stmt    → expr ; | if ( expr ) stmt | for ( optexpr ; optexpr ) stmt | others")
    print("  expr    → (simplified for demonstration)")
    print("  optexpr → expr | ε")
    
    # Test cases - limited to 2 representative examples
    test_cases = [
        (
            ['if', '(', 'expr', ')', 'expr', ';'],
            "Test Case 1: If statement with expression body"
        ),
        (
            ['for', '(', 'x', ';', 'y', ')', 'others'],
            "Test Case 2: For loop with initialization and condition"
        )
    ]
    
    for tokens, description in test_cases:
        test_parser(tokens, description)
