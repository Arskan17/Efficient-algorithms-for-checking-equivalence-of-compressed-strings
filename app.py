from itertools import combinations # https://docs.python.org/3/library/itertools.html#itertools.combinations
from math import gcd # https://docs.python.org/3/library/math.html#math.gcd
import input
import sys

# def compute_all_pairs(grammar):
#     nonterminals = set(grammar.keys())  # Collect all nonterminals
#     S = set(combinations(nonterminals, 2))  # Generate all pairs
#     return S

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

def check_lengths(S, lengths_1, lengths_2):
    # Check if |w_A| = |w_B| for each (A, B) in S
    checks = [lengths_1[pair[0]] == lengths_2[pair[1]] for pair in S]
    return all(checks)

def compute_descending_nonterminals(lengths):
    desc_nonterminals = sorted(lengths, key=lengths.get, reverse=True) # sort nonterminals in descending order according to |w_A|
    return desc_nonterminals

def compute_rel(rel, pair, i):
    # Create a relation (A,B,i) for each pair in the set S, or in our case, {"(A,B)": [i_1, i_2, ...]}
    if pair not in rel:
        rel[pair] = [i]
    # If the pair already exists, append i to the list
    else:
        rel[pair].append(i)
        rel[pair] = list(set(rel[pair]))  # Remove duplicates
    return rel

def compute_split(A, rel, merged_lengths_dict, E, F):
    for pair in list(rel.keys()):
        B = pair[0]
        C = pair[1]
        i = rel[pair][0]
        w_B = merged_lengths_dict.get(B, 1)
        w_C = merged_lengths_dict.get(C, 1)
        w_E = merged_lengths_dict.get(E, 1)
        w_F = merged_lengths_dict.get(F, 1)


        if A != B and A != C: # Case 1 
            rel
        
        elif A == B and A != C: # Case 2
            if w_E > i and (w_C+i) > w_E:
                rel = compute_rel(rel, (E,C), i)
                rel = compute_rel(rel, (C,F), (w_E - i))
            elif w_E > i and (w_C+i) <= w_E:
                rel = compute_rel(rel, (E,C), i)
            elif w_E == i and w_C <= w_F:
                rel = compute_rel(rel, (C,F), 0)
            elif w_E == i and w_C > w_F:
                rel = compute_rel(rel, (F,C), 0)
            elif w_E < i:
                rel = compute_rel(rel, (F,C), (i - w_E))

        elif A != B and A == C: # Case 3
            if (w_E+i) >= w_B:
                rel = compute_rel(rel, (B,E), i)
            elif (w_E+i) < w_B:
                rel = compute_rel(rel, (B,E), i)
                rel = compute_rel(rel, (B,F), (w_E + i))

        elif A == B and A == C: # Case 4
            if i == 0:
                rel
            elif w_E > i >= 1 and i >= w_F:
                rel = compute_rel(rel, (E,E), i)
                rel = compute_rel(rel, (E,F), (w_E - i))
            elif w_E > i >= 1 and i < w_F:
                rel = compute_rel(rel, (E,E), i) 
                rel = compute_rel(rel, (F,F), i)
                rel = compute_rel(rel, (E,F), (w_E - i))
            elif w_E == i and w_E >= w_F:
                rel = compute_rel(rel, (E,F), 0)
            elif w_E == i and w_E < w_F:
                rel = compute_rel(rel, (F,E), 0)
                rel = compute_rel(rel, (F,F), i)
            elif w_E < i and i >= w_F:
                rel = compute_rel(rel, (F,E), (i - w_E))
            elif w_E < i and i < w_F:
                rel = compute_rel(rel, (F,E), (i - w_E))
                rel = compute_rel(rel, (F,F), i)

    return rel

def simple_compact(values, w_A):
    if len(values) < 3:
        return values # SimpleCompact fails given that there are fewer than 3 triples

    i, j, k = values[0], values[1], values[2]
    if (j - i) + (k - i) <= w_A - i:
        g = gcd(j - i, k - i)
        # new_values = [i, i + g] + values[3:]
        return simple_compact(([i, i + g] + values[3:]), w_A)  # Recursively apply to the new list
    
    elif (j - i) + (k - i) > w_A - i:
        return values

def compute_compact(rel, merged_lengths_dict):
    for (A,B), values in rel.items():
        if A.isupper() and B.isupper():
            if len(values) < 3:
                continue  # Skip if there are fewer than 3 triples for this key

            w_A = merged_lengths_dict.get(A, 1)

            # # Iterate through consecutive triplets in the sorted list
            # for index in range(len(values) - 2):
            #     i, j, k = values[index], values[index + 1], values[index + 2]
            #     if (j - i) + (k - i) <= w_A - i:
            #         g = gcd(j - i, k - i)
            #         # Replace the three triples with two triples
            #         rel[key] = [i, i + g]
            #         return rel  # Return immediately after the first successful replacement

            rel[(A,B)] = simple_compact(values, w_A)
    
    return rel

def a_b_check(rel):
    suffixes = [(key,values) for key, values in rel.items() if key[0].islower() and key[1].islower()]
    print(f'suffixes := {suffixes}')
    return all([(key[0] == key[1]) and (values[0] == 0) for key, values in suffixes])


if __name__ == '__main__':
    # input
    grammar_1 = input.G[0] # grammar G which defines a set of words
    grammar_2 = input.G[1]
    S = input.S # set S of pairs of nonterminals
    print(f'set S = {S}')


    # output
    ############################################################################################################
    # compute lengths of words generated by nonterminals in G and check if for each (A, B) in S w_A = w_B
    ############################################################################################################


    # begin
    lengths_1 = compute_lengths(grammar_1) # compute |w_A| for each nonterminal A
    lengths_2 = compute_lengths(grammar_2)
    print(lengths_1)
    print(lengths_2)
    
    if not check_lengths(S, lengths_1, lengths_2): # if there is (A, B) in S such that |w_A| != |w_B| then return false
        sys.exit(False)

    desc_nonterminals_1 = compute_descending_nonterminals(lengths_1) # ( A_1, ..., A_n) in descending order according to |w_A|
    # print(f'(A1, ..., An) := {desc_nonterminals_1}')
    desc_nonterminals_2 = compute_descending_nonterminals(lengths_2)
    # print(f'(A1, ..., An) := {desc_nonterminals_2}')

    rel = {}
    rel = compute_rel(rel, next(iter(S)), 0) # compute relation rel := U(A,B) in S (A, B, 0); 
    print(f'rel := {rel}')

    # compute split and compact for each Ai with each (A, B) in rel until there are no nonterminals in triples of rel
    merged_lengths_dict = {**lengths_1, **lengths_2}
    desc_nonterminals = sorted(merged_lengths_dict, key=merged_lengths_dict.get, reverse=True)
    print(f'(A1, ..., An) := {desc_nonterminals}')

    merged_grammar = {**grammar_1, **grammar_2} # merge grammar_1 and grammar_2

    for A in desc_nonterminals:
        E, F = merged_grammar[A]
        rel = compute_split(A, rel, merged_lengths_dict, E, F)
        rel = compute_compact(rel, merged_lengths_dict)
        # print(f'compact := {r}')
    print(rel)
    print(a_b_check(rel)) # if there exists (a,b,0) in rel and a!=b return false, else return true