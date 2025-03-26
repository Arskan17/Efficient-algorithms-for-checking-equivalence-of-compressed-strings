# Efficient-algorithms-for-checking-equivalence-of-compressed-strings

We describe a polynomial time algorithm for the following problem:  
**The Problem:**  
Let G be a grammar which defines a set of words and S be a set of pairs of nonteminals from G.
Check if *w<sub>A</sub>* = *w<sub>B</sub>* for every pair (A, B) from S.  
Let G be a grammar with n productions which defines a set of words W.
Since the shortest words derivable from a nonterminal of a grammar in Chomsky normal form with n productions are of size not exceeding 2<sup>n</sup> the lengths of words from *W* are not longer than 2<sup>n</sup>. Such numbers can be stored in *n* bits.  
Standard algorithms for basic operations (comparing, addition, substraction,
division, multiplication) on such numbers work in polynomial time with respect to n.
This allows to compute the length of every word from *W* in polynomial time.

## Input
The algorithm gets two inputs,
- a grammar *G* which defines a set of words.  
        e.g. *G* = S → AB, 𝐴 → 𝑎C, C → bc, 𝐵 → 𝑑  
        the set of words *W* = {"abcd", "abc", "bc", "d"}  
        the set lengths |*w*| for each nonterminal, {'C': 2, 'A': 3, 'B': 1, 'S': 4}
- a set *S* of pairs of nonterminals from *G*.  
        *S* = {('S', 'A'), ('S', 'C'), ('S', 'B'), ('A', 'C'), ('A', 'B'), ('C', 'B')}