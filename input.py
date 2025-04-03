# Replace with your grammar. Every key is a nonterminal and its value is a list of symbols, which are either terminals or nonterminals.
G = [
    # 0. Simple Grammar
    {
    "S": ["A", "B"], # S → AB
    "A": ["a", "C"], # 𝐴 → 𝑎C
    "B": ["d"], # 𝐵 → 𝑑
    "C": ["b", "c"] # C → bc
    },
    # 1.
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["a"],
    "D": ["b"],
    "E": ["c"],
    "F": ["d"]
    },
    # 2.
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["G", "H"],
    "D": ["i"],
    "E": ["j"],
    "F": ["k"],
    "G": ["l"],
    "H": ["m"]
    },
    # 3. More Branching
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["G", "H"],
    "D": ["I", "J"],
    "E": ["K", "L"],
    "F": ["M", "N"],
    "G": ["o"],
    "H": ["p"],
    "I": ["q"],
    "J": ["r"],
    "K": ["s"],
    "L": ["t"],
    "M": ["u"],
    "N": ["v"]
    },
    # 4. Indirect Dependencies
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["G", "H"],
    "D": ["E", "I"],
    "E": ["j"],
    "F": ["k"],
    "G": ["l"],
    "H": ["m"],
    "I": ["n"]
    },
    # 5. Multiple Productions Per Nonterminal
    {
    "S": ["A", "B"],
    "A": ["X", "E"],
    "X": ["C", "D"],
    "B": ["Y", "H"],
    "Y": ["F", "G"],
    "C": ["i"],
    "D": ["j"],
    "E": ["k"],
    "F": ["l"],
    "G": ["m"],
    "H": ["n"]
    },
    # 6. Deeply Nested Nonterminals
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "C": ["E", "F"],
    "E": ["G", "H"],
    "G": ["i"],
    "H": ["j"],
    "F": ["k"],
    "D": ["l"],
    "B": ["m"]
    },
    # 7. Balanced Tree Structure
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["G", "H"],
    "D": ["I", "J"],
    "E": ["K", "L"],
    "F": ["M", "N"],
    "G": ["o"],
    "H": ["p"],
    "I": ["q"],
    "J": ["r"],
    "K": ["s"],
    "L": ["t"],
    "M": ["u"],
    "N": ["v"]
    },
    # 8. Interleaved Dependencies
    {
    "S": ["A", "B"],
    "A": ["C", "D"],
    "B": ["E", "F"],
    "C": ["G", "H"],
    "D": ["I", "J"],
    "E": ["K", "L"],
    "F": ["M", "N"],
    "G": ["D", "O"],
    "H": ["P"],
    "I": ["Q"],
    "J": ["R"],
    "K": ["S"],
    "L": ["T"],
    "M": ["U"],
    "N": ["V"],
    "O": ["w"],
    "P": ["x"],
    "Q": ["y"],
    "R": ["z"],
    "S": ["1"],
    "T": ["2"],
    "U": ["3"],
    "V": ["4"]
    },
    # # 9. Recursion
    # {
    # "S": ["A", "B"],
    # "A": ["X", "E"],
    # "X": ["C", "D"],
    # "C": ["A", "F"],
    # "D": ["g"],
    # "E": ["h"],
    # "F": ["i"]
    # },
    # # 10. A More Complex Recursion Structure
    # {
    # "S": ["A", "B"],
    # "A": ["C", "D"],
    # "B": ["E", "F"],
    # "C": ["A", "G"],
    # "D": ["H", "I"],
    # "E": ["J", "K"],
    # "F": ["L", "M"],
    # "G": ["N"],
    # "H": ["O"],
    # "I": ["P"],
    # "J": ["Q"],
    # "K": ["R"],
    # "L": ["S"],
    # "M": ["T"],
    # "N": ["u"],
    # "O": ["v"],
    # "P": ["w"],
    # "Q": ["x"],
    # "R": ["y"],
    # "S": ["z"],
    # "T": ["1"]
    # }
]


#Alternative compact array representation
# G = {
#     4: (2, 3),  # X4 = X2 X3
#     2: "ab",    # X2 = "ab"
#     3: "cd"     # X3 = "cd"
# }