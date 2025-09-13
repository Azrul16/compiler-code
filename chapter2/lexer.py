"""
Lexical Analyzer Implementation

Converts source code into tokens by:
- Skipping whitespace
- Recognizing numbers, identifiers, and keywords
- Identifying operators and special symbols
- Building a symbol table
"""

import sys
from token_classes import Token, Num, Word
import tag_constants

class Lexer:
    def __init__(self, input_text=None):
        self.line = 1
        self.peek = ' '
        self.words = {}
        self.input_text = input_text
        self.input_index = 0
        
        # Reserve keywords
        self.reserve(Word(tag_constants.Tag.TRUE, "true"))
        self.reserve(Word(tag_constants.Tag.FALSE, "false"))
    
    def reserve(self, word):
        self.words[word.lexeme] = word
    
    def read_char(self):
        if self.input_text:
            if self.input_index < len(self.input_text):
                char = self.input_text[self.input_index]
                self.input_index += 1
                return char
            return '\0'
        else:
            return sys.stdin.read(1)
    
    def scan(self):
        # Skip whitespace
        while True:
            if self.peek in ' \t':
                pass
            elif self.peek == '\n':
                self.line += 1
            else:
                break
            self.peek = self.read_char()
            if self.peek == '\0':
                return Token(tag_constants.Tag.NUM)
        
        # Handle numbers
        if self.peek.isdigit():
            v = 0
            while self.peek.isdigit():
                v = v * 10 + int(self.peek)
                self.peek = self.read_char()
            return Num(v)
        
        # Handle identifiers and keywords
        if self.peek.isalpha():
            buffer = []
            while self.peek.isalnum():
                buffer.append(self.peek)
                self.peek = self.read_char()
            s = ''.join(buffer)
            
            # Check if reserved word
            w = self.words.get(s)
            if w is not None:
                return w
            
            # It's an identifier
            w = Word(tag_constants.Tag.ID, s)
            self.words[s] = w
            return w
        
        # Handle single character tokens
        t = Token(ord(self.peek))
        self.peek = ' '
        return t

if __name__ == "__main__":
    print("Testing Lexical Analyzer:")
    print("=" * 50)
    
    test_input = "x = 42 + hello true"
    lexer = Lexer(test_input)
    
    print(f"Input: '{test_input}'")
    print("\nTokens:")
    print("-" * 30)
    
    for i in range(6):
        token = lexer.scan()
        print(f"{i+1}: {token}")
    
    print("\nSymbol Table Contents:")
    print("-" * 30)
    for key, value in lexer.words.items():
        print(f"{key}: {value}")