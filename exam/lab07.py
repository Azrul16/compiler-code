"""
Chained Symbol Table Implementation
Features:
1. Supports nested scopes
2. Implements the "most closely nested" rule
3. Handles variable declarations and lookups
4. Supports different types of symbols (variables, functions, etc.)
5. Maintains scope hierarchy
"""

from enum import Enum, auto
from typing import Dict, Optional, List

class SymbolType(Enum):
    VARIABLE = auto()
    FUNCTION = auto()
    PARAMETER = auto()
    ARRAY = auto()
    CONSTANT = auto()

class Symbol:
    def __init__(self, name: str, symbol_type: SymbolType, data_type: str = None):
        self.name = name
        self.symbol_type = symbol_type
        self.data_type = data_type
        self.line_declared = 0
        self.scope_level = 0
        
    def __str__(self):
        return f"{self.name} ({self.symbol_type.name}, {self.data_type}) at line {self.line_declared}"

class Scope:
    def __init__(self, parent: Optional['Scope'] = None, scope_name: str = ""):
        self.symbols: Dict[str, Symbol] = {}
        self.parent = parent
        self.children: List[Scope] = []
        self.scope_name = scope_name
        self.level = 0 if parent is None else parent.level + 1
        
        if parent:
            parent.children.append(self)
    
    def define(self, symbol: Symbol) -> bool:
        """
        Define a new symbol in current scope.
        Returns False if symbol already exists in this scope.
        """
        if symbol.name in self.symbols:
            return False
        
        symbol.scope_level = self.level
        self.symbols[symbol.name] = symbol
        return True
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """
        Look up a symbol in this scope and all parent scopes.
        Implements the "most closely nested" rule.
        """
        current = self
        while current:
            if name in current.symbols:
                return current.symbols[name]
            current = current.parent
        return None
    
    def get_symbols(self) -> Dict[str, Symbol]:
        """Get all symbols accessible from this scope"""
        result = {}
        current = self
        while current:
            # Add symbols from current scope, not overwriting more local ones
            for name, symbol in current.symbols.items():
                if name not in result:
                    result[name] = symbol
            current = current.parent
        return result

class ChainedSymbolTable:
    def __init__(self):
        self.global_scope = Scope(scope_name="global")
        self.current_scope = self.global_scope
        self.scope_stack = [self.global_scope]
    
    def enter_scope(self, scope_name: str = "") -> Scope:
        """Create and enter a new scope"""
        new_scope = Scope(self.current_scope, scope_name)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope
        return new_scope
    
    def exit_scope(self) -> Optional[Scope]:
        """Exit current scope and return to parent scope"""
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            return self.current_scope
        return None
    
    def define(self, name: str, symbol_type: SymbolType, data_type: str = None, line: int = 0) -> bool:
        """Define a new symbol in current scope"""
        symbol = Symbol(name, symbol_type, data_type)
        symbol.line_declared = line
        return self.current_scope.define(symbol)
    
    def resolve(self, name: str) -> Optional[Symbol]:
        """Look up a symbol starting from current scope"""
        return self.current_scope.resolve(name)
    
    def dump_table(self, scope: Optional[Scope] = None, indent: int = 0) -> str:
        """Generate a readable representation of the symbol table"""
        if scope is None:
            scope = self.global_scope
        
        result = []
        indent_str = "  " * indent
        result.append(f"{indent_str}Scope: {scope.scope_name or f'anonymous_{scope.level}'}")
        
        # Sort symbols by name for consistent output
        sorted_symbols = sorted(scope.symbols.items())
        for name, symbol in sorted_symbols:
            result.append(f"{indent_str}  {symbol}")
        
        # Recursively dump child scopes
        for child in scope.children:
            result.append(self.dump_table(child, indent + 1))
        
        return "\n".join(result)

def main():
    print("Chained Symbol Table Demo")
    print("=" * 50)
    
    # Create symbol table
    table = ChainedSymbolTable()
    
    # Test case 1: Global scope
    print("\nTest Case 1: Global scope declarations")
    print("-" * 40)
    table.define("printf", SymbolType.FUNCTION, "int", 1)
    table.define("MAX_SIZE", SymbolType.CONSTANT, "int", 2)
    print(table.dump_table())
    
    # Test case 2: Function scope
    print("\nTest Case 2: Function scope")
    print("-" * 40)
    table.enter_scope("main")
    table.define("x", SymbolType.VARIABLE, "int", 3)
    table.define("y", SymbolType.VARIABLE, "float", 4)
    print(table.dump_table())
    
    # Test case 3: Nested block scope
    print("\nTest Case 3: Nested block scope")
    print("-" * 40)
    table.enter_scope("if_block")
    table.define("temp", SymbolType.VARIABLE, "float", 5)
    print(table.dump_table())
    
    # Test case 4: Symbol resolution
    print("\nTest Case 4: Symbol resolution")
    print("-" * 40)
    test_symbols = ["temp", "x", "printf", "undefined"]
    for name in test_symbols:
        symbol = table.resolve(name)
        if symbol:
            print(f"Found: {symbol}")
        else:
            print(f"Not found: {name}")
    
    # Test case 5: Exiting scopes
    print("\nTest Case 5: Exiting scopes")
    print("-" * 40)
    table.exit_scope()  # exit if_block
    table.exit_scope()  # exit main
    print(table.dump_table())
    
    # Interactive mode
    print("\nInteractive Mode")
    print("=" * 50)
    print("Available commands:")
    print("1. enter <scope_name> - Enter a new scope")
    print("2. exit - Exit current scope")
    print("3. define <name> <type> <data_type> - Define a new symbol")
    print("4. resolve <name> - Look up a symbol")
    print("5. dump - Show current symbol table")
    print("6. quit - Exit interactive mode")
    
    table = ChainedSymbolTable()  # Reset table for interactive mode
    
    while True:
        try:
            command = input("\nEnter command: ").strip().split()
            if not command:
                continue
            
            if command[0] == 'quit':
                break
            elif command[0] == 'enter' and len(command) > 1:
                table.enter_scope(command[1])
                print(f"Entered scope: {command[1]}")
            elif command[0] == 'exit':
                if table.exit_scope():
                    print("Exited scope")
                else:
                    print("Cannot exit global scope")
            elif command[0] == 'define' and len(command) >= 4:
                name = command[1]
                try:
                    symbol_type = SymbolType[command[2].upper()]
                    if table.define(name, symbol_type, command[3]):
                        print(f"Defined: {name}")
                    else:
                        print(f"Error: {name} already defined in current scope")
                except KeyError:
                    print(f"Invalid symbol type. Use one of: {', '.join(t.name for t in SymbolType)}")
            elif command[0] == 'resolve' and len(command) > 1:
                symbol = table.resolve(command[1])
                if symbol:
                    print(f"Found: {symbol}")
                else:
                    print(f"Not found: {command[1]}")
            elif command[0] == 'dump':
                print("\nCurrent Symbol Table:")
                print(table.dump_table())
            else:
                print("Invalid command")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
