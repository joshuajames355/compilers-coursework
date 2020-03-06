from lexical import *

#Start symbol S - capitals mark non terminals
#S -> p(y1..yd)
# | (B)       
# | not S
# | forall x S | foreach x S | exists x S                      x variable

#P -> y1..yd                                    p a predicate of arity d, yi a variable 

#a term inside a bracket
# B -> A = A     
# | S D

#A -> C | x         C constants, y variables 
#D -> ^ S | v S | => S | <=> S

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
        self.start = GraphNode('S', 0)
        self.current = self.start

        self.source = source
        self.index = 0 #in source
        
        while self.index < len(source):
            currentToken = self.source[self.index]

            if self.current.identifier == 'S':
                if currentToken.tokenClass == PREDICATE:
                    self.addCurrentToken(currentToken)
                    self.match(BRACKET_START)
                    for _ in range(currentToken.attributes-1):
                        self.match(VARIABLE)
                        self.match(COMMA)
                    self.match(VARIABLE)
                    self.match(BRACKET_END)
                    self.complete()     

                elif currentToken.tokenClass == BRACKET_START:
                    self.addCurrentToken(currentToken)
                    self.pushChild('B')  
                elif currentToken.tokenClass == BRACKET_END:
                    if len(self.current.children) == 2 and self.current.children[1].identifier == 'B':
                        self.addCurrentToken(currentToken)
                        self.complete()

                elif currentToken.tokenClass == NEGATION:
                    self.addCurrentToken(currentToken)
                    self.current.complete = True
                    self.pushChild('S') 

                elif currentToken.tokenClass == QUANTIFIER:
                    self.addCurrentToken(currentToken)
                    self.match(VARIABLE)
                    self.current.complete = True
                    self.pushChild('S') 

                else:
                    raise Exception("Failed to match token: {}".format(str(self.source[self.index])))

            elif self.current.identifier == 'B':
                if len(self.current.children) == 0:
                    if currentToken.tokenClass == VARIABLE or currentToken.tokenClass == CONSTANT:
                        self.addCurrentToken(currentToken)

                        self.match(EQUALITY)
                        self.matchMultiple([VARIABLE, CONSTANT])
                        self.complete()
                    else:
                        self.pushChild('S')
                elif len(self.current.children) == 1: #Actually in class D,
                    self.match(CONNECTIVE)
                    self.pushChild('S')
                elif len(self.current.children) == 3:
                    self.complete()

        return self.start

    def addCurrentToken(self, token):
        self.current.children.append(GraphNode('',self.current, token, True))
        self.index += 1

    def pushChild(self, className):
        newNode = GraphNode(className, self.current, False)
        self.current.children.append(newNode)
        self.current = newNode    

    def matchMultiple(self, tokens):
        if self.index < len(self.source):
            if self.source[self.index].tokenClass not in tokens:
                raise Exception("Unexpected token: {} found".format(str(self.source[self.index])))
            self.current.children += [GraphNode('', self.current, self.source[self.index])]
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    #match a token without adding it to the tree
    def matchIgnore(self, token):
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != token:
                raise Exception("Unexpected token: {} found".format(str(self.source[self.index])))
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def match(self, token):
        if self.index < len(self.source):
            if self.source[self.index].tokenClass != token:
                raise Exception("Unexpected token: {} found".format(str(self.source[self.index])))
            self.current.children += [GraphNode('', self.current, self.source[self.index])]
            self.index += 1
        else:
            raise Exception("End of file reached unexpectedly")

    def complete(self):
        self.current.complete = True
        while True:
            if self.current.parent == 0 or not self.current.complete:
                return
            self.current = self.current.parent                  
