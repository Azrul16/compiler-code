# Problem: Construct NFA for regex a* (zero or more 'a's).
# Accepts "", "a", "aa", "aaa", ...

def nfa_regex_a_star(string):
    return all(ch == "a" for ch in string)  # only 'a's allowed

tests = ["", "a", "aa", "aaa", "b", "ab"]
for t in tests:
    print(f"{t}: {nfa_regex_a_star(t)}")
