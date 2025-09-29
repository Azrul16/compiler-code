"""
Whitespace Skipper for Source Programs
Handles:
- Spaces
- Tabs
- Newlines
- Comments (both single-line and multi-line)
"""

class WhitespaceSkipper:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
    
    def skip_whitespace(self):
        """Skip all whitespace and comments, return the cleaned content"""
        result = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            
            # Handle standard whitespace (space, tab, newline)
            if char.isspace():
                if char == '\n':
                    self.line += 1
                    self.column = 1
                elif char == '\t':
                    self.column += 4  # assuming tab = 4 spaces
                else:
                    self.column += 1
                self.pos += 1
                continue
            
            # Handle single-line comments
            if char == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '/':
                self.pos += 2  # skip '//'
                while self.pos < len(self.source) and self.source[self.pos] != '\n':
                    self.pos += 1
                continue
            
            # Handle multi-line comments
            if char == '/' and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == '*':
                self.pos += 2  # skip '/*'
                while self.pos + 1 < len(self.source):
                    if self.source[self.pos] == '*' and self.source[self.pos + 1] == '/':
                        self.pos += 2  # skip '*/'
                        break
                    if self.source[self.pos] == '\n':
                        self.line += 1
                        self.column = 1
                    self.pos += 1
                continue
            
            # Non-whitespace character found
            result.append(char)
            self.column += 1
            self.pos += 1
        
        return ''.join(result)
    
    def get_position_info(self):
        """Return current line and column information"""
        return f"Line {self.line}, Column {self.column}"

def main():
    print("Whitespace Skipper Demo")
    print("=" * 50)
    
    # Limited to 2 representative test cases
    test_cases = [
        # Test Case 1: Mixed whitespace and comments
        """
        int main() {
            // Main function
            return 0;  /* Exit code */
        }
        """,
        
        # Test Case 2: Complex comments and indentation
        """int factorial(int n) {
            /* Recursive factorial
               implementation */
            if (n <= 1) return 1;
            return n * factorial(n-1);  // Recursive call
        }"""
    ]
    
    for i, source in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("-" * 40)
        print("Original source code:")
        print(source)
        
        skipper = WhitespaceSkipper(source)
        cleaned = skipper.skip_whitespace()
        
        print("\nAfter skipping whitespace and comments:")
        print(cleaned)
        print(f"\nFinal position: {skipper.get_position_info()}")

if __name__ == "__main__":
    main()
