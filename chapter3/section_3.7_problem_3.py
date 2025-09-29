# Problem: Convert NFA to DFA using subset construction.

nfa = {
    0: {"a": [0, 1], "b": [0]},  # same NFA as before
    1: {"b": [2]},
    2: {}
}

accept_states = {2}

def nfa_to_dfa(nfa, start, accept):
    dfa = {}
    unmarked = [frozenset([start])]
    marked = set()
    dfa_accept = set()

    while unmarked:
        current = unmarked.pop()
        if current in marked:
            continue
        marked.add(current)

        dfa[current] = {}
        for symbol in {"a", "b"}:  # alphabet
            next_states = set()
            for state in current:
                if symbol in nfa[state]:
                    next_states.update(nfa[state][symbol])
            next_set = frozenset(next_states)
            if next_set:
                dfa[current][symbol] = next_set
                if next_set not in marked:
                    unmarked.append(next_set)
            if next_states & accept:
                dfa_accept.add(next_set)

    return dfa, dfa_accept

dfa, dfa_accept = nfa_to_dfa(nfa, 0, accept_states)

print("DFA Transition Table:")
for state, trans in dfa.items():
    print(f"{state} -> {trans}")
print("Accepting States:", dfa_accept)
