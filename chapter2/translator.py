"""
Complete Postfix Translator

Integrates all components for infix to postfix translation.
Provides both command-line and interactive modes.
"""

from lexer import Lexer
from parser import Parser
import sys

class PostfixTranslator:
    def __init__(self):
        pass
    
    def translate(self, input_text):
        lexer = Lexer(input_text)
        parser = Parser(lexer)
        
        print("Postfix: ", end='')
        parser.expr()
        print()
    
    def interactive_mode(self):
        print("Interactive Postfix Translator")
        print("Enter expressions or 'quit' to exit")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\nInfix expression: ").strip()
                if user_input.lower() in ['quit', 'exit', '']:
                    break
                
                self.translate(user_input)
                
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    translator = PostfixTranslator()
    
    if len(sys.argv) > 1:
        expression = ' '.join(sys.argv[1:])
        translator.translate(expression)
    else:
        translator.interactive_mode()