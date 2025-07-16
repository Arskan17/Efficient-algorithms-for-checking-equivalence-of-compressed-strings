from collections import Counter
import json

class SLP:
    def __init__(self):
        self.rules = {}          # A -> (B, C) where A, B, C ∈ Σ ∪ V
        self.reverse_rules = {}  # map (rhs1, rhs2) -> lhs
        self.symbol_counter = 1
        self.start = None

    def new_nonterminal(self):
        nt = f'X{self.symbol_counter}'
        self.symbol_counter += 1
        return nt

    def repair(self, input_string):
        sequence = list(input_string)

        # Step 1: apply Re-Pair
        while True:
            pairs = [(sequence[i], sequence[i + 1]) for i in range(len(sequence) - 1)]
            freq = Counter(pairs)
            most_common = freq.most_common(1)

            if not most_common or most_common[0][1] < 2:
                break

            pair, _ = most_common[0]

            if pair in self.reverse_rules:
                nt = self.reverse_rules[pair]
            else:
                nt = self.new_nonterminal()
                self.rules[nt] = pair
                self.reverse_rules[pair] = nt

            # Replace occurrences of the pair
            i = 0
            new_sequence = []
            while i < len(sequence):
                if i < len(sequence) - 1 and (sequence[i], sequence[i + 1]) == pair:
                    new_sequence.append(nt)
                    i += 2
                else:
                    new_sequence.append(sequence[i])
                    i += 1

            sequence = new_sequence

        # Step 2: Flatten final sequence into one start symbol
        self.start = self.sequence_to_binary_tree(sequence)
        return self

    def sequence_to_binary_tree(self, symbols):
        """Convert a sequence of symbols into a binary SLP rooted at a new start symbol."""
        while len(symbols) > 1:
            new_symbols = []
            i = 0
            while i < len(symbols):
                if i + 1 < len(symbols):
                    a, b = symbols[i], symbols[i + 1]
                    if (a, b) in self.reverse_rules:
                        nt = self.reverse_rules[(a, b)]
                    else:
                        nt = self.new_nonterminal()
                        self.rules[nt] = (a, b)
                        self.reverse_rules[(a, b)] = nt
                    new_symbols.append(nt)
                    i += 2
                else:
                    # Odd symbol left over
                    new_symbols.append(symbols[i])
                    i += 1
            symbols = new_symbols
        return symbols[0]

    def print_rules(self):
        print(f"Start symbol: {self.start}")
        for lhs, rhs in self.rules.items():
            print(f"{lhs} → {rhs[0]} {rhs[1]}")

    def save_to_json(self, filepath):
        data = {lhs: list(rhs) for lhs, rhs in self.rules.items()}
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    s = "abbabba"
    # file = "dna.50MB"
    # with open(f"pizza&chille corpus/{file}", "r") as f:
    #     s = f.read()
    slp = SLP()
    slp.repair(s)
    # print(f"Done compressing {file}")
    # slp.save_to_json(f"testing_dataset/pizza&chille corpus_SLP/{file}_SLP.json")
    slp.print_rules()
