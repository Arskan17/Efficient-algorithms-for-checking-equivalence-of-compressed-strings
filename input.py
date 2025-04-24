# Replace with your grammar. Every key is a nonterminal and its value is a list of symbols, which are either terminals or nonterminals.

# G = {"X": ["Y","Z"], "Y": ["Z","Z"], "Z": ["a","b"],
#          "T": ["U","b"], "U": ["a","V"], "V": ["W","W"], "W": ["b","a"]}
# S = {("X","T")}

# G = {
#         "X": ["Y", "Z"],        "Y": ["A", "B"],        "Z": ["C", "D"],        "A": ["a", "b"],        "B": ["a", "b"],        "C": ["a", "b"],        "D": ["a", "b"],
#         "T": ["U", "V"],        "U": ["E", "F"],        "V": ["G", "H"],        "E": ["a", "b"],        "F": ["a", "b"],        "G": ["a", "b"],        "H": ["a", "b"]
#     }
# S = {("X", "T")}

G = {
    "A": ["B", "D"],    "B": ["E", "F"],    "D": ["b", "b"],    "E": ["a", "a"],    "F": ["C", "C"],    "C": ["b", "a"],
    "X": ["Y", "Z"],    "Y": ["a", "R"],    "Z": ["R", "S"],    "R": ["a", "b"],    "S": ["R", "b"]
    }
S = {("A", "X")}

old_G = [
    # 0. Simple Grammar
    {
    "S": ["A", "B"], # S → AB
    "A": ["a", "C"], # 𝐴 → XC
    "X": ["a"], # 𝑋 → 𝑎
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