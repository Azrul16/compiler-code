"""
Implementation of Lvalue and Rvalue calls for instruction generation.
Handles:
1. Identifier references
2. Constants
3. Temporary variable generation
4. Expression evaluation
5. Assignment operations
"""

from enum import Enum, auto
from typing import List, Optional

class NodeType(Enum):
    ID = auto()
    TEMP = auto()
    CONSTANT = auto()
    OPERATOR = auto()

class Node:
    temp_counter = 0
    
    @classmethod
    def get_temp(cls) -> str:
        """Generate a new temporary variable name"""
        cls.temp_counter += 1
        return f"t{cls.temp_counter}"
    
    def __init__(self, node_type: NodeType, value: str):
        self.type = node_type
        self.value = value
        self.code: List[str] = []  # Generated instructions
    
    def __str__(self):
        return f"{self.value}"

class Expression:
    def __init__(self):
        self.code: List[str] = []
        self.result: Optional[Node] = None
    
    def add_instruction(self, instruction: str):
        """Add a new instruction to the code sequence"""
        self.code.append(instruction)
    
    def merge_code(self, other_code: List[str]):
        """Merge another code sequence into this one"""
        self.code.extend(other_code)

class InstructionGenerator:
    def __init__(self):
        self.symbol_table = {}  # Simple symbol table for this example
    
    def is_identifier(self, name: str) -> bool:
        """Check if a name is a valid identifier"""
        return name.isidentifier()
    
    def is_constant(self, value: str) -> bool:
        """Check if a value represents a constant"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def rvalue(self, x: Node) -> Node:
        """
        Generate rvalue for a node:
        - For identifiers or constants, return the node itself
        - For expressions, generate a temporary and return its node
        """
        if x.type in {NodeType.ID, NodeType.CONSTANT}:
            return x
        
        # Generate new temporary for complex expressions
        temp_name = Node.get_temp()
        temp_node = Node(NodeType.TEMP, temp_name)
        temp_node.code = x.code + [f"{temp_name} = {x.value}"]
        return temp_node
    
    def lvalue(self, x: Node) -> Node:
        """
        Generate lvalue for a node:
        - For identifiers, return the node itself
        - For other cases, generate error (can't assign to non-lvalue)
        """
        if x.type != NodeType.ID:
            raise ValueError(f"Cannot use {x.value} as an lvalue")
        return x
    
    def gen_binary_op(self, left: Node, op: str, right: Node) -> Node:
        """Generate code for binary operation"""
        left_rvalue = self.rvalue(left)
        right_rvalue = self.rvalue(right)
        
        temp_name = Node.get_temp()
        result = Node(NodeType.TEMP, temp_name)
        result.code = (left_rvalue.code + right_rvalue.code +
                      [f"{temp_name} = {left_rvalue.value} {op} {right_rvalue.value}"])
        return result
    
    def gen_assignment(self, target: Node, value: Node) -> Expression:
        """Generate code for assignment operation"""
        lval = self.lvalue(target)
        rval = self.rvalue(value)
        
        result = Expression()
        result.merge_code(rval.code)
        result.add_instruction(f"{lval.value} = {rval.value}")
        result.result = lval
        return result

def main():
    print("Instruction Generation with Lvalue/Rvalue Demonstration")
    print("=" * 60)
    
    gen = InstructionGenerator()
    
    # Test Case 1: Simple assignment with constant
    print("\nTest Case 1: Simple assignment (x = 5)")
    print("-" * 40)
    x = Node(NodeType.ID, "x")
    five = Node(NodeType.CONSTANT, "5")
    result = gen.gen_assignment(x, five)
    print("Generated code:")
    for instr in result.code:
        print(f"  {instr}")
    
    # Test Case 2: Complex expression with temporaries
    print("\nTest Case 2: Complex expression (y = a + b * c)")
    print("-" * 40)
    y = Node(NodeType.ID, "y")
    a = Node(NodeType.ID, "a")
    b = Node(NodeType.ID, "b")
    c = Node(NodeType.ID, "c")
    
    # Generate b * c
    mult = gen.gen_binary_op(b, "*", c)
    # Generate a + (b * c)
    add = gen.gen_binary_op(a, "+", mult)
    # Generate final assignment
    result = gen.gen_assignment(y, add)
    
    print("Generated code:")
    for instr in result.code:
        print(f"  {instr}")

if __name__ == "__main__":
    main()
