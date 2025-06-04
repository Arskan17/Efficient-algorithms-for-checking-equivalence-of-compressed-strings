from collections import Counter
import json

class SLP:
    def __init__(self):
        self.rules = {}          # A → (B, C)
        self.reverse_rules = {}  # (B, C) → A
        self.symbol_counter = 1
        self.start = None

    def new_nonterminal(self):
        nt = f'X{self.symbol_counter}'
        self.symbol_counter += 1
        return nt

    def repair(self, input_string):
        sequence = list(input_string)

        # Step 1: Re-Pair compression
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

            # Replace all occurrences of the pair
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

        # Step 2: Only wrap remaining sequence if needed
        self.start = self._final_wrap(sequence)
        return self

    def _final_wrap(self, sequence):
        """Turn the leftover sequence into a single nonterminal, using as few new rules as possible."""
        if len(sequence) == 1:
            return sequence[0]  # Done!

        # Build a binary tree bottom-up, but reuse existing rules when possible
        while len(sequence) > 1:
            new_seq = []
            i = 0
            while i < len(sequence):
                if i + 1 < len(sequence):
                    a, b = sequence[i], sequence[i+1]
                    if (a, b) in self.reverse_rules:
                        nt = self.reverse_rules[(a, b)]
                    else:
                        nt = self.new_nonterminal()
                        self.rules[nt] = (a, b)
                        self.reverse_rules[(a, b)] = nt
                    new_seq.append(nt)
                    i += 2
                else:
                    new_seq.append(sequence[i])
                    i += 1
            sequence = new_seq

        return sequence[0]

    def print_rules(self):
        print(f"Start symbol: {self.start}")
        for lhs, (rhs1, rhs2) in self.rules.items():
            print(f"{lhs} → {rhs1} {rhs2}")

    def save_to_json(self, filepath):
        data = {lhs: list(rhs) for lhs, rhs in self.rules.items()}
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    # s = "abababbabbababbbabaababbabbabbabbababbabbabbababbabababbababbbabbaababbababbabababbabababbbabbabababbabbaba"
    file = "test_string_re-pair.txt"
    with open(f"{file}", "r") as f:
        s = f.read()
    slp = SLP()
    slp.repair(s)
    print(f"Done compressing {file}")
    slp.save_to_json(f"testing_dataset/random_strings_SLP/{file}_size-605264_SLP_11.json")