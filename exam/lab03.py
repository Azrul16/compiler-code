"""
Infix to Postfix Expression Translator
Supports:
- Basic arithmetic operators (+, -, *, /)
- Parentheses
- Numbers and variables
"""

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class InfixToPostfix:
    def __init__(self):
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '(': 0,  # lowest precedence
        }
        
    def tokenize(self, expression):
        """Convert input string into list of tokens"""
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
                
            # Handle numbers (including multi-digit)
            if char.isdigit():
                num = ""
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                tokens.append(Token('NUMBER', num))
                continue
                
            # Handle variables/identifiers
            if char.isalpha():
                var = ""
                while i < len(expression) and (expression[i].isalnum()):
                    var += expression[i]
                    i += 1
                tokens.append(Token('VARIABLE', var))
                continue
                
            # Handle operators and parentheses
            if char in '+-*/()':
                tokens.append(Token('OPERATOR', char))
                i += 1
                continue
                
            raise ValueError(f"Invalid character: {char}")
            
        return tokens

    def translate(self, expression):
        """Translate infix expression to postfix"""
        tokens = self.tokenize(expression)
        operator_stack = []
        output = []
        
        for token in tokens:
            if token.type in ('NUMBER', 'VARIABLE'):
                output.append(token.value)
                
            elif token.value == '(':
                operator_stack.append(token.value)
                
            elif token.value == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()  # remove '('
                else:
                    raise ValueError("Mismatched parentheses")
                    
            else:  # operators
                while (operator_stack and operator_stack[-1] != '(' and 
                       self.precedence[operator_stack[-1]] >= self.precedence[token.value]):
                    output.append(operator_stack.pop())
                operator_stack.append(token.value)
        
        # Pop remaining operators
        while operator_stack:
            op = operator_stack.pop()
            if op == '(':
                raise ValueError("Mismatched parentheses")
            output.append(op)
            
        return ' '.join(output)

def main():
    translator = InfixToPostfix()
    
    # Test cases
    test_expressions = [
        "3 + 4",
        "a + b * c",
        "(a + b) * c",
        "5 + ((1 + 2) * 4) - 3",
        "x * y / (5 + 2)",
        "42"
    ]
    
    print("Infix to Postfix Translator")
    print("=" * 40)
    
    for expr in test_expressions:
        try:
            print(f"\nInfix:   {expr}")
            postfix = translator.translate(expr)
            print(f"Postfix: {postfix}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nInteractive Mode")
    print("=" * 40)
    print("Enter expressions (or 'quit' to exit)")
    
    while True:
        try:
            expr = input("\nInfix: ").strip()
            if expr.lower() == 'quit':
                break
            if expr:
                postfix = translator.translate(expr)
                print(f"Postfix: {postfix}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
