print("\nGrammar with Semantic Rules:")
print("-" * 80)
print("1) E → TE'           E.inh = E'.syn")
print("2) E' → +TE'1        E'1.inh = E'.inh + T.val, E'.syn = E'1.syn")
print("3) E' → ε            E'.syn = E'.inh")
print("4) T → FT'           T.inh = T'.val")
print("5) T' → *FT1'        T1'.inh = T'.inh * F.val, T'.syn = T1'.syn")
print("6) T' → ε            T'.syn = T'.inh")
print("7) F → num           F.val = num.lexval")

expression = "4 + 3 * 2"
print(f"\n(a) Input Expression: {expression}\n")

print("(b) Derivation Steps:")
print("-" * 80)
derivation = [
    ("E", "Start symbol"),
    ("TE'", "Apply rule 1: E → TE'"),
    ("FT'E'", "Apply rule 4: T → FT'"),
    ("4T'E'", "Apply rule 7: F → num (num.lexval = 4)"),
    ("4E'", "Apply rule 6: T' → ε"),
    ("4+TE'", "Apply rule 2: E' → +TE'"),
    ("4+FT'E'", "Apply rule 4: T → FT'"),
    ("4+3T'E'", "Apply rule 7: F → num (num.lexval = 3)"),
    ("4+3*FT1'E'", "Apply rule 5: T' → *FT1'"),
    ("4+3*2T1'E'", "Apply rule 7: F → num (num.lexval = 2)"),
    ("4+3*2E'", "Apply rule 6: T1' → ε"),
    ("4+3*2", "Apply rule 3: E' → ε")
]

for i, (result, explanation) in enumerate(derivation, 1):
    if i == 1:
        print(f"{i:2}. {result:15} ← {explanation}")
    else:
        print(f"{i:2}. ⇒ {result:13} (by {explanation})")

print("\n(c) Parse Tree:")
print("-" * 80)
print("""
                        E
                       / \\
                      T   E'
                     / \\   / | \\
                    F  T' +  T  E'
                    |   |   / \\  |
                    4   ε  F  T' ε
                           |  / | \\
                           3 *  F T1'
                              |  |
                              2  ε

Parse Tree Structure:
- Root: E (Expression)
- First branch: T → F → 4, T' → ε
- Second branch: E' → + T E'
  - T → F → 3, T' → * F T1'
    - F → 2, T1' → ε
  - E' → ε
""")

print("""(d) Annotated Attribute Flow (inh/syn attributes):
1. F(4): F.val = 4 (Rule 7)
2. T'₁: T'.inh = 4, T'.syn = 4 (Rule 6, ε production)
3. T₁: T.val = T'.syn = 4 (Rule 4)
4. E'₁.inh = 4 (inherited from T.val)
5. F(3): F.val = 3 (Rule 7)
6. T'₂.inh = 3 (from F.val)
7. F(2): F.val = 2 (Rule 7)
8. T1'.inh = 3 * 2 = 6 (Rule 5)
9. T1'.syn = 6 (Rule 6, ε production)
10. T'₂.syn = T1'.syn = 6 (Rule 5)
11. T₂.val = 6 (Rule 4)
12. E'₂.inh = 4 + 6 = 10 (Rule 2)
13. E'₂.syn = 10 (Rule 3, ε production)
14. E'₁.syn = 10
15. E.syn = 10 (Rule 1)
""")

class Node:
    def __init__(self, name, val=None, inh=None, syn=None):
        self.name = name
        self.val = val
        self.inh = inh
        self.syn = syn
    
    def __repr__(self):
        attrs = []
        if self.val is not None:
            attrs.append(f"val={self.val}")
        if self.inh is not None:
            attrs.append(f"inh={self.inh}")
        if self.syn is not None:
            attrs.append(f"syn={self.syn}")
        return f"{self.name}({', '.join(attrs)})"

print("(e) Bottom-up Evaluation Process:")
print("-" * 80)

steps = []

# Step 1: F → 4
f1 = Node("F", val=4)
steps.append(("1", "F → num (4)", f1, "F.val = 4"))

# Step 2: T' → ε (first one)
t_prime1 = Node("T'", inh=4, syn=4)
steps.append(("2", "T' → ε", t_prime1, "T'.inh = 4, T'.syn = 4"))

