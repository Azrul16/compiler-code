# NFA for (a|b)*a

nfa = {
    'q0': {'a': ['q0', 'q1'], 'b': ['q0']},
    'q1': {}
}
start_state = 'q0'
accept_states = {'q1'}

def nfa_accept(string, current_states=None):
    if current_states is None:
        current_states = {start_state}
    for ch in string:
        next_states = set()
        for state in current_states:
            if ch in nfa[state]:
                next_states.update(nfa[state][ch])
        current_states = next_states
    return bool(current_states & accept_states)

# Testing
accepted = ["a", "ba", "aba", "bba", "abba"]
rejected = ["", "b", "bb", "abb", "bab"]

print("\nTask 2: (a|b)*a")
print("Accepted:")
for s in accepted:
    print(s, "->", nfa_accept(s))

print("\nRejected:")
for s in rejected:
    print(s, "->", nfa_accept(s))
