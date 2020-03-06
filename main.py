import fileParser
from lexical import lexical

def main():
    tokens, formula = fileParser.loadFile("example1.txt")
    test = lexical(tokens, formula)

main()

#Start symbol S - capitals mark non terminals
#S -> T | (S ^ S) | ... | not S
#T -> P(y1..yd) | (C = D) | (C = x) | (x = C) | (x = y)     p a predicate of arity d, C,D constants, x,y variables
