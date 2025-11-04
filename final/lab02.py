class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def __repr__(self, level=0):
        ret = "  " * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

def parse_id_plus_id_times_id():
    # Parse tree for: id + id * id
    F1 = Node('id')
    T1 = Node('T', [F1, Node("T'", [Node('ε')])])
    F2 = Node('id')
    F3 = Node('id')
    T2 = Node('T', [F2, Node("T'", [Node('*'), F3, Node("T'", [Node('ε')])])])
    E2 = Node('E', [T2, Node("E'", [Node('ε')])])
    E1 = Node('E', [T1, Node("E'", [Node('+'), E2])])
    return E1

print("Lab02: Top-Down Parse Tree for 'id + id * id'")
root = parse_id_plus_id_times_id()
print(root)
print()
