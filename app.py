from itertools import combinations # https://docs.python.org/3/library/itertools.html#itertools.combinations
import input

def compute_all_pairs(grammar):
    nonterminals = set(grammar.keys())  # Collect all nonterminals
    S = set(combinations(nonterminals, 2))  # Generate all pairs
    return S

def compute_lengths(grammar):
    lengths = {}

    def get_length(symbol):
        if symbol in lengths:  # Memoization
            return lengths[symbol]
        if symbol not in grammar:  # Base case (it's a terminal)
            return 1
        lengths[symbol] = sum(get_length(s) for s in grammar[symbol])  # Recursive sum
        return lengths[symbol]

    for nonterminal in grammar:
        get_length(nonterminal)  # Compute length for each nonterminal

    return lengths

if __name__ == '__main__':
    grammar = input.G
    lengths = compute_lengths(grammar)
    print(lengths)
    S = compute_all_pairs(G)
    print(S)