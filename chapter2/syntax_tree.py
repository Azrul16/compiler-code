"""
Syntax Tree Implementation

Represents program structure as trees for intermediate code generation.
Supports three-address code generation.
"""

class Node:
    def __init__(self):
        pass
    
    def __str__(self):
        return "Node"
    
    def gen(self):
        pass

class Expr(Node):
    def __init__(self):
        super().__init__()

class Stmt(Node):
    def __init__(self):
        super().__init__()

class Op(Expr):
    temp_count = 1
    
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"
    
    def gen(self):
        left_temp = self.left.gen() if hasattr(self.left, 'gen') else str(self.left)
        right_temp = self.right.gen() if hasattr(self.right, 'gen') else str(self.right)
        temp = f"t{Op.temp_count}"
        Op.temp_count += 1
        print(f"{temp} = {left_temp} {self.op} {right_temp}")
        return temp

class Assign(Stmt):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
    
    def __str__(self):
        return f"{self.left} = {self.right}"
    
    def gen(self):
        right_temp = self.right.gen() if hasattr(self.right, 'gen') else str(self.right)
        print(f"{self.left} = {right_temp}")

class NumNode(Expr):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
    def gen(self):
        return str(self.value)

class IdNode(Expr):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return self.name
    
    def gen(self):
        return self.name

if __name__ == "__main__":
    print("Testing Syntax Tree:")
    print("=" * 50)
    
    # Create syntax tree for: x = a + b * 3
    expr = Op('*', IdNode('b'), NumNode(3))
    expr = Op('+', IdNode('a'), expr)
    stmt = Assign(IdNode('x'), expr)
    
    print("Syntax Tree:", stmt)
    print("\nThree-Address Code:")
    stmt.gen()