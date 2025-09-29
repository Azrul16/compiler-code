# Problem: Use the DFA obtained to test strings

# Define the DFA transition table
dfa = {
    frozenset([0]): {'a': frozenset([1]), 'b': frozenset([2])},
    frozenset([1]): {'a': frozenset([1]), 'b': frozenset([2])},
    frozenset([2]): {'a': frozenset([1]), 'b': frozenset([2])}
}

# Define accepting states
dfa_accept = {frozenset([2])}

def simulate_dfa(dfa, start, accept, string):
    state = frozenset([start])
    for ch in string:
        if ch in dfa[state]:
            state = dfa[state][ch]
        else:
            return False
    return state in accept

# Example usage:
tests = ["ab", "aab", "babab", "aaa", "bb"]
for t in tests:
    print(f"{t}: {simulate_dfa(dfa, 0, dfa_accept, t)}")
