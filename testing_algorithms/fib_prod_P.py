fibonacci_grammar = {}

def fib_P(f_n: int) -> dict:
    p_n = f_n // 2 # to compute `F_2i`, where i = n//2, first compute `P_i` and then apply (b -> ba)
    rest = f_n % 2


    if rest == 0: # Even case
        """ to go from `P_i` to `F_2i`, substitute b with ba `(b -> ba)`"""

        fibonacci_grammar["B1"] = ['b', 'a']

        for i in range(2, p_n + 1):
            if i == 2:
                fibonacci_grammar[f"A{i}"] = ['a', f"B{i - 1}"]
            elif i == 3:
                fibonacci_grammar[f"B{i-1}"] = ['a', f"C{i - 2}"]
                fibonacci_grammar[f"C{i-2}"] = [f"B{i - 2}", f"B{i - 2}"]
                fibonacci_grammar[f"A{i}"] = [f"A{i - 1}", f"B{i - 1}"]
            else:
                fibonacci_grammar[f"B{i-1}"] = [f"A{i - 2}", f"C{i - 2}"]
                fibonacci_grammar[f"C{i-2}"] = [f"B{i - 2}", f"B{i - 2}"]
                fibonacci_grammar[f"A{i}"] = [f"A{i - 1}", f"B{i - 1}"]

    if rest == 1: # Odd case
        """ to go from `P_i` to `F_2i+1`, first go from `P_i` to `F_2i` (b -> ba), and then go from `F_2i` to `F_2i+1` by doing (a -> ab) and (b -> a)"""

        fibonacci_grammar["A1"] = ['a', 'b']
        fibonacci_grammar["B1"] = ['a', 'A1']

        for i in range(2, p_n + 1):
            if i == 2:
                fibonacci_grammar[f"A{i}"] = [f"A{i - 1}", f"B{i - 1}"]
            else:
                fibonacci_grammar[f"B{i-1}"] = [f"A{i - 2}", f"C{i - 2}"]
                fibonacci_grammar[f"C{i-2}"] = [f"B{i - 2}", f"B{i - 2}"]
                fibonacci_grammar[f"A{i}"] = [f"A{i - 1}", f"B{i - 1}"]

    return fibonacci_grammar

if __name__ == "__main__":
    fib_P(5)
    print(fibonacci_grammar)