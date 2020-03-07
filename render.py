from graphviz import Digraph, escape


def drawTree(rootNode, outputFile, view=False):
    dot = Digraph(comment="Parse Tree")

    addTree(rootNode, dot)

    dot.render(outputFile, view=view)


def addTree(rootNode, dot):
    dot.node(str(id(rootNode)), escape(rootNode.identifier if rootNode.token == 0 else rootNode.token.name))
    for x in rootNode.children:
        addTree(x, dot)
        dot.edge(str(id(rootNode)), str(id(x)))
       
