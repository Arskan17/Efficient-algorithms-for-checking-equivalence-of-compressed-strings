import json
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Union

class RePairCompressor:
    def __init__(self, nonterminal:str):
        self.grammar = {}
        self.rule_counter = 0
        self.start_symbol = None
        self.nonterminal = nonterminal
    
    def _generate_rule_name(self) -> str:
        """Generate a new rule name (F1, F2, F3, ...)"""
        self.rule_counter += 1
        return f"{self.nonterminal}{self.rule_counter}"
    
    def _count_pairs(self, sequence: List[str]) -> Counter:
        """Count all adjacent pairs in the sequence"""
        pairs = Counter()
        for i in range(len(sequence) - 1):
            pair = (sequence[i], sequence[i + 1])
            pairs[pair] += 1
        return pairs
    
    def _replace_pair(self, sequence: List[str], target_pair: Tuple[str, str], replacement: str) -> List[str]:
        """Replace all occurrences of target_pair with replacement in sequence"""
        result = []
        i = 0
        while i < len(sequence):
            if i < len(sequence) - 1 and (sequence[i], sequence[i + 1]) == target_pair:
                result.append(replacement)
                i += 2  # Skip both elements of the pair
            else:
                result.append(sequence[i])
                i += 1
        return result
    
    def _update_grammar_rules(self, old_pair: Tuple[str, str], new_rule: str):
        """Update all existing grammar rules by replacing the pair with new rule"""
        # Only update existing rules, not the newly created one
        rules_to_update = list(self.grammar.keys())
        if new_rule in rules_to_update:
            rules_to_update.remove(new_rule)
        
        for rule_name in rules_to_update:
            self.grammar[rule_name] = self._replace_pair(
                self.grammar[rule_name], old_pair, new_rule
            )
    
    def compress(self, text: str) -> Dict[str, List[str]]:
        """
        Compress a string using the Re-Pair algorithm to produce CFG in CNF
        
        Args:
            text: Input string to compress
            
        Returns:
            Dictionary representing the grammar rules in CNF format
        """
        # Initialize with individual characters
        sequence = list(text)
        
        # Reset state
        self.grammar = {}
        self.rule_counter = 0
        self.start_symbol = None
        
        while True:
            # Count all pairs in the current sequence
            pair_counts = self._count_pairs(sequence)
            
            # Also count pairs in all existing grammar rules
            for rule_name, rule_body in self.grammar.items():
                rule_pairs = self._count_pairs(rule_body)
                for pair, count in rule_pairs.items():
                    pair_counts[pair] += count
            
            # Find the most frequent pair (must occur at least twice)
            if not pair_counts or max(pair_counts.values()) < 2:
                break
            
            # Get the most frequent pair
            most_frequent_pair = max(pair_counts, key=pair_counts.get)
            
            # Create new rule - store as list with exactly 2 elements
            new_rule = self._generate_rule_name()
            self.grammar[new_rule] = [most_frequent_pair[0], most_frequent_pair[1]]
            
            # Replace the pair in the main sequence
            sequence = self._replace_pair(sequence, most_frequent_pair, new_rule)
            
            # Update all existing grammar rules (but not the newly created one)
            self._update_grammar_rules(most_frequent_pair, new_rule)
        
        # Handle the final sequence to create proper CNF
        while len(sequence) > 1:
            if len(sequence) == 2:
                # Create final rule with exactly 2 symbols
                start_rule = self._generate_rule_name()
                self.grammar[start_rule] = [sequence[0], sequence[1]]
                self.start_symbol = start_rule
                break
            else:
                # If more than 2 symbols, we need to create binary rules
                # Take the first two symbols and create a rule
                new_rule = self._generate_rule_name()
                self.grammar[new_rule] = [sequence[0], sequence[1]]
                
                # Replace the first two symbols with the new rule
                sequence = [new_rule] + sequence[2:]
        
        # If only one symbol remains, it's the start symbol
        if len(sequence) == 1:
            self.start_symbol = sequence[0]
        elif len(sequence) == 0:
            self.start_symbol = ""
        
        return self.grammar
    
    def get_start_symbol(self) -> str:
        """Get the start symbol of the grammar"""
        return self.start_symbol
    
    def get_grammar_with_start(self) -> Dict[str, Union[List[str], str]]:
        """Get grammar with explicit start symbol"""
        result = dict(self.grammar)
        result['_start'] = self.start_symbol
        return result
    
    def decompress(self, grammar: Dict[str, List[str]], start_symbol: str = None) -> str:
        """
        Decompress a grammar back to the original string
        
        Args:
            grammar: Grammar rules dictionary
            start_symbol: Starting symbol
            
        Returns:
            Decompressed string
        """
        if start_symbol is None:
            # Find the rule with the highest number as start symbol
            rule_numbers = []
            for rule in grammar.keys():
                if rule.startswith('F'):
                    try:
                        rule_numbers.append(int(rule[1:]))
                    except ValueError:
                        continue
            start_symbol = f"F{max(rule_numbers)}" if rule_numbers else ""
        
        def expand(symbol: str) -> str:
            if symbol not in grammar:
                return symbol  # Terminal symbol (original character)
            
            result = ""
            for sub_symbol in grammar[symbol]:
                result += expand(sub_symbol)
            return result
        
        return expand(start_symbol)
    
    def save_grammar(self, grammar: Dict[str, List[str]], filename: str):
        """Save grammar to a JSON file with start symbol information"""        
        with open(filename, 'w') as f:
            json.dump(dict(grammar), f, indent=2)


def main():
    # Example usage
    nonterminal = "F"
    compressor = RePairCompressor(nonterminal=nonterminal)

    test_string = "atscgghgfcttashffggccffghttgassta"
    print(f"Original string: {test_string}")
    
    grammar = compressor.compress(test_string)
    start_symbol = compressor.get_start_symbol()
    
    print(f"Compressed grammar: {grammar}")
    print(f"Start symbol: {start_symbol}")
    
    # Save to file
    file_name = f"test_string_re-pair_size{len(test_string)}_{nonterminal}.json"
    compressor.save_grammar(grammar, f"testing_dataset/random_strings_SLP/{file_name}")
    print("Grammar saved to {file_name}")
    
    # Test decompression
    decompressed = compressor.decompress(grammar, start_symbol)
    print(f"Decompressed string: {decompressed}")
    print(f"Compression successful: {test_string == decompressed}")
    
    print("\n" + "#"*50 + "\n")

if __name__ == "__main__":
    main()