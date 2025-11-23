
class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []
    
    def print_tree(self, prefix="", is_last=True):
        """Print tree in a nice format"""
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(self.value))
        
        if self.children:
            extension = "    " if is_last else "│   "
            for i, child in enumerate(self.children):
                child.print_tree(prefix + extension, i == len(self.children) - 1)

def top_down_parse_tree():
    """
    Top-down parse tree for: id + id * id
    
    Using non-left-recursive grammar:
    E → T E'
    E' → + T E' | ε
    T → F T'
    T' → * F T' | ε
    F → id
    """
    # Root
    E = TreeNode("E")
    
    # E → T E'
    T1 = TreeNode("T")
    E_prime = TreeNode("E'")
    E.children = [T1, E_prime]
    
    # T → F T' (first T)
    F1 = TreeNode("F")
    T_prime1 = TreeNode("T'")
    T1.children = [F1, T_prime1]
    
    # F → id (first id)
    id1 = TreeNode("id")
    F1.children = [id1]
    
    # T' → ε (no multiplication for first term)
    epsilon1 = TreeNode("ε")
    T_prime1.children = [epsilon1]
    
    # E' → + T E' (addition)
    plus = TreeNode("+")
    T2 = TreeNode("T")
    E_prime2 = TreeNode("E'")
    E_prime.children = [plus, T2, E_prime2]
    
    # T → F T' (second T)
    F2 = TreeNode("F")
    T_prime2 = TreeNode("T'")
    T2.children = [F2, T_prime2]
    
    # F → id (second id)
    id2 = TreeNode("id")
    F2.children = [id2]
    
    # T' → * F T' (multiplication)
    multiply = TreeNode("*")
    F3 = TreeNode("F")
    T_prime3 = TreeNode("T'")
    T_prime2.children = [multiply, F3, T_prime3]
    
    # F → id (third id)
    id3 = TreeNode("id")
    F3.children = [id3]
    
    # T' → ε (end)
    epsilon2 = TreeNode("ε")
    T_prime3.children = [epsilon2]
    
    # E' → ε (end of expression)
    epsilon3 = TreeNode("ε")
    E_prime2.children = [epsilon3]
    
    return E

def bottom_up_parse_tree():
    """
    Bottom-up parse tree for: id * id
    
    Using grammar:
    E → T
    T → T * F | F
    F → id
    
    Bottom-up reduction sequence:
    1. id (shift)
    2. id → F (reduce by F → id)
    3. F → T (reduce by T → F)
    4. * (shift)
    5. id (shift)
    6. id → F (reduce by F → id)
    7. T * F → T (reduce by T → T * F)
    8. T → E (reduce by E → T)
    """
    # Root
    E = TreeNode("E")
    
    # E → T
    T = TreeNode("T")
    E.children = [T]
    
    # T → T * F
    T_left = TreeNode("T")
    multiply = TreeNode("*")
    F_right = TreeNode("F")
    T.children = [T_left, multiply, F_right]
    
    # Left T → F (first id)
    F_left = TreeNode("F")
    T_left.children = [F_left]
    
    # F → id (first id)
    id1 = TreeNode("id")
    F_left.children = [id1]
    
    # Right F → id (second id)
    id2 = TreeNode("id")
    F_right.children = [id2]
    
    return E

print("TOP-DOWN PARSE TREE for: id + id * id")
print("(Using grammar: E → TE', E' → +TE'|ε, T → FT', T' → *FT'|ε, F → id)")
print()
top_tree = top_down_parse_tree()
top_tree.print_tree()

print("\n" + "=" * 70)
print("BOTTOM-UP PARSE TREE for: id * id")
print("(Using grammar: E → T, T → T*F|F, F → id)")
print("(Shift-reduce parsing)")
print()
bottom_tree = bottom_up_parse_tree()
bottom_tree.print_tree()

print()
# ============================================================
#   PREDICTIVE (TOP-DOWN) & SHIFT-REDUCE (BOTTOM-UP) PARSER
#   Grammar:
#     E  → T E'
#     E' → + T E' | ε
#     T  → F T'
#     T' → * F T' | ε
#     F  → ( E ) | id
# ============================================================

# ----------------------------
# TOP-DOWN PREDICTIVE PARSER
# ----------------------------
grammar = {
    'E': [['T', "E'"]],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

# Predictive Parsing Table
parsing_table = {
    ('E', 'id'): ['T', "E'"],
    ('E', '('): ['T', "E'"],
    ("E'", '+'): ['+', 'T', "E'"],
    ("E'", ')'): ['ε'],
    ("E'", '$'): ['ε'],
    ('T', 'id'): ['F', "T'"],
    ('T', '('): ['F', "T'"],
    ("T'", '*'): ['*', 'F', "T'"],
    ("T'", '+'): ['ε'],
    ("T'", ')'): ['ε'],
    ("T'", '$'): ['ε'],
    ('F', 'id'): ['id'],
    ('F', '('): ['(', 'E', ')']
}

def top_down_parse(input_tokens):
    print("\n========= TOP-DOWN PARSING =========")
    stack = ['$', 'E']
    index = 0
    print(f"{'Stack':<25}{'Input':<25}{'Action'}")
    while len(stack) > 0:
        top = stack[-1]
        current = input_tokens[index]

        print(f"{''.join(stack):<25}{' '.join(input_tokens[index:]):<25}", end='')

        if top == current == '$':
            print("Accept")
            break
        elif top == current:
            stack.pop()
            index += 1
            print(f"Match {current}")
        elif (top, current) in parsing_table:
            stack.pop()
            production = parsing_table[(top, current)]
            if production != ['ε']:
                for symbol in reversed(production):
                    stack.append(symbol)
            print(f"{top} → {' '.join(production)}")
        else:
            print("Error")
            break


# ----------------------------
# BOTTOM-UP SHIFT-REDUCE PARSER
# ----------------------------
productions = {
    1: ('E', ['T', "E'"]),
    2: ("E'", ['+', 'T', "E'"]),
    3: ("E'", ['ε']),
    4: ('T', ['F', "T'"]),
    5: ("T'", ['*', 'F', "T'"]),
    6: ("T'", ['ε']),
    7: ('F', ['id']),
    8: ('F', ['(', 'E', ')'])
}

def find_reduction(stack):
    """Check if the stack tail matches any RHS"""
    for num, (lhs, rhs) in productions.items():
        if rhs == ['ε']:
            continue
        rhs_str = ' '.join(rhs)
        stack_str = ' '.join(stack[-len(rhs):])
        if rhs_str == stack_str:
            return num, lhs, rhs
    return None, None, None

def bottom_up_parse(tokens):
    print("\n========= BOTTOM-UP PARSING =========")
    stack = []
    i = 0
    print(f"{'Stack':<30}{'Input':<20}{'Action'}")

    while True:
        print(f"{' '.join(stack):<30}{' '.join(tokens[i:]):<20}", end='')

        # Try reduction first
        num, lhs, rhs = find_reduction(stack)
        if lhs:
            for _ in rhs:
                stack.pop()
            stack.append(lhs)
            print(f"Reduce: {lhs} → {' '.join(rhs)}")
        elif i < len(tokens):
            stack.append(tokens[i])
            i += 1
            print("Shift")
        else:
            print("Reject")
            break

        # Accept condition
        if stack == ['E'] and i == len(tokens):
            print(f"{' '.join(stack):<30}{' '.join(tokens[i:]):<20}Accept")
            break

if __name__ == "__main__":
    # Top-down parse for "id + id * id"
    input_tokens_top = ['id', '+', 'id', '*', 'id', '$']
    top_down_parse(input_tokens_top)

    # Bottom-up parse for "id * id"
    input_tokens_bottom = ['id', '*', 'id', '$']
    bottom_up_parse(input_tokens_bottom)
