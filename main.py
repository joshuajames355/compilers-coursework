from fileParser import loadFile
from lexical import lexical
from syntax import SyntaxAnalyser, generateGrammar
from render import drawTree

import argparse

def main():
    parser = argparse.ArgumentParser(description="First Order Logic Parser.")
    parser.add_argument('input', help="The input file")
    parser.add_argument('-o', help="The output file", default="output")
    parser.add_argument("-l", help="The log file", default="log.txt" )
    parser.add_argument("-v", help="View the file after rendering it", action='store_true')
    args=parser.parse_args()

    tokens, formula = loadFile(args.input)
    tokenList = lexical(tokens, formula)
    syntax = SyntaxAnalyser()
    tree = syntax.syntax(tokenList)
    drawTree(tree, args.o, args.v)

main()
