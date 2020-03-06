import string

VARIABLE = 0
CONSTANT = 1
PREDICATE = 2
EQUALITY = 3
CONNECTIVE = 4
QUANTIFIER = 5 #2 parameters
NEGATION = 6 
BRACKET_START = 7
BRACKET_END = 8
COMMA = 9

class Token:
    tokenClass = -1 #one of the values above
    name = "" #the name 
    attributes = -1 #for predicate, the arity

    def __init__(self, tokenClass, name, attributes = -1):
        self.tokenClass = tokenClass
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return "Class: {} - Name: {} Attributes: {}".format(self.tokenClass, self.name, self.attributes)

def tokensFromTokensImport(tokensImport):
    out = []
    for each in tokensImport.variables:
        out += [Token(VARIABLE, each)]
    for each in tokensImport.constants:
        out += [Token(CONSTANT, each)]
    for index, each in enumerate(tokensImport.predicates):
        out += [Token(PREDICATE, each.name, each.arity)]
    for each in tokensImport.equality:
        out += [Token(EQUALITY, each)]
    for index, each in enumerate(tokensImport.connectives):
        if index == 4:
            out += [Token(NEGATION, each)]
        else:
            out += [Token(CONNECTIVE, each)]
    for each in tokensImport.quantifiers:
        out += [Token(QUANTIFIER, each)]
    return out

#tokens - a list of strings, representing all possible tokens
#source - string
def lexical(tokens, source):
    MAX_TOKEN_LENGTH = max(map(len, tokens.getTokenList()))
    TOKENS_BY_SIZE = [list(filter(lambda x : len(x.name) == size, tokensFromTokensImport(tokens))) for size in range(MAX_TOKEN_LENGTH + 1)]

    output = []

    start = 0
    current = 0
    while current < len(source):
        currentChar = source[current]
        currentToken = source[start:current]
        currentLength = current - start

        mustAddCurrent = False #if matches have been found, either in the current char, or start:current (not including current)
        mustAddPrevious = False

        if currentChar in ["(", ")", ","]: #handle these seperatley, as all other tokens are seperated by whitespace (or these chars)
            mustAddCurrent = True
            mustAddPrevious = True
        if currentChar in string.whitespace:
            if start == current: #strip leading whitespace
                start += 1
                current += 1
                continue
            mustAddPrevious = True
        #ensure final char in source code is handled correctly
        if current == len(source) - 1 and not mustAddCurrent:
            currentToken = source[start:current+1]
            currentLength = current - start +1
            mustAddCurrent = True

        if currentLength > MAX_TOKEN_LENGTH:
            raise ValueError("Invalid token: {} in formula at position: {}".format(currentToken, start))

        #match tokens
        if mustAddPrevious and currentLength > 0:
            match = False
            for token in TOKENS_BY_SIZE[currentLength]:
                if currentToken == token.name:
                    match = token
                    break
            if not match:
                raise ValueError("Invalid token: {} in formula at position: {}".format(currentToken, start))

            output += [match]

            start = current + 1
        if mustAddCurrent:
            if currentChar == "(":
                output += [Token(BRACKET_START, "(", -1)]
            if currentChar == ")":
                output += [Token(BRACKET_END, ")", -1)]
            if currentChar == ",":
                output += [Token(COMMA, ",", -1)]
            start = current + 1

        current += 1

    return output
