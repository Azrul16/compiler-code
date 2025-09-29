# Problem: Construct NFA for regex a* (any number of 'a's).
# Accepts "", "a", "aa", "aaa", ...

def nfa_a_star(string):
    # Simple simulation: accepts if all chars are 'a'
    return all(ch == "a" for ch in string)

tests = ["", "a", "aa", "b", "ab"]
for t in tests:
    print(f"{t}: {nfa_a_star(t)}")
