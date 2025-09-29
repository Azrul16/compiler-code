# Problem: Simulate NFA using epsilon-closure and state transitions.
# NFA accepts strings over {a,b} ending with "ab".

from collections import defaultdict

# NFA transition table with epsilon (ε) transitions
# Format: {state: {symbol: [next_states]}}
nfa = {
    0: {"a": [0, 1], "b": [0]},  # loop on 'a' or 'b', move to q1 on 'a'
    1: {"b": [2]},               # q1 goes to q2 on 'b'
    2: {}                        # accepting state
}

start_state = 0
accept_states = {2}

def nfa_simulate(nfa, string, start, accept):
    current_states = {start}
    for ch in string:
        next_states = set()
        for state in current_states:
            if ch in nfa[state]:
                next_states.update(nfa[state][ch])
        current_states = next_states
    return len(current_states & accept) > 0

# Example usage:
tests = ["ab", "aab", "babab", "aaa", "bb"]
for t in tests:
    print(f"{t}: {nfa_simulate(nfa, t, start_state, accept_states)}")