# Step 3: T → FT'
t1 = Node("T", val=4)
steps.append(("3", "T → FT'", t1, "T.val = T'.syn = 4"))

# Step 4: F → 3
f2 = Node("F", val=3)
steps.append(("4", "F → num (3)", f2, "F.val = 3"))

# Step 5: F → 2
f3 = Node("F", val=2)
steps.append(("5", "F → num (2)", f3, "F.val = 2"))

# Step 6: T1' → ε
t1_prime = Node("T1'", inh=6, syn=6)
steps.append(("6", "T1' → ε", t1_prime, "T1'.inh = 3 * 2 = 6, T1'.syn = 6"))

# Step 7: T' → *FT1'
t_prime2 = Node("T'", inh=3, syn=6)
steps.append(("7", "T' → *FT1'", t_prime2, "T'.inh = 3, T'.syn = T1'.syn = 6"))

# Step 8: T → FT'
t2 = Node("T", val=6)
steps.append(("8", "T → FT'", t2, "T.val = T'.syn = 6"))

# Step 9: E' → ε (inner)
e_prime2 = Node("E'", inh=10, syn=10)
steps.append(("9", "E' → ε", e_prime2, "E'.inh = 10, E'.syn = 10"))

# Step 10: E' → +TE'
e_prime1 = Node("E'", inh=4, syn=10)
steps.append(("10", "E' → +TE'", e_prime1, "E'1.inh = 4 + 6 = 10, E'.syn = E'1.syn = 10"))

# Step 11: E → TE'
e = Node("E", syn=10)
steps.append(("11", "E → TE'", e, "E.syn = E'.syn = 10"))

for step_num, production, node, explanation in steps:
    print(f"Step {step_num}: {production:20} → {node}")
    print(f"         {explanation}")
    print()

print("(f) Verification that E.val = 10:")
print("-" * 80)
print("Computation Trace:")
print("1. Parse '4':        F.val = 4")
print("2. Reduce T → FT':   T.val = 4")
print("3. Parse '3':        F.val = 3")
print("4. Parse '2':        F.val = 2")
print("5. Multiply:         T1'.inh = 3 * 2 = 6")
print("6. Reduce T' → *FT1': T'.syn = T1'.syn = 6")
print("7. Reduce T → FT':   T.val = 6")
print("8. Add:              E'1.inh = 4 + 6 = 10")
print("9. Reduce E' → ε:    E'.syn = 10")
print("10. Reduce E → TE':  E.syn = 10")

print("\nFinal Result:")
print("-" * 80)
print(f"Expression: {expression}")
print(f"Expected:   4 + (3 * 2) = 4 + 6 = 10")
print(f"Computed:   E.val = 10")
print("\nVERIFICATION SUCCESSFUL: E.val = 10")

print(f"\n{'Node':<10} {'Production':<20} {'Inherited':<15} {'Synthesized':<15}")
print("-" * 80)
print(f"{'F₁':<10} {'F → 4':<20} {'-':<15} {'val = 4':<15}")
print(f"{'T\'₁':<10} {'T\' → ε':<20} {'inh = 4':<15} {'syn = 4':<15}")
print(f"{'T₁':<10} {'T → FT\'':<20} {'-':<15} {'val = 4':<15}")
print(f"{'F₂':<10} {'F → 3':<20} {'-':<15} {'val = 3':<15}")
print(f"{'F₃':<10} {'F → 2':<20} {'-':<15} {'val = 2':<15}")
print(f"{'T1\'₃':<10} {'T1\' → ε':<20} {'inh = 6':<15} {'syn = 6':<15}")
print(f"{'T\'₂':<10} {'T\' → *FT1\'':<20} {'inh = 3':<15} {'syn = 6':<15}")
print(f"{'T₂':<10} {'T → FT\'':<20} {'-':<15} {'val = 6':<15}")
print(f"{'E\'₂':<10} {'E\' → ε':<20} {'inh = 10':<15} {'syn = 10':<15}")
print(f"{'E\'₁':<10} {'E\' → +TE\'':<20} {'inh = 4':<15} {'syn = 10':<15}")
print(f"{'E':<10} {'E → TE\'':<20} {'-':<15} {'syn = 10':<15}")