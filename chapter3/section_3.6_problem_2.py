# Problem: Build DFA using transition table and simulate it.
# DFA accepts binary strings with even number of 0's.

dfa_table = {
    "q0": {"0": "q1", "1": "q0"},  # start (q0) is even
    "q1": {"0": "q0", "1": "q1"}   # q1 means odd number of 0's
}

start_state = "q0"
accept_states = {"q0"}

def simulate_dfa(string):
    state = start_state
    for ch in string:
        state = dfa_table[state].get(ch, None)
        if state is None:
            return False
    return state in accept_states

# Example usage:
tests = ["", "0", "00", "1010", "1100"]
for t in tests:
    print(f"{t}: {simulate_dfa(t)}")
