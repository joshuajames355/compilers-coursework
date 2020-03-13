from lexical import *

def generateGrammar(tokenData):
    output = "NonTerminals = {:S, :B, :A, :B, :D}\n"
    output += "Terminal = {" + ", ".join( ["','", "(", ")" ] + tokenData.getTokenList()) + "}"
    output += "\nProduction Rules: \n"
    output += ":S -> " 
    for each in tokenData.predicates:
        output += each.name + "(" + ("V,"*each.arity)[:2*each.arity-1] + ") | "
    output += "(:B) | "
    for each in tokenData.quantifiers:
        output += each + " V :S | "
    for index, each in enumerate(tokenData.connectives):
        if index == 4:
            output += each + " :S"
    output += "\n:B -> :A " +  tokenData.equality[0] +  " :A | :S :D"
    output += "\n:A -> :C | :V"
    output += "\n:D -> "
    for (index,each) in enumerate(tokenData.connectives):
        if index != 4:
            output += each + " :S | "
    output += "\n:V -> " + " | ".join(tokenData.variables)
    output += "\n:C -> " + " | ".join(tokenData.constants)
    return output


class GraphNode:
    identifier = 'S'
    token = 0
    parent = 0
    children = []
    complete = False

    def __init__(self, identifier, parent, token=0, complete=False):
        self.identifier = identifier
        self.token = token #only for leaf nodes?
        self.parent = parent
        self.children = []
        self.complete = complete

class SyntaxAnalyser:
    def __init__(self):
        self.start = 0 #the graph
        self.current = 0

        self.source = [] #the source
        self.index = 0

    def syntax(self, source):
        self.start = GraphNode(':S', 0)
        self.current = self.start

        self.source = source
        self.index = 0 #in source
        
        while self.index < len(source):
            currentToken = self.source[self.index]

            if self.current.identifier == ':S':
                if currentToken.tokenClass == PREDICATE:
                    self.addCurrentToken(currentToken)
                    self.match(BRACKET_START)
                    for _ in range(currentToken.attributes-1):
                        self.matchVariable()
                        self.match(COMMA)
                    self.matchVariable()
                    self.match(BRACKET_END)
                    self.complete()     

                elif currentToken.tokenClass == BRACKET_START:
                    self.addCurrentToken(currentToken)
                    self.pushChild(':B')  
                elif currentToken.tokenClass == BRACKET_END and len(self.current.children) == 2 and self.current.children[1].identifier == ':B':
                        self.addCurrentToken(currentToken)
                        self.complete()

                elif currentToken.tokenClass == NEGATION:
                    self.addCurrentToken(currentToken)
                    self.current.complete = True
                    self.pushChild(':S') 

                elif currentToken.tokenClass == QUANTIFIER:
                    self.addCurrentToken(currentToken)
                    self.matchVariable()
                    self.current.complete = True
                    self.pushChild(':S') 

                else:
                    raise Exception("Unexpected token: {} found while at non-terminal: :S. Needed to be: PREDICATE, BRACKET_START, BRACKET_END, NEGATION OR QUANTIFIER".format(str(self.source[self.index])))

            elif self.current.identifier == ':B':
                if len(self.current.children) == 0:
                    if currentToken.tokenClass == VARIABLE or currentToken.tokenClass == CONSTANT:
                        self.matchVariableConstant()

                        self.match(EQUALITY)
                        self.matchVariableConstant()
                        self.complete()
                    else:
                        self.pushChild(':S')
                elif len(self.current.children) == 1: 
                    self.current.complete = True
                    self.pushChild(':D')

                
            elif self.current.identifier == ':D':
                self.match(CONNECTIVE)
                self.current.complete = True
                self.pushChild(':S')

        if self.current != self.start:
            raise Exception("Unexpected EOF at position: {} Current node is of type: {}".format(len(source)-1, self.current.identifier))

        return self.start

    def addCurrentToken(self, token):
        self.current.children.append(GraphNode('',self.current , token, True))
        self.index += 1

    def pushChild(self, className):
        newNode = GraphNode(className, self.current, False)
        self.current.children.append(newNode)
        self.current = newNode    

    #match a token without adding it to the tree
    def matchIgnore(self, token):
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != token:
                raise Exception("Unexpected token: {} found, expecting a token of type: {}".format(str(self.source[self.index]), getTokenClassStr(token)))
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def match(self, token):
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != token:
                raise Exception("Unexpected token: {} found, expecting a token of type: {}".format(str(self.source[self.index]), getTokenClassStr(token)))
            self.current.children += [GraphNode('', self.current, self.source[self.index])]
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def matchVariable(self): #adds the V subtree
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != VARIABLE:
                raise Exception("Unexpected token: {} found, expecting a token of type: {}".format(str(self.source[self.index]), getTokenClassStr(VARIABLE)))
            
            newChild = GraphNode(':V', self.current, complete=True)
            newChild.children = [GraphNode('', newChild, self.source[self.index], True)]
            self.current.children += [newChild]
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def matchVariableConstant(self): #adds the V/D subtree
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != VARIABLE and self.source[self.index].tokenClass != CONSTANT:
                raise Exception("Unexpected token: {} found, expecting a token of type: {} or: {}".format(str(self.source[self.index]), getTokenClassStr(VARIABLE), getTokenClassStr(CONSTANT)))
            
            t = ':V'
            if self.source[self.index].tokenClass != VARIABLE:
                t = ':C'

            newChild = GraphNode(t, self.current, complete=True)
            newChild.children = [GraphNode('', newChild, self.source[self.index], True)]
            self.current.children += [newChild]
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def complete(self):
        self.current.complete = True
        while True:
            if self.current.parent == 0 or not self.current.complete:
                return
            self.current = self.current.parent       