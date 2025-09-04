import sys
import json

fibonacci_productions = {}

def generate_fibonacci_grammar(i):
    """
    Generates the productions for an SLP that produces the i-th Fibonacci word.
    Uses the recursive definition: F_i = F_{i-1}F_{i-2} for i >= 3.

    Args:
        i: The index of the Fibonacci word whose grammar is to be generated
           (integer >= 1).

    Returns:
        The nonterminal symbol for F_i (string). The generated productions
        are stored in the global fibonacci_productions dictionary.
    """
    # Construct the nonterminal name for the current index
    current_nonterminal = f"F{i}"

    # Check if the production for this nonterminal is already generated
    if current_nonterminal in fibonacci_productions:
        return current_nonterminal  # Return the existing nonterminal name

    # Base cases: Replace F2 with "a" and F1 with "b"
    if i == 1:
        return "b"  # F1 -> "b"
    elif i == 2:
        return "a"  # F2 -> "a"

    # Recursive step for F3 and beyond
    elif i > 2:
        # Recursively generate grammars for F_{i-1} and F_{i-2}
        fib_im1_rhs = generate_fibonacci_grammar(i - 1)
        fib_im2_rhs = generate_fibonacci_grammar(i - 2)

        # Production Fi -> [F_{i-1}, F_{i-2}]
        fibonacci_productions[current_nonterminal] = [fib_im1_rhs, fib_im2_rhs]
        return current_nonterminal
    else:
        # Handle invalid input
        raise ValueError("Input index i must be a positive integer.")
    
def fibonacci(i):
    """
    Calculate the i-th Fibonacci number.

    Args:
        i (int): The index of the Fibonacci number to calculate (i >= 0).

    Returns:
        int: The i-th Fibonacci number.
    """
    if i < 0:
        raise ValueError("Index must be a non-negative integer.")
    elif i == 0:
        return 0
    elif i == 1:
        return 1

    # Iterative calculation
    a, b = 0, 1
    for _ in range(2, i + 1):
        a, b = b, a + b

    return b

def m(index):
    if index < 3:
        print("Please enter an integer greater than or equal to 3.")
    else:
        # Clear previous productions just in case (important if function was called multiple times)
        fibonacci_productions.clear()

        # Generate the grammar productions
        start_symbol = generate_fibonacci_grammar(index)

        # Print the generated productions in the requested format
        print(f"\nProductions for the SLP generating F_{index} (Start Symbol: {start_symbol})")
        print(f"The F-{index} is of size: {fibonacci(index)}")
        # print(fibonacci_productions)

        # Save the productions to a JSON file
        # with open("G1.json", "w") as f:
        #     f.write(json.dumps(fibonacci_productions))

        return fibonacci_productions


if __name__ == "__main__":
    try:
        # Get input from the user
        index = int(input("Enter the index (i) for the Fibonacci word grammar (e.g., 7): "))

        m(index)

    except ValueError as e:
        print(f"Invalid input: {e}")
    except RecursionError:
        print("Recursion depth exceeded. The requested Fibonacci word index is too large to generate the grammar this way.")
    except Exception as e:
        print(f"An error occurred: {e}")