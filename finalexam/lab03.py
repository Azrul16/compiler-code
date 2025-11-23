def first_set(grammar, nt, first, computed):
    if nt in computed: return first[nt]
    for prod in grammar[nt]:
        if prod == ['ε']:
            first[nt].add('ε')
            continue
        for sym in prod:
            if sym not in grammar:
                first[nt].add(sym)
                break
            else:
                first[nt].update(first_set(grammar, sym, first, computed) - {'ε'})
                if 'ε' not in first[sym]: break
        else:
            first[nt].add('ε')
    computed.add(nt)
    return first[nt]

def follow_set(grammar, first):
    follow = {nt: set() for nt in grammar}
    follow[list(grammar.keys())[0]].add('$')
    for _ in range(5):
        for nt in grammar:
            for prod in grammar[nt]:
                for i, sym in enumerate(prod):
                    if sym in grammar:
                        rest = prod[i+1:]
                        if not rest:
                            follow[sym].update(follow[nt])
                        else:
                            for ns in rest:
                                if ns not in grammar:
                                    follow[sym].add(ns)
                                    break
                                else:
                                    follow[sym].update(first[ns] - {'ε'})
                                    if 'ε' not in first[ns]: break
                            else:
                                follow[sym].update(follow[nt])
    return follow

grammar = {
    'E': [['T', "E'"], ['ε']],
    "E'": [['+', 'T', "E'"], ['ε']],
    'T': [['F', "T'"]],
    "T'": [['*', 'F', "T'"], ['ε']],
    'F': [['(', 'E', ')'], ['id']]
}

print("FIRST AND FOLLOW SETS")
print("Grammar: E -> TE'|e, E' -> +TE'|e, T -> FT', T' -> *FT'|e, F -> (E)|id\n")

first = {nt: set() for nt in grammar}
computed = set()
for nt in grammar:
    first_set(grammar, nt, first, computed)

print("FIRST SETS:")
for nt in grammar:
    items = sorted(first[nt], key=lambda x: (x == 'ε', x))
    items_str = ', '.join(['e' if x == 'ε' else x for x in items])
    print(f"FIRST({nt:3}) = {{ {items_str} }}")

follow = follow_set(grammar, first)
print("\nFOLLOW SETS:")
for nt in grammar:
    items = sorted(follow[nt], key=lambda x: (x == '$', x))
    print(f"FOLLOW({nt:3}) = {{ {', '.join(items)} }}")

# PART 2: Three Address Code
class TAC:
    def __init__(self):
        self.temp_count = 0
        self.code = []
    
    def newtemp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def emit(self, result, arg1, op=None, arg2=None):
        if op is None:
            self.code.append(f"{result} = {arg1}")
        elif arg2 is None:  # Unary operation
            self.code.append(f"{result} = {op} {arg1}")
        else:
            self.code.append(f"{result} = {arg1} {op} {arg2}")
        return result
    
    def parse(self, expr):
        expr = expr.replace(' ', '')
        if '=' in expr:
            var, rhs = expr.split('=', 1)
            self.emit(var, self.parse_expr(rhs))
            return var
        return self.parse_expr(expr)
    
    def parse_expr(self, s):
        depth = 0
        for i in range(len(s)-1, -1, -1):
            if s[i] == ')': depth += 1
            elif s[i] == '(': depth -= 1
            elif depth == 0 and s[i] == '+' and i > 0 and s[i-1] not in '(+-*/':
                return self.emit(self.newtemp(), self.parse_expr(s[:i]), '+', self.parse_term(s[i+1:]))
        return self.parse_term(s)
    
    def parse_term(self, s):
        depth = 0
        for i in range(len(s)-1, -1, -1):
            if s[i] == ')': depth += 1
            elif s[i] == '(': depth -= 1
            elif depth == 0 and s[i] == '*' and i > 0 and s[i-1] not in '(+-*/':
                return self.emit(self.newtemp(), self.parse_term(s[:i]), '*', self.parse_unary(s[i+1:]))
        return self.parse_unary(s)
    
    def parse_unary(self, s):
        if s.startswith('-'):
            return self.emit(self.newtemp(), self.parse_unary(s[1:]), '-')
        return self.parse_primary(s)
    
    def parse_primary(self, s):
        return self.parse_expr(s[1:-1]) if s.startswith('(') and s.endswith(')') else s

print("\n")
print("THREE ADDRESS CODE")
expr = "a = (-c * b) + (-c * d)"
print(f"\nExpression: {expr}\n")

gen = TAC()
gen.parse(expr)
for i, code in enumerate(gen.code, 1):
    print(f"{i}. {code}")
