requires graphviz

Install
-------------

Requires graphviz. 

For windows
1. Download from http://www.graphviz.org/
2. Add the bin directory (e.g. C:\Program Files (x86)\Graphviz2.38\bin) to the system PATH.
3. Install the python wrapper with pip install graphviz

Usage
--------------

usage: main.py [-h] [-o O] [-g G] [-l L] [-v] input

First Order Logic Parser.

positional arguments:
  input       The input file

optional arguments:
  -h, --help  show this help message and exit
  -o O        The output file for the tree (output by default)
  -g G        The output file for the grammar (grammar.txt by default)
  -l L        The log file (log.txt by default)
  -v          View the file after rendering it

The program reads a file in the format specified by the coursework specification,
generates the relevant parse tree, and outputs that as both a dot file (used by graphviz) and a pdf. 
It also outputs the grammar to both the log file and the grammar file specified. A simple sucess/fail 
message is displayed in the console (stdout), see the log file for slightly more information.

e.g. python main.py example.txt -o parseTree -l logTest.txt -v
This will read input for example.txt, output the dot file to parseTree, 
the pdf to parseTree.pdf, and the log file to logTest.txt. It will also automaticly 
open the pdf file.

Errors
-------

Here are same example errors:

Unexpected token: [type: BRACKET_START, Name: '(', position: 9] found, expecting a token of type: VARIABLE
Invalid token: xk in formula at position: 8

Position here means this token is found in the 9th position in the input formula (indexing starts at 0,
ignoring all whitespace preceding the formula).

The program will terminate after encountering an error.

Input file format
-----------------

As previously stated, this is identical to the format specified in the specification.
It must contain a set of labels (variables:, constants:, predicates:, equality, connectives:, formula:),
and a matching set of data after each label. For the formula, this is just the formula to parse, for
the other labels, this is a list of items. Their must be 1 equality symbol, 2 quantifiers (exists, and foreach respectivley), and 5 connectives (and, or , implies, iff and negation). For predicates, the items are followed by a set of square brackets
which contain the arity of the predicate. For example: 

variables: w x y z
constants: C D
predicates: P[2] Q[1]
equality: =
connectives: \land \lor \implies \iff \neg
quantifiers: \exists \forall
formula: \forall x ( \exists y ( P(x,y) \implies \neg Q(x) )
\lor \exists z ( ( (C = z) \land Q(z) ) \land P(x,z) ) )

