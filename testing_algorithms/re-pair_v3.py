import json
import time
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
        """Pair counting using a single pass"""
        pairs = Counter()
        for i in range(len(sequence) - 1):
            pair = (sequence[i], sequence[i + 1])
            pairs[pair] += 1
        return pairs
    
    def _replace_pair(self, sequence: List[str], target_pair: Tuple[str, str], replacement: str) -> List[str]:
        """Pair replacement"""
        if len(sequence) < 2:
            return sequence
        
        result = []
        i = 0
        while i < len(sequence):
            if i < len(sequence) - 1 and sequence[i] == target_pair[0] and sequence[i + 1] == target_pair[1]:
                result.append(replacement)
                i += 2
            else:
                result.append(sequence[i])
                i += 1
        return result
    
    def _update_grammar_rules(self, old_pair: Tuple[str, str], new_rule: str):
        """Grammar rule updates"""
        for rule_name in list(self.grammar.keys()):
            if rule_name != new_rule:  # Don't update the newly created rule
                self.grammar[rule_name] = self._replace_pair(
                    self.grammar[rule_name], old_pair, new_rule
                )
    
    def compress(self, text: str, progress_callback=None) -> Dict[str, List[str]]:
        """
        Compress a string using optimized Re-Pair algorithm
        
        Args:
            text: Input string to compress
            progress_callback: Optional callback function for progress updates
            
        Returns:
            Dictionary representing the grammar rules in CNF format
        """
        # Convert to list once
        sequence = list(text)
        original_length = len(sequence)
        
        # Reset state
        self.grammar = {}
        self.rule_counter = 0
        self.start_symbol = None
        
        iteration = 0
        start_time = time.time()
        
        while True:
            iteration += 1
            
            # Progress reporting
            if progress_callback and iteration % 10 == 0:
                current_time = time.time()
                elapsed = current_time - start_time
                progress_callback(iteration, len(sequence), original_length, elapsed)
            
            # Count pairs in main sequence
            pair_counts = self._count_pairs(sequence)
            
            # Count pairs in grammar rules
            for rule_body in self.grammar.values():
                if len(rule_body) >= 2:
                    rule_pairs = self._count_pairs(rule_body)
                    for pair, count in rule_pairs.items():
                        pair_counts[pair] += count
            
            # Find most frequent pair
            if not pair_counts:
                break
            
            max_count = max(pair_counts.values())
            if max_count < 2:
                break
            
            # Get the most frequent pair
            most_frequent_pair = max(pair_counts, key=pair_counts.get)
            
            # Create new rule
            new_rule = self._generate_rule_name()
            self.grammar[new_rule] = [most_frequent_pair[0], most_frequent_pair[1]]
            
            # Replace in main sequence
            sequence = self._replace_pair(sequence, most_frequent_pair, new_rule)
            
            # Update grammar rules
            self._update_grammar_rules(most_frequent_pair, new_rule)
        
        # Handle final sequence
        while len(sequence) > 1:
            if len(sequence) == 2:
                start_rule = self._generate_rule_name()
                self.grammar[start_rule] = [sequence[0], sequence[1]]
                self.start_symbol = start_rule
                break
            else:
                # Create binary tree for longer sequences
                new_rule = self._generate_rule_name()
                self.grammar[new_rule] = [sequence[0], sequence[1]]
                sequence = [new_rule] + sequence[2:]
        
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
    
    def save_grammar(self, grammar: Dict[str, List[str]], filename: str):
        """Save grammar to a JSON file with start symbol information"""        
        with open(filename, 'w') as f:
            json.dump(dict(grammar), f, indent=2)


def main():
    # Example usage
    nonterminal = "F"
    compressor = RePairCompressor(nonterminal=nonterminal)

    # read file
    si = 32
    with open("pizza&chille corpus/dna.50MB", "r", encoding='utf-8') as f:
        test_string = f.read(si * si).lower()  # Read first 128 KB for testing
        # test_string_list = list(test_string)
        # test_string_list[3]="g"
        # test_string_list[-1]="g"
        # test_string = ''.join(test_string_list)


    # test_string = "atscgghgfcttashffggccffghttgassta"
    print(f"Original string: {test_string}")
    
    grammar = compressor.compress(test_string)
    start_symbol = compressor.get_start_symbol()
    
    print(f"Compressed grammar: {grammar}")
    print(f"Start symbol: {start_symbol}")
    
    # Save to file
    file_name = f"test_string_re-pair_dna-{si}KiB-1_{nonterminal}.json"
    compressor.save_grammar(grammar, f"testing_dataset/pizza&chille corpus_SLP/{file_name}")
    print(f"Grammar saved to {file_name}")

if __name__ == "__main__":
    main()