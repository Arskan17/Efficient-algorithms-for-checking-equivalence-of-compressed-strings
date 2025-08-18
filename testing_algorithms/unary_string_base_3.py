from collections import Counter

def get_most_frequent_trigram(input_string: list) -> tuple:
    """Gives back the most frequent trigram by creating triplets of adjacent character, and giving the one with the highest frequency.  
    -> a tuple with the trigram and its frequency in the input string.  
    Runs in `O(n)` expected time.
    """
    occurence_frequency_set = Counter(zip(input_string, input_string[1:], input_string[2:])) # O(n)+O(n)+O(n) = **O(n)**
    return occurence_frequency_set.most_common(1)[0] if occurence_frequency_set else None # O(n log 1) = **O(n)**. `n log 1` because `Counter.most_common(k)` runs in `n log k`

def replace_trigrams(input_string: list, trigram: tuple, non_terminal: str, replacement_character_id: int) -> list:
    """Create a new list of tokens(string after replacements) by replacing the trigrams by the new character.  
    -> the new string with trigrams substituted with new character.  
    Runs in `O(n)` expected time.
    """
    sub_rules = {}
    result = []
    i = 0

    # **O(n)**
    while i < len(input_string):
        if i < len(input_string)-2 and (input_string[i], input_string[i+1], input_string[i+2]) == trigram:
            # Create two sub rules for the trigram. A -> aaa to A1 -> aa, A2 -> A1a
            if i < 3:
                replacement_character = f"{non_terminal}{replacement_character_id}"
                replacement_character_id += 1
                sub_rules[replacement_character] = (input_string[i], input_string[i+1])

                replacement_character_1 = f"{non_terminal}{replacement_character_id}"
                replacement_character_id += 1
                result.append(replacement_character_1)

                sub_rules[replacement_character_1] = (replacement_character, input_string[i+2])

            else:
                # Just append the previous replacement character since we are in a repeating context
                replacement_character = f"{non_terminal}{replacement_character_id-1}"
                result.append(replacement_character)

            i += 3
        else:
            # If there are no trigrams, return the original input string
            result.append(input_string[i])
            i += 1

    return result, sub_rules, replacement_character_id

def get_final_rule(input_string: list, non_terminal: str, replacement_character_id: int) -> tuple:
    sub_rules = {}
    result = []
    i = 0

    while i < len(input_string):
        if i < len(input_string)-1:
            replacement_character = f"{non_terminal}{replacement_character_id}"
            replacement_character_id += 1
            
            result.append(replacement_character)
            sub_rules[replacement_character] = (input_string[i], input_string[i+1])
            i += 2
        else:
            result.append(input_string[i])
            i += 1

    return result, sub_rules, replacement_character_id

def re_triple(input_string: list, non_terminal: str) -> dict:
    Rules = {}
    replacement_character_id = 0

    while True:
        # Step 2. Find the most frequent triple t in T.
        # **O(n)**
        most_frequent_triple = get_most_frequent_trigram(input_string)

        # Step 4. Re-evaluate the frequencies of pairs for the renewed text generated.
        # If the maximum frequency is 1, add S → (current text) to R, and terminate. Otherwise, return to Step 2.
        # **O(n)**
        if not most_frequent_triple:
            break
        trigram, frequency = most_frequent_triple
        if frequency < 2:
            break
        # Step 3. Replace of trigram, t, with a new variable v, then add v → t to R.
        # **O(n)**
        input_string, sub_rules, replacement_character_id = replace_trigrams(input_string=input_string, trigram=trigram, non_terminal=non_terminal, replacement_character_id=replacement_character_id)
        Rules = {**Rules, **sub_rules}

    # Final step. Convert the last string (with no trigram having occurence more than 1) to new rules, so as to get a starting node.
    left, right = input_string[:-1], input_string[-1]
    while len(left) > 1:
        left, sub_rules, replacement_character_id = get_final_rule(input_string=left, non_terminal=non_terminal, replacement_character_id=replacement_character_id)
        Rules = {**Rules, **sub_rules}

    start_node = (left[0], right)
    Rules[non_terminal] = start_node

    return Rules

def main(length: int):
    input_string = 'a' * length
    non_terminal = 'B'
    return re_triple(input_string=input_string, non_terminal=non_terminal)


if __name__ == "__main__":
    main(length=15)