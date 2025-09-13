"""
Token Classes Implementation

Base class for tokens with subclasses for numbers and words.
Tokens are the basic building blocks recognized by the lexical analyzer.
"""

class Token:
    def __init__(self, tag):
        self.tag = tag
    
    def __str__(self):
        return f"Token<{self.tag}>"
    
    def __repr__(self):
        return self.__str__()

class Num(Token):
    def __init__(self, value):
        # Import here to avoid circular imports
        import tag_constants
        super().__init__(tag_constants.Tag.NUM)
        self.value = value
    
    def __str__(self):
        return f"Num<{self.value}>"

class Word(Token):
    def __init__(self, tag, lexeme):
        super().__init__(tag)
        self.lexeme = lexeme
    
    def __str__(self):
        return f"Word<{self.tag}, '{self.lexeme}'>"

if __name__ == "__main__":
    print("Testing Token Classes:")
    print("=" * 50)
    
    # Create some tokens
    plus_token = Token(43)  # ASCII for '+'
    num_token = Num(42)
    word_token = Word(256, "variable")
    
    print("Plus token:", plus_token)
    print("Number token:", num_token)
    print("Word token:", word_token)
    print("Number value:", num_token.value)
    print("Word lexeme:", word_token.lexeme)