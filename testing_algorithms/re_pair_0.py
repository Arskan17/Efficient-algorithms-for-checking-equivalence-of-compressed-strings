from collections import Counter

def get_most_frequent_bigram(input_string: list) -> tuple:
    """Gives back the most frequent bigram by creating pairs of adjecent character, and giving the one with the highest frequency.  
    -> a tuple with the bigram and its frequency in the input string.  
    Runs in `O(n)` expected time.
    """
    occurence_frequency_set = Counter(zip(input_string, input_string[1:])) # O(n)+O(n)+O(n) = **O(n)**
    return occurence_frequency_set.most_common(1)[0] if occurence_frequency_set else None # O(n log 1) = **O(n)**. `n log 1` because `Counter.most_common(k)` runs in `n log k`

def replace_bigrams(input_string: list, bigram: tuple, replacement_character: str) -> list:
    """Create a new list of tokens(string after replacements) by replacing the bigrams by the new character.  
    -> the new string with bigrams substituted with new character.  
    Runs in `O(n)` expected time.
    """
    result = []
    i = 0

    # **O(n)**
    while i < len(input_string):
        if i < len(input_string)-1 and (input_string[i], input_string[i+1]) == bigram:
            result.append(replacement_character)
            i += 2
        else:
            result.append(input_string[i])
            i += 1
    return result

def get_final_rule(input_string: list, non_terminal: str, replacement_character_id: int) -> tuple:
    sub_rules = {}
    result = []
    i = 0

    while i < len(input_string):
        replacement_character = f"{non_terminal}{replacement_character_id}"
        replacement_character_id += 1
        if i < len(input_string)-1:
            result.append(replacement_character)
            sub_rules[replacement_character] = (input_string[i], input_string[i+1])
            i += 2
        else:
            result.append(input_string[i])
            i += 1

    return result, sub_rules, replacement_character_id

def re_pair(input_string: list, non_terminal: str) -> dict:
    Rules = {}
    # Step 1. Replace each symbol a ∈ Σ with a new variable v_a and add v_a → a to R.
    # For this I just create a list with individual characters from the input string.
    # **O(n)**
    input_string = list(input_string.lower())
    replacement_character_id = 0
    # Skip step 1. since we won't need v_a → a

    while True:
        # Step 2. Find the most frequent pair p in T.
        # **O(n)**
        most_frequent_pair = get_most_frequent_bigram(input_string)
        bigram, frequency = most_frequent_pair

        # Step 4. Re-evaluate the frequencies of pairs for the renewed text generated in Step 3.
        # If the maximum frequency is 1, add S → (current text) to R, and terminate. Otherwise, return to Step 2.
        # **O(n)**
        if not most_frequent_pair or frequency < 2:
            break

        replacement_character = f"{non_terminal}{replacement_character_id}"
        replacement_character_id += 1
        # Step 3. Replace of bigram, p, with a new variable v, then add v → p to R.
        # **O(n)**
        input_string = replace_bigrams(input_string, bigram, replacement_character)
        Rules[replacement_character] = bigram

    # Final step. Convert the last string (with no bigram having occurence more than 1) to new rules, so as to get a starting node.
    left, right = input_string[0], input_string[1:]
    while len(right) > 1:
        right, sub_rules, replacement_character_id = get_final_rule(input_string=right, non_terminal=non_terminal, replacement_character_id=replacement_character_id)
        Rules = {**Rules, **sub_rules}

    start_node = (left, right[0])
    Rules[non_terminal] = start_node

    return Rules


if __name__ == "__main__":
    input_string = 'aaaabaaaabaab'
    non_terminal = 'A'
    print(re_pair(input_string=input_string, non_terminal=non_terminal))