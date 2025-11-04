# DFA for (b*ab*)* | b*
# We'll use DFA that accepts strings containing at least one 'a'

def dfa_contains_a(string, verbose=False):
    state = 'q0'
    for ch in string:
        if ch not in ('a', 'b'):
            raise ValueError("Only 'a' or 'b' allowed.")
        if state == 'q0':
            if ch == 'a':
                state = 'q1'
        # Once in q1, it stays in q1 for any input
        if verbose:
            print(f"Read {ch} -> {state}")
    if verbose:
        print("ACCEPT" if state == 'q1' else "REJECT")
    return state == 'q1'


# Testing
accepted = ["a", "ba", "abb", "babab", "aa"]
rejected = ["", "b", "bb", "bbbb", "bbb"]

print("\nTask 3: (b*ab*)* | b*")
print("Accepted:")
for s in accepted:
    print(s, "->", dfa_contains_a(s))

print("\nRejected:")
for s in rejected:
    print(s, "->", dfa_contains_a(s))
