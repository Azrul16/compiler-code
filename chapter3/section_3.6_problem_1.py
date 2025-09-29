# Problem: Implement a DFA simulator in Python.
# DFA accepts binary strings ending with '01'.

def dfa_accepts(string):
    # DFA states: q0 (start), q1, q2 (accept), dead
    state = "q0"
    for ch in string:
        if state == "q0":
            state = "q1" if ch == "0" else "q0"
        elif state == "q1":
            state = "q2" if ch == "1" else "q1"
        elif state == "q2":
            state = "q2" if ch in "01" else "dead"
        else:
            state = "dead"

    return state == "q2"

# Example usage:
tests = ["01", "001", "1001", "111", "110"]
for t in tests:
    print(f"{t}: {dfa_accepts(t)}")
