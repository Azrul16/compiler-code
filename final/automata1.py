# DFA for even number of 1's

def dfa_even_ones(string, verbose=False):
    state = 'q0'  # start in even
    for ch in string:
        if ch not in ('0', '1'):
            raise ValueError("Only binary strings allowed.")
        if state == 'q0':
            state = 'q0' if ch == '0' else 'q1'
        else:  # q1
            state = 'q1' if ch == '0' else 'q0'
        if verbose:
            print(f"Read {ch} -> {state}")
    if verbose:
        print("ACCEPT" if state == 'q0' else "REJECT")
    return state == 'q0'


# Example simulation:
dfa_even_ones("1101010", verbose=True)

# Testing
accepted = ["", "0", "11", "1010", "1101010"]
rejected = ["1", "10", "111", "1011", "001"]

print("\nAccepted:")
for s in accepted:
    print(s, "->", dfa_even_ones(s))

print("\nRejected:")
for s in rejected:
    print(s, "->", dfa_even_ones(s))
