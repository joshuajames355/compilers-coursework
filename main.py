import fileParser
from lexical import lexical
from syntax import SyntaxAnalyser

def main():
    tokens, formula = fileParser.loadFile("example1.txt")
    #print(str(tokens))
    tokenList = lexical(tokens, formula)
    #print("\n".join(map(str, test)))
    
    syntax = SyntaxAnalyser()
    out = syntax.syntax(tokenList)

main()
