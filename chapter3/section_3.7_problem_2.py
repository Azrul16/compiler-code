# Problem: Simulate NFA with epsilon transitions.
# Regex: (a|b)*ab (all strings ending with "ab")

from collections import defaultdict

nfa = {
    0: {"a": [0, 1], "b": [0]},  # loop on a|b, go to q1 on 'a'
    1: {"b": [2]},               # q1 -> q2 on 'b'
    2: {}                        # accept state
}

start_state = 0
accept_states = {2}

def simulate_nfa(nfa, string, start, accept):
    states = {start}
    for ch in string:
        next_states = set()
        for s in states:
            if ch in nfa[s]:
                next_states.update(nfa[s][ch])
        states = next_states
    return bool(states & accept)

# Example usage
tests = ["ab", "aab", "babab", "aaa", "bb"]
for t in tests:
    print(f"{t}: {simulate_nfa(nfa, t, start_state, accept_states)}")
