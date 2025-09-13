"""
Symbol Table Environment Implementation

Implements chained symbol tables for handling nested scopes.
Supports the "most closely nested" rule for scoping.
"""

class Environment:
    def __init__(self, prev=None):
        self.table = {}
        self.prev = prev
    
    def put(self, name, symbol):
        self.table[name] = symbol
    
    def get(self, name):
        env = self
        while env is not None:
            if name in env.table:
                return env.table[name]
            env = env.prev
        return None
    
    def __str__(self):
        result = []
        env = self
        level = 0
        while env is not None:
            result.append(f"Level {level}: {env.table}")
            env = env.prev
            level += 1
        return "\n".join(result)

if __name__ == "__main__":
    print("Testing Symbol Table Environment:")
    print("=" * 50)
    
    # Create a simple symbol class
    class Symbol:
        def __init__(self, name, type):
            self.name = name
            self.type = type
        
        def __str__(self):
            return f"{self.name}:{self.type}"
    
    # Create environments
    global_env = Environment()
    global_env.put("x", Symbol("x", "int"))
    global_env.put("y", Symbol("y", "char"))
    
    local_env = Environment(global_env)
    local_env.put("y", Symbol("y", "bool"))
    local_env.put("z", Symbol("z", "float"))
    
    print("Environment Chain:")
    print("-" * 30)
    print(local_env)
    
    print("\nSymbol Lookups:")
    print("-" * 30)
    print("x in local:", local_env.get("x"))
    print("y in local:", local_env.get("y"))
    print("z in local:", local_env.get("z"))
    print("w in local:", local_env.get("w"))