"""
Non-recursive implementation of parser procedures with complete implementation
No external imports needed.
"""

class Tag:
    # Single-character tokens use ASCII values
    # Multi-character tokens
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259
    # Relational operators
    LE = 260  # <=
    GE = 261  # >=
    EQ = 262  # ==
    NE = 263  # !=

class Token:
    def __init__(self, tag):
        self.tag = tag
    
    def __str__(self):
        return f"Token<{self.tag}>"
    
    def __repr__(self):
        return self.__str__()

class Num(Token):
    def __init__(self, value):
        super().__init__(Tag.NUM)
        self.value = value
    
    def __str__(self):
        return f"Num<{self.value}>"

class Word(Token):
    def __init__(self, tag, lexeme):
        super().__init__(tag)
        self.lexeme = lexeme
    
    def __str__(self):
        return f"Word<{self.tag}, '{self.lexeme}'>"

class Lexer:
    def __init__(self, input_text=None):
        self.line = 1
        self.peek = ' '
        self.words = {}
        self.input_text = input_text
        self.input_index = 0
        
        # Reserve keywords
        self.reserve(Word(Tag.TRUE, "true"))
        self.reserve(Word(Tag.FALSE, "false"))
    
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
                return Token(Tag.NUM)
        
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
            w = Word(Tag.ID, s)
            self.words[s] = w
            return w
        
        # Handle single character tokens
        t = Token(ord(self.peek))
        self.peek = ' '
        return t

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
        # Non-recursive expr implementation
        # Original recursive version combined term() and rest()
        # Now we handle it iteratively
        self.term()
        
        # Instead of recursive rest(), handle operators in a loop
        while self.lookahead.tag in {ord('+'), ord('-')}:
            if self.lookahead.tag == ord('+'):
                self.match(ord('+'))
                self.term()
                print('+', end='')
            elif self.lookahead.tag == ord('-'):
                self.match(ord('-'))
                self.term()
                print('-', end='')
    
    def term(self):
        # Non-recursive term implementation
        # Original version was already non-recursive, but included here for completeness
        if self.lookahead.tag == Tag.NUM:
            print(self.lookahead.value, end='')
            self.match(Tag.NUM)
        else:
            raise SyntaxError("Expected number")

def main():
    print("Testing Non-recursive Parser:")
    print("=" * 50)
    
    # Limited to 2 representative test cases
    test_cases = [
        "3+4-1",     # Test Case 1: Multiple operations
        "9-5+2"      # Test Case 2: Different operation order
    ]
    
    for test_input in test_cases:
        print(f"\nTest Case: '{test_input}'")
        print("Converting infix to postfix...")
        print("Input: ", test_input)
        print("Postfix output: ", end='')
        
        try:
            lexer = Lexer(test_input)
            parser = Parser(lexer)
            parser.expr()
            print()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    import sys
    main()
