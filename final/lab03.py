from collections import defaultdict

grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F": [["(", "E", ")"], ["id"]],
}

FIRST = defaultdict(set)
FOLLOW = defaultdict(set)

def compute_first(symbol):
    if not symbol.isupper():
        return {symbol}
    for production in grammar[symbol]:
        for sym in production:
            first_of_sym = compute_first(sym)
            FIRST[symbol].update(first_of_sym - {'ε'})
            if 'ε' not in first_of_sym:
                break
        else:
            FIRST[symbol].add('ε')
    return FIRST[symbol]

def compute_follow():
    FOLLOW['E'].add('$')
    changed = True
    while changed:
        changed = False
        for head, bodies in grammar.items():
            for body in bodies:
                for i, B in enumerate(body):
                    if B.isupper():
                        first_of_beta = set()
                        for sym in body[i+1:]:
                            first_of_sym = compute_first(sym)
                            first_of_beta.update(first_of_sym - {'ε'})
                            if 'ε' not in first_of_sym:
                                break
                        else:
                            if not FOLLOW[head].issubset(FOLLOW[B]):
                                FOLLOW[B].update(FOLLOW[head])
                                changed = True
                        if not first_of_beta.issubset(FOLLOW[B]):
                            FOLLOW[B].update(first_of_beta)
                            changed = True

for nonterminal in grammar:
    compute_first(nonterminal)
compute_follow()

print("FIRST sets:")
for nt in FIRST:
    print(f"FIRST({nt}) = {FIRST[nt]}")

print("\nFOLLOW sets:")
for nt in FOLLOW:
    print(f"FOLLOW({nt}) = {FOLLOW[nt]}")


# ----- Three Address Code Generation -----
temp_count = 1
def new_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def three_address_code():
    print("\nGenerating three-address code for: a = (-c * b) + (-c * d)")
    t1 = new_temp(); print(f"{t1} = -c")
    t2 = new_temp(); print(f"{t2} = {t1} * b")
    t3 = new_temp(); print(f"{t3} = -c")
    t4 = new_temp(); print(f"{t4} = {t3} * d")
    t5 = new_temp(); print(f"{t5} = {t2} + {t4}")
    print(f"a = {t5}")

three_address_code()
