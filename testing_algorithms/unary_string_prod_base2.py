# I need an algorithm that'll convert a unary string into grammar productions.
# The schema I want is something like `A1 -> a a, A2 -> A1 A1, ..., An -> An-1 An-1`.
# Of course it should take in the size of the unary string I want as input, and generate the productions as a dictionary. In this dictionary productions are structured; keys on the lhs, and values on th rhs, like so
# `{"A1": ["a","a"],
# "A2": ["A1","A1"], ...}`.
# Thank you!