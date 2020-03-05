class FileData:
    ##all are list of tokens, pulled directly from a file
    variables = []
    constants = []
    predicates = []
    equality = []
    connectives = [] #2 parameters
    quantifiers = []
    formula = ""

    def __str__(self):
        return """Variables: {}
constants: {}
predicates: {}
equality: {}
connectives: {}
quantifiers: {}
formula: {}""".format(self.variables, self.constants, " ".join(map(str, self.predicates)), self.equality, self.connectives, self.quantifiers, self.formula)

class Predicate:
    name = ""
    arity = -1

    @staticmethod
    def fromString(string):
        new = Predicate()
        if string.endswith("]") and string.count("["):
            new.name = string[:string.find("[")]
            new.arity = int(string[string.find("[")+1:string.find("]")])

        return new

    def __str__(self):
        return  "{}[{}]".format(self.name, str(self.arity))

#filename -string
#returns (RuleSet, formula)
def loadFromFile(filename):
    KEYWORDS = ["variables:", "constants:", "predicates:", "equality:", "connectives:", "quantifiers:", "formula:"]
    rules = FileData()
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
                    rules.formula = data[startIndex:endOfSection].strip()
                startIndex = currentIndex + 1
                lastKeyword = newKeyword

            currentIndex += 1

    return rules

#listIn is a string, which is a list of items, seperated by whitespace
def parseList(listIn):
    return list(map(lambda x: x.strip(), listIn.split()))