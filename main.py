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

    with open(args.l, mode="a") as logFile:
        try:
            tokens, formula = loadFile(args.input)
            logFile.write("Imported file: {}\n".format(args.input))   
            logFile.write("Grammar:\n{}\n".format(generateGrammar(tokens)))   
            tokenList = lexical(tokens, formula)
            syntax = SyntaxAnalyser()
            tree = syntax.syntax(tokenList)
            logFile.write("Formula Sucessfully parsed!\n")
            drawTree(tree, args.o, args.v)
            logFile.write("Written tree to: {}\n".format(args.o))
        except Exception as e:
            logFile.write("An Error Occured! \n" + str(e) + "\n")    

main()
