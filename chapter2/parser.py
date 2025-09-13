"""
Predictive Parser Implementation

Recursive-descent parser that uses lookahead to determine
which production to apply. Implements infix to postfix translation.
"""

from lexer import Lexer
import tag_constants

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = self.lexer.scan()
    
    def match(self, expected_tag):
        if self.lookahead.tag == expected_tag:
            self.lookahead = self.lexer.scan()
        else:
            raise SyntaxError(f"Expected {expected_tag}, got {self.lookahead.tag}")
    
    def expr(self):
        self.term()
        self.rest()
    
    def rest(self):
        while True:
            if self.lookahead.tag == ord('+'):
                self.match(ord('+'))
                self.term()
                print('+', end='')
            elif self.lookahead.tag == ord('-'):
                self.match(ord('-'))
                self.term()
                print('-', end='')
            else:
                break
    
    def term(self):
        if self.lookahead.tag == tag_constants.Tag.NUM:
            print(self.lookahead.value, end='')
            self.match(tag_constants.Tag.NUM)
        else:
            raise SyntaxError("Expected number")

if __name__ == "__main__":
    print("Testing Predictive Parser:")
    print("=" * 50)
    
    test_cases = [
        "9-5+2",
        "3+4-1", 
        "7",
    ]
    
    for test_input in test_cases:
        print(f"\nInput: '{test_input}'")
        print("Postfix output: ", end='')
        
        try:
            lexer = Lexer(test_input)
            parser = Parser(lexer)
            parser.expr()
            print()
        except Exception as e:
            print(f"Error: {e}")