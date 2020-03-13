from fileParser import loadFile
from lexical import lexical
from syntax import SyntaxAnalyser, generateGrammar
from render import drawTree

import argparse

def main():
    parser = argparse.ArgumentParser(description="First Order Logic Parser.")
    parser.add_argument('input', help="The input file")
    parser.add_argument('-o', help="The output file for the tree (output by default)", default="output")
    parser.add_argument('-g', help="The output file for the grammar (grammar.txt by default)", default="grammar.txt")
    parser.add_argument("-l", help="The log file (log.txt by default)", default="log.txt" )
    parser.add_argument("-v", help="View the file after rendering it", action='store_true')
    args=parser.parse_args()

    with open(args.l, mode="a") as logFile:
        try:
            tokens, formula = loadFile(args.input)
            logFile.write("Imported file: {}\n".format(args.input)) 
            logFile.write("Formula:\n{}\n".format(formula)) 

            grammar = generateGrammar(tokens)
            logFile.write("Grammar:\n{}\n".format(grammar))   
            with open(args.g, mode="w") as grammarFile:
                grammarFile.write(grammar)

            tokenList = lexical(tokens, formula)
            syntax = SyntaxAnalyser()
            tree = syntax.syntax(tokenList)
            logFile.write("Formula Sucessfully parsed!\n")
            drawTree(tree, args.o, args.v)

            logFile.write("Written tree to: {}\n".format(args.o))

            print("Sucess, See log file ({}) for more details".format(args.l))
        except Exception as e:
            logFile.write("An Error Occured! \n" + str(e) + "\n")
            print("An Error Occured! \n" + str(e))
            exit(1)    

main()
