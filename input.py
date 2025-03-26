# Replace with your grammar. Every key is a nonterminal and its value is a list of symbols, which are either terminals or nonterminals.
G = {
    "S": ["A", "B"], # S → AB
    "A": ["a", "C"], # 𝐴 → 𝑎C
    "C": ["b", "c"], # C → bc
    "B": ["d"] # 𝐵 → 𝑑
}


#Alternative compact array representation
# G = {
#     4: (2, 3),  # X4 = X2 X3
#     2: "ab",    # X2 = "ab"
#     3: "cd"     # X3 = "cd"
# }