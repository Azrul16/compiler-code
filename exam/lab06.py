"""
Complete Lexical Analyzer
Features:
1. Tokenizes all common programming language elements
2. Handles multi-character operators
3. Recognizes string and character literals
4. Skips comments (single and multi-line)
5. Maintains symbol table
6. Provides detailed error reporting
"""

from enum import Enum, auto
import re

class TokenType(Enum):
    # Keywords
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    INT = auto()
    FLOAT = auto()
    CHAR = auto()
    VOID = auto()
    RETURN = auto()
    
    # Identifiers and literals
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT_LITERAL = auto()
    STRING = auto()
    CHAR_LITERAL = auto()
    
    # Operators
    PLUS = auto()          # +
    MINUS = auto()         # -
    MULTIPLY = auto()      # *
    DIVIDE = auto()        # /
    ASSIGN = auto()        # =
    EQ = auto()           # ==
    NE = auto()           # !=
    LT = auto()           # <
    GT = auto()           # >
    LE = auto()           # <=
    GE = auto()           # >=
    
    # Delimiters
    LPAREN = auto()       # (
    RPAREN = auto()       # )
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    SEMICOLON = auto()    # ;
    COMMA = auto()        # ,
    
    # Special
    EOF = auto()
    ERROR = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}') at line {self.line}, column {self.column}"

class LexicalError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"{message} at line {line}, column {column}")

class LexicalAnalyzer:
    def __init__(self):
        # Keywords mapping
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'char': TokenType.CHAR,
            'void': TokenType.VOID,
            'return': TokenType.RETURN
        }
        
        # Operator mapping
        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '=': TokenType.ASSIGN,
            '==': TokenType.EQ,
            '!=': TokenType.NE,
            '<': TokenType.LT,
            '>': TokenType.GT,
            '<=': TokenType.LE,
            '>=': TokenType.GE,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            ',': TokenType.COMMA
        }
        
        # Symbol table
        self.symbol_table = {}
        
        # State variables
        self.source = ""
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = None
    
    def init_scanner(self, source):
        """Initialize the scanner with source code"""
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.advance()
    
    def advance(self):
        """Move to next character"""
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
            self.pos += 1
            self.column += 1
    
    def peek(self):
        """Look at next character without consuming it"""
        peek_pos = self.pos
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            self.advance()
    
    def skip_comment(self):
        """Skip single and multi-line comments"""
        if self.current_char == '/' and self.peek() == '/':
            # Single-line comment
            while self.current_char and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peek() == '*':
            # Multi-line comment
            self.advance()  # skip /
            self.advance()  # skip *
            while self.current_char:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  # skip *
                    self.advance()  # skip /
                    break
                if self.current_char == '\n':
                    self.line += 1
                    self.column = 1
                self.advance()
    
    def read_identifier(self):
        """Read an identifier or keyword"""
        start_column = self.column
        result = ""
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(result, TokenType.IDENTIFIER)
        token = Token(token_type, result, self.line, start_column)
        
        # Add to symbol table if it's an identifier
        if token_type == TokenType.IDENTIFIER:
            if result not in self.symbol_table:
                self.symbol_table[result] = {
                    'first_seen': (self.line, start_column),
                    'occurrences': []
                }
            self.symbol_table[result]['occurrences'].append((self.line, start_column))
        
        return token
    
    def read_number(self):
        """Read a number (integer or float)"""
        start_column = self.column
        result = ""
        is_float = False
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if is_float:
                    raise LexicalError("Invalid float literal", self.line, self.column)
                is_float = True
            result += self.current_char
            self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT_LITERAL, float(result), self.line, start_column)
        return Token(TokenType.INTEGER, int(result), self.line, start_column)
    
    def read_string(self):
        """Read a string literal"""
        start_column = self.column
        self.advance()  # skip opening quote
        result = ""
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char in {'n', 't', '"', '\\'}:
                    result += '\\' + self.current_char
                else:
                    raise LexicalError("Invalid escape sequence", self.line, self.column)
            else:
                result += self.current_char
            self.advance()
        
        if not self.current_char:
            raise LexicalError("Unterminated string literal", self.line, start_column)
        
        self.advance()  # skip closing quote
        return Token(TokenType.STRING, result, self.line, start_column)
    
    def read_char_literal(self):
        """Read a character literal"""
        start_column = self.column
        self.advance()  # skip opening quote
        
        if not self.current_char:
            raise LexicalError("Unterminated character literal", self.line, start_column)
        
        if self.current_char == '\\':
            self.advance()
            if self.current_char in {'n', 't', "'", '\\'}:
                value = '\\' + self.current_char
            else:
                raise LexicalError("Invalid escape sequence", self.line, self.column)
        else:
            value = self.current_char
        
        self.advance()
        
        if self.current_char != "'":
            raise LexicalError("Unterminated character literal", self.line, start_column)
        
        self.advance()  # skip closing quote
        return Token(TokenType.CHAR_LITERAL, value, self.line, start_column)
    
    def get_next_token(self):
        """Get the next token from input"""
        while self.current_char:
            # Skip whitespace and comments
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '/' and (self.peek() == '/' or self.peek() == '*'):
                self.skip_comment()
                continue
            
            # Identifier or keyword
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Number
            if self.current_char.isdigit():
                return self.read_number()
            
            # String literal
            if self.current_char == '"':
                return self.read_string()
            
            # Character literal
            if self.current_char == "'":
                return self.read_char_literal()
            
            # Multi-character operators
            if self.current_char in {'=', '!', '<', '>'}:
                op = self.current_char
                if self.peek() == '=':
                    op += '='
                    self.advance()
                    self.advance()
                    return Token(self.operators[op], op, self.line, self.column - len(op))
            
            # Single-character operators and delimiters
            if self.current_char in self.operators:
                char = self.current_char
                self.advance()
                return Token(self.operators[char], char, self.line, self.column - 1)
            
            # Invalid character
            raise LexicalError(f"Invalid character: {self.current_char}", self.line, self.column)
        
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self, source):
        """Tokenize the entire source code"""
        self.init_scanner(source)
        tokens = []
        
        try:
            while True:
                token = self.get_next_token()
                tokens.append(token)
                if token.type == TokenType.EOF:
                    break
        except LexicalError as e:
            print(f"Lexical Error: {e}")
            return []
        
        return tokens

