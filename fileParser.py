import string

#stores the token information imported from the file
class TokensImport:
    ##all are list of tokens, pulled directly from a file
    variables = []
    constants = []
    predicates = [] #instanes of Predicate, represents name and arity
    equality = [] #needs to be length 1
    connectives = [] #needs to be length 5
    quantifiers = [] #needs to be length 2

    def __str__(self):
        return """
Variables: {}
constants: {}
predicates: {}
equality: {}
connectives: {}
quantifiers: {}""".format(
        ", ".join(self.variables), 
        ", ".join(self.constants), 
        ", ".join(map(str, self.predicates)), 
        ", ".join(self.equality), 
        ", ".join(self.connectives), 
        ", ".join(self.quantifiers))

    #gets a list of all tokens (listed in the file, so no ( , ) etc), as strings
    def getTokenList(self):
        return self.variables + self.constants + self.quantifiers + self.equality + self.connectives + list(map(lambda  x: x.name, self.predicates))

class Predicate:
    name = ""
    arity = -1

    @staticmethod
    def fromString(items):
        new = Predicate()
        if items.endswith("]") and items.count("[") == 1:
            new.name = items[:items.find("[")]
            new.arity = int(items[items.find("[")+1:items.find("]")])

        return new

    def __str__(self):
        return  "{}[{}]".format(self.name, str(self.arity))

#filename -string
#returns (RuleSet, formula)
def loadFile(filename):
    KEYWORDS = ["variables:", "constants:", "predicates:", "equality:", "connectives:", "quantifiers:", "formula:"]
    formula = ""

    rules = TokensImport()
    with open(filename) as file:
        data = file.read()

        lastKeyword = ""
        startIndex = 0
        currentIndex = 0

        while currentIndex < len(data):
            currentString = data[startIndex:currentIndex]

            newKeyword = ""
            for x in KEYWORDS:
                if currentString.endswith(x):
                    newKeyword = x
            if currentIndex+1 == len(data) or newKeyword != "":
                if currentIndex+1 == len(data): #special case to handle when EOF terminates a section without any whitespace/labels following it
                    endOfSection = currentIndex - len(newKeyword) + 1
                else:
                    endOfSection = currentIndex - len(newKeyword)

                if lastKeyword == "variables:":
                    rules.variables = parseList(data[startIndex:endOfSection])
                if lastKeyword == "constants:":
                    rules.constants = parseList(data[startIndex:endOfSection])
                if lastKeyword == "predicates:":
                    rules.predicates = list(map(lambda x: Predicate.fromString(x), parseList(data[startIndex:endOfSection])))
                if lastKeyword == "equality:":
                    rules.equality = parseList(data[startIndex:endOfSection])
                if lastKeyword == "connectives:":
                    rules.connectives = parseList(data[startIndex:endOfSection])
                if lastKeyword == "quantifiers:":
                    rules.quantifiers = parseList(data[startIndex:endOfSection])
                if lastKeyword == "formula:":
                    formula = data[startIndex:endOfSection].strip()
                startIndex = currentIndex + 1
                lastKeyword = newKeyword

            currentIndex += 1

    validateRules(rules)
    return (rules, formula)

def validateRules(rules):
    if len(rules.equality) != 1:
        raise ValueError("Must have only 1 equality symbol")
    if len(rules.connectives) != 5:
        raise ValueError("Must have only 5 connectives")
    if len(rules.quantifiers) != 2:
        raise ValueError("Must have only 2 quantifiers")
    for x in rules.variables + rules.constants + list(map(lambda x: x.name, rules.predicates)):
        validateVariable(x)
    for x in rules.equality:
        validateEquality(x)      
    for x in rules.connectives + rules.quantifiers:
        validateConnective(x)      
    checkUnique(rules)

def checkUnique(rules):
    found = []
    everything = rules.equality + rules.connectives + rules.quantifiers + rules.variables + rules.constants + list(map(lambda x: x.name, rules.predicates))
    for each in everything:
        if each in found:
            raise ValueError("Invalid duplicate identifier: {}".format(each))
        found.append(each)

VALID_CHARS_VAR = set(string.ascii_letters + string.digits + "_")
def validateVariable(name):
    if not set(name) < VALID_CHARS_VAR:
        raise ValueError("Invalid variable/constant name: {}".format(name))

VALID_CHARS_CONNECTIVES = set(string.ascii_letters + string.digits + "_" + "\\")
def validateConnective(name):
    if not set(name) < VALID_CHARS_CONNECTIVES:
        raise ValueError("Invalid connective/qualifier name: {}".format(name))

VALID_CHARS_EQUALITY = set(string.ascii_letters + string.digits + "_" + "\\" + "=")
def validateEquality(name):
    if not set(name) < VALID_CHARS_EQUALITY:
        raise ValueError("Invalid name for equality symbol: {}".format(name))

#listIn is a string, which is a list of items, seperated by whitespace
def parseList(listIn):
    return list(map(lambda x: x.strip(), listIn.split()))