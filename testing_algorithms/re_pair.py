from collections import defaultdict


def symbol_gen(prefix: str = 'A'):
    """Yield A1, A2, A3, ... as non-terminal symbols.

     
    """
    i = 1
    while True:
        yield f"{prefix}{i}"
        i += 1

# Returns the most frequent pair
def most_frequent_pair(sequence):
    # We create a dictionary that will have the symbol pair as the key and the value as the occurrences of the digram
    pair_count = defaultdict(int)
    i = 0

    while i < len(sequence) - 1:
        pair = (sequence[i], sequence[i+1])
        pair_count[pair] += 1
        # check if there is an overlap
        if (i+2)< len(sequence) and sequence[i] == sequence[i+1] and sequence[i+1] == sequence[i+2]:
            # We increase by 2 so that the overlap is considered only once
            i += 2  
        else:
            i += 1
            
    if not pair_count:
        return None
    # We return the pair with higher occurrence
    max_key = max(pair_count, key = pair_count.get)
    return (max_key, pair_count[max_key])


# Replaces the pair present in the sequence with the new non-terminal symbol
def replace_pair(sequence, pair, non_terminal_symbol):
    i = 0
    while i < len(sequence) - 1:
        if sequence[i] == pair[0] and sequence[i+1] == pair[1]:
            sequence = sequence[:i] + [non_terminal_symbol] + sequence[i+2:]    
        i += 1
    return sequence

def re_pair(sequence):
    sequence = list(sequence.lower())
    # The initial non-terminal symbol will be 'A'
    non_terminal_symbol = 'A'
    rules = []
    while True:
        # Get the most frequent pair of symbols
        pair, occurrence = most_frequent_pair(sequence)
        if occurrence <= 1:
            break
        # Replace the most frequent pair in the text with the new non-terminal symbol
        sequence = replace_pair(sequence, pair, non_terminal_symbol)
        # We add the new production rule
        rules.append((non_terminal_symbol, pair))
        # Create the new non-terminal symbol
        non_terminal_symbol = chr(ord(non_terminal_symbol) + 1)
    return sequence, rules

def re_pair_chomsky(sequence,S):
    """Build a binary grammar (dict) via RE-PAIR; inline preterminals into terminals.

    Returns:
    - axiom: the start symbol (string)
    - rules: dict[str, tuple[symbol,symbol]] where symbol is either a terminal (char)
      or a non-terminal (e.g., 'A1'). All RHS are pairs of size 2.
    """
    # S = 'G2'
    text = sequence.lower()
    gen = symbol_gen(S)
    rules: dict[str, tuple] = {}

    # 1) Preterminals: give each terminal char its own non-terminal temporarily
    # so we can operate purely on non-terminal tokens for RE-PAIR.
    term_map: dict[str, str] = {}
    for ch in sorted(set(text)):
        nt = next(gen)
        term_map[ch] = nt
        rules[nt] = (ch,)  # mark as preterminal for later inlining

    # 2) Tokenize to non-terminals
    tokens = [term_map[ch] for ch in text]

    # Edge case: empty input
    if not tokens:
        # Create a degenerate start with two identical terminals (no tokens exist)
        axiom = S
        rules[axiom] = ('', '')
        return axiom, rules

    # 3) RE-PAIR on tokens
    while True:
        mf = most_frequent_pair(tokens)
        if mf is None:
            occurrence = 0
        else:
            pair, occurrence = mf

        if occurrence <= 1:
            break

        new_nt = next(gen)
        tokens = replace_pair(tokens, pair, new_nt)
        rules[new_nt] = pair

    # 4) Chain the remaining tokens into a right-branching binary tree; start is 'S'
    axiom = S
    current_head = axiom
    while len(tokens) > 1:
        if len(tokens) != 2:
            next_head = next(gen)
            tail = next_head
        else:
            tail = tokens[1]
            next_head = None
        rules[current_head] = (tokens[0], tail)
        tokens = tokens[1:]
        if next_head is None:
            break
        current_head = next_head

    # If only one token remained, synthesize a trivial pair to keep binary RHS
    if axiom not in rules:
        rules[axiom] = (tokens[0], tokens[0])

    # 5) Inline preterminals (B -> 'b') wherever they appear on RHS and drop them
    preterms = {nt: rhs[0] for nt, rhs in list(rules.items()) if len(rhs) == 1}
    if preterms:
        for nt, rhs in list(rules.items()):
            if len(rhs) == 2:
                l, r = rhs
                l2 = preterms.get(l, l)
                r2 = preterms.get(r, r)
                if (l2, r2) != rhs:
                    rules[nt] = (l2, r2)
        # Remove preterminal rules after inlining
        for nt in preterms:
            rules.pop(nt, None)

    return axiom, rules




def main(text, S):
    # text = 'aaabcaabaaabcabdabd'
    # compressed_text, rules = re_pair(text)
    # print("Compressed text with re_pair(S):", compressed_text)
    # print("Production rules:", rules)
    # size = len(rules)*2 + len(compressed_text)
    # print("Grammar size:", size)

    start, rules = re_pair_chomsky(sequence=text, S=S)
    # print("\nStart symbol:", start)
    # print("Production rules (dict):", rules)
    # print("Grammar size:", len(rules))
    return start, rules

if __name__=='__main__':
    main('aaabcaabaaabcabdabd', 'A')
