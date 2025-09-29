"""
Keyword and Identifier Distinguisher
Implements a lexical analyzer that can:
1. Recognize keywords
2. Identify valid identifiers
3. Build a symbol table
"""

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"{self.type}<{self.value}> at line {self.line}, column {self.column}"

class LexicalAnalyzer:
    def __init__(self):
        # Define keywords (using C-like language keywords as example)
        self.keywords = {
            'if', 'else', 'while', 'for', 'do', 'break', 'continue',
            'int', 'float', 'char', 'void', 'return', 'struct',
            'switch', 'case', 'default', 'const', 'static'
        }
        
        # Symbol table for identifiers
        self.symbol_table = {}
        
        # Current position in input
        self.pos = 0
        self.line = 1
        self.column = 1
        
    def is_valid_identifier_start(self, char):
        """Check if character can start an identifier"""
        return char.isalpha() or char == '_'
    
    def is_valid_identifier_char(self, char):
        """Check if character can be in an identifier"""
        return char.isalnum() or char == '_'
    
    def skip_whitespace(self, text):
        """Skip whitespace and update position"""
        while self.pos < len(text) and text[self.pos].isspace():
            if text[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def analyze(self, text):
        """Analyze input text and return list of tokens"""
        tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        while self.pos < len(text):
            self.skip_whitespace(text)
            if self.pos >= len(text):
                break
            
            char = text[self.pos]
            start_column = self.column
            
            # Handle identifiers and keywords
            if self.is_valid_identifier_start(char):
                start = self.pos
                while self.pos < len(text) and self.is_valid_identifier_char(text[self.pos]):
                    self.pos += 1
                    self.column += 1
                
                word = text[start:self.pos]
                
                if word in self.keywords:
                    tokens.append(Token('KEYWORD', word, self.line, start_column))
                else:
                    # Add to symbol table if it's an identifier
                    if word not in self.symbol_table:
                        self.symbol_table[word] = {
                            'first_seen': (self.line, start_column),
                            'occurrences': []
                        }
                    self.symbol_table[word]['occurrences'].append((self.line, start_column))
                    tokens.append(Token('IDENTIFIER', word, self.line, start_column))
            
            # Handle numbers
            elif char.isdigit():
                start = self.pos
                while self.pos < len(text) and (text[self.pos].isdigit() or text[self.pos] == '.'):
                    self.pos += 1
                    self.column += 1
                tokens.append(Token('NUMBER', text[start:self.pos], self.line, start_column))
            
            # Handle operators and other characters
            else:
                tokens.append(Token('SYMBOL', char, self.line, self.column))
                self.pos += 1
                self.column += 1
        
        return tokens

def main():
    analyzer = LexicalAnalyzer()
    
    # Limited to 2 representative test cases
    test_cases = [
        # Test case 1: Function with keywords and identifiers
        """
        int calculate(float azrul) {
            return azrul * 2;
        }
        """,
        
        # Test case 2: Complex identifiers and multiple keywords
        """
        void process_data(int count) {
            float 10abc = 0.0;
            while (count > 0) {
                10abc += count;
            }
        }
        """
    ]
    
    print("Keyword and Identifier Analyzer")
    print("=" * 50)
    
    for i, source in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 40)
        print("Source code:")
        print(source)
        
        tokens = analyzer.analyze(source)
        
        print("\nTokens found:")
        for token in tokens:
            if token.type in ['KEYWORD', 'IDENTIFIER']:
                print(token)
        
        print("\nSymbol table entries:")
        for identifier, info in analyzer.symbol_table.items():
            print(f"Identifier: {identifier}")
            print(f"  First seen at: Line {info['first_seen'][0]}, Column {info['first_seen'][1]}")
            print(f"  Occurrences: {len(info['occurrences'])}")

if __name__ == "__main__":
    main()