def main():
    print("Complete Lexical Analyzer")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        # Test case 1: Basic program structure
        """
        int main() {
            return 0;
        }
        """,
        
        # Test case 2: Variables and expressions
        """
        float calculate(int x, float y) {
            float result = 0.0;
            if (x > 0) {
                result = x * y;
            }
            return result;
        }
        """,
        
        # Test case 3: Comments and strings
        """
        // Single line comment
        void print_message() {
            /* Multi-line
               comment */
            char msg = 'H';
            string text = "Hello, World!";
        }
        """
    ]
    
    analyzer = LexicalAnalyzer()
    
    for i, source in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 40)
        print("Source code:")
        print(source)
        
        tokens = analyzer.tokenize(source)
        
        print("\nTokens:")
        for token in tokens:
            if token.type != TokenType.EOF:
                print(token)
        
        print("\nSymbol table:")
        for identifier, info in analyzer.symbol_table.items():
            print(f"Identifier: {identifier}")
            print(f"  First seen at: Line {info['first_seen'][0]}, Column {info['first_seen'][1]}")
            print(f"  Occurrences: {len(info['occurrences'])}")
    
    # Interactive mode
    print("\nInteractive Mode")
    print("=" * 50)
    print("Enter source code (press Ctrl+D or Ctrl+Z to finish):")
    
    try:
        user_input = []
        while True:
            line = input()
            user_input.append(line)
    except (EOFError, KeyboardInterrupt):
        if user_input:
            source = '\n'.join(user_input)
            analyzer = LexicalAnalyzer()
            tokens = analyzer.tokenize(source)
            
            print("\nAnalysis Results:")
            print("-" * 40)
            
            print("\nTokens:")
            for token in tokens:
                if token.type != TokenType.EOF:
                    print(token)
            
            print("\nSymbol table:")
            for identifier, info in analyzer.symbol_table.items():
                print(f"Identifier: {identifier}")
                print(f"  First seen at: Line {info['first_seen'][0]}, Column {info['first_seen'][1]}")
                print(f"  Occurrences: {len(info['occurrences'])}")

if __name__ == "__main__":
    main()
