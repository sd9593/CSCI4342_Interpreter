#Description: This program reads in a text file from the command line,
# separates the input on white space, and determines if each input sequence 
# follows the given grammar rules.

import sys

identifierDictionary = {} # dictionary to store identifier value assignments
tokenDictionary = {} #dictionary to store lexeme token assignments

def Main():
	inputFile = sys.argv[1] #takes file argument from command line
	input = ""
	inputList = []
	input = RemoveTabs_NewLines(inputFile, input)
	inputList = SplitOnSpaces(input)
	LexemeProcessing(inputList)
	Parsing(inputList)

#removes tabs and new line characters from read input
def RemoveTabs_NewLines(inputFile, input):
	fin = open(inputFile, "r")
	for line in fin:
		newLine = line.replace('\t', '').replace('\n', ' ')
		input = input + newLine
	fin.close()
	return input

#splits input on spaces and returns list of possible lexemes
def SplitOnSpaces(input):
	inputList = input.split()
	return inputList

#determines if input matches valid token and outputs that token (or invalid)
def LexemeProcessing(inputList):
	for item in inputList:
		match item:
			case (
				"(" | ")" | "[" | "]" | "." | "," | ";" | ":" | ".." |
		 		 "not" | "if" | "then" | "else" | "of" | "while" | "do" |
				 "begin" |"end" | "read" | "write" | "var" | "array" |
				 "procedure" | "program"
			):
				tokenDictionary[item] = "Special Keyword"
			case (":="):
				tokenDictionary[item] = "Assignment Operator"
			case ("=" | "<>" | "<" | "<=" | ">=" | ">"):
				tokenDictionary[item] = "Relational Operator"
			case ("+" | "-" | "or"):
				tokenDictionary[item] = "Adding Operator"
			case ("*" | "div" | "and"):
				tokenDictionary[item] = "Multiplying Operator"
			case ("true" | "false"):
				tokenDictionary[item] = "Predefined Identifier"
			case ("Integer" | "Boolean"):
				tokenDictionary[item] = "Simple Type"
			case _: #default case
				if (item[0:1].isalpha()):
					valid = True
					for i in item:
						if (i.isalpha() | i.isdigit()):
							pass
						else:
							valid = False
							break
					if valid:
						tokenDictionary[item] = "Identifier"
						identifierDictionary[item] = "Null"
					else:
						tokenDictionary[item] = "Invalid Input"
						print (item + " : Invalid Input")
						quit()
				elif (item.isdigit()):
					tokenDictionary[item] = "Integer Constant"
				else:
					tokenDictionary[item] = "Invalid Input"
					print (item + " : Invalid Input")
					quit()

def Parsing(inputList):
	index = 0
	if inputList[0] != "program":
		print("all code must start with being declared as a program")
		quit()
	else:
		ProgramCheck(inputList, index+1)

#<program> -> program <identifier> ; <block> .
def ProgramCheck(inputList, index):
	if tokenDictionary.get(inputList[index]) != "Identifier":
		print ("identifier expected after program declaration")
		quit()
	elif inputList[index+1] != ";":
		print("; expected after identifier in program statement")
		quit()
	else:
		index = BlockCheck(inputList, index+2)
		if inputList[index] != ".":
			print(". expected at end of program")
			quit()
	return index

#<block> -> <variable declaration part> <procedure declaration part> <statement part>
def BlockCheck(inputList, index):
	index = VariableDeclarationPartCheck(inputList, index)
	index = ProcedureDeclarationPartCheck(inputList, index)
	index = StatementPartCheck(inputList, index)
	return index

#<variable declaration part> -> var <variable definition> ; {<variable definition> ;}
#{} are not in language, simply mean any number of what is contained in {}
def VariableDeclarationPartCheck(inputList, index):
	#print("vardecpart")
	if inputList[index] != "var":
		print("var expected before variable declaration")
		quit()
	else:
		index = VariableDeclarationCheck(inputList, index+1)
		if inputList[index] != ";":
			print("; expected after variable declaration")
			quit()
		else:
			index = index + 1
		multipleDeclarations = True
		while multipleDeclarations:
			if tokenDictionary.get(inputList[index]) == "Identifier":
				index = VariableDeclarationCheck(inputList, index)
				if inputList[index] != ";":
					print("; expected after variable declaration")
					quit()
				else:
					index = index + 1
			else:
				multipleDeclarations = False
	return index

#<variable declaration> -> <identifier> {, <identifier>} : <type>
#{} are not in language, simply mean any number of what is contained in {}
def VariableDeclarationCheck(inputList, index):
	#print("vardec")
	if tokenDictionary.get(inputList[index]) != "Identifier":
		print("identifier expected in variable declaration")
		quit()
	else:
		multipleIdentifiers = True
		while multipleIdentifiers:
			if inputList[index+1] == ",":
				if  tokenDictionary.get(inputList[index+2]) == "Identifier":
					index = index + 2
				else:
					multipleIdentifiers = False
			else:
				multipleIdentifiers = False
		if inputList[index+1] != ":":
			print(": expected after identifiers in variable declaration")
			quit()
		else:
			index = TypeCheck(inputList, index+2)
	return index

#<type> -> <simple type> | <array type>
#| not actually in language, just means one or the other
def TypeCheck(inputList, index):
	#print("type")
	if tokenDictionary.get(inputList[index]) != "Simple Type":
		index = ArrayTypeChecker(inputList, index)
	else:
		index = index + 1
	return index

#<array type> -> array [ <index range> ] of <simple type>
def ArrayTypeChecker(inputList, index):
	#print("arraytype")
	if inputList[index] != "array":
		print("array expected for array type")
		quit()
	elif inputList[index+1] != "[":
		print("[ expected for array type")
		quit()
	else:
		index = IndexRangeCheck(inputList, index+2)
		if inputList[index] != "]":
			print("] expected for array type")
			quit()
		elif inputList[index+1] != "of":
			print("of expected for array type")
			quit()
		elif tokenDictionary.get(inputList[index+2]) != "Simple Type":
			print("simple type expected for array type")
			quit()
		else:
			index = index + 3
	return index

#<index range> -> <integer constant> .. <integer constant>
def IndexRangeCheck(inputList, index):
	#print("indexrange")
	if tokenDictionary.get(inputList[index]) != "Integer Constant":
		print("integer constant expected for index range")
		quit()
	elif inputList[index+1] != "..":
		print(".. expected for index range")
		quit()
	elif tokenDictionary.get(inputList[index+2]) != "Integer Constant":
		print("integer constant expected for index range")
		quit()
	else:
		index = index + 3
	return index

#<procedure declaration part> -> {<procedure declaration> ;}
#{} are not in language, simply mean any number of what is contained in {}
def ProcedureDeclarationPartCheck(inputList, index):
	#print("procdecpart")
	if inputList[index] == "procedure":
		index = ProcedureDeclarationCheck(inputList, index)
		if inputList[index] != ";":
			print("; expected after procedure declaration")
			quit()
		else:
			index = index + 1
			multipleProcedures = True
			while multipleProcedures:
				if inputList[index] == "procedure":
					index = ProcedureDeclarationCheck(inputList, index)
					if inputList[index] != ";":
						print("; expected in procedure declaration")
						quit()
					else:
						index = index + 1
				else:
					multipleProcedures = False
	return index

#<procedure declaration> -> procedure <identifier> ; <block>
def ProcedureDeclarationCheck(inputList, index):
	#print("procdec")
	if inputList[index] != "procedure":
		print("procedure expected in procedure declaration")
		quit()
	elif tokenDictionary.get(inputList[index+1]) != "Identifier":
		print("identifier expected in procedure declaration")
		quit()
	elif inputList[index + 2] != ";":
		print("; expected in procedure declaration")
		quit()
	else:
		index = BlockCheck(inputList, index+3)
	return index

#statement part> -> <compound statement>
def StatementPartCheck(inputList, index):
	#print("statpart")
	index = CompoundStatementCheck(inputList, index)
	return index

#<compound statement> -> begin <statement> {<statement>} end
#{} are not in language, simply mean any number of what is contained in {}
def CompoundStatementCheck(inputList, index):
	#print("compstat")
	if inputList[index] != "begin":
		print("begin expected in compound statement")
		quit()
	else:
		index = StatementCheck(inputList, index+1)
		if inputList[index] != "end":
			multipleStatements = True
			while multipleStatements:
				if inputList[index] != "end":
					index = StatementCheck(inputList, index )
				else:
					multipleStatements = False
			if inputList[index] != "end":
				print("end expected in compound statement")
				quit()
			else:
				index = index + 1
		else:
			index = index + 1
	return index

#<statement> -> <simple statement> ; | <structured statement>
#| not actually in language, just means one or the other
def StatementCheck(inputList, index):
	#print("stat")
	if inputList[index] == "begin":
		index = StructuredStatementCheck(inputList, index)
	elif inputList[index] == "if":
		index = StructuredStatementCheck(inputList, index)
	elif inputList[index] == "while":
		index = StructuredStatementCheck(inputList, index)
	else:
		index = SimpleStatementCheck(inputList, index)
		if inputList[index] != ";":
			print("; expected after simple statement")
			quit()
		else:
			index = index + 1
	return index

#<simple statement> -> <assignment statement> | <procedure statment> | <read statement> | <write statement>
#| not actually in language, just means one or the other
def SimpleStatementCheck(inputList, index):
	#print("simplestat")
	if inputList[index] == "read":
		index = ReadStatementCheck(inputList, index)
	elif inputList[index] == "write":
		index = WriteStatementCheck(inputList, index)
	else:
		if inputList[index + 1] == ":=":
			index = AssignmentStatementCheck(inputList, index)
		else:
			index = ProcedureStatementCheck(inputList, index)
	return index

def ProcedureStatementCheck(inputList, index):
	if tokenDictionary.get(inputList[index]) != "Identifier":
		print("identifier expected in procedure statement")
		quit()
	else:
		index = index + 1
	return index

#<read statement> -> read ( <input variable> )
def ReadStatementCheck(inputList, index):
	#print("readstat")
	if inputList[index] != "read":
		print("read expected in read statement")
		quit()
	elif inputList[index+1] != "(":
		print("( expected in read statement")
		quit()
	else:
		index = InputVariableCheck(inputList, index+2)
		if inputList[index] != ")":
			print(") expected in read statement")
			quit()
		else:
			index = index + 1
	return index

#<input variable> -> <variable>
def InputVariableCheck(inputList, index):
	#print("inputvar")
	index = VariableCheck(inputList, index)
	return index

#<variable> -> <entire variable> | <indexed variable>
#<entire variable> -> <variable identifier>
#<variable identifier> -> <identifier>
#| not actually in language, just means one or the other
def VariableCheck(inputList, index):
	#print("varc")
	if tokenDictionary.get(inputList[index]) != "Identifier":
		print("identifier expected in variable")
		quit()
	elif inputList[index+1] == "[":
		index = IndexedVariableCheck(inputList, index)
	else:
		index = index + 1
	return index

#<indexed variable> -> <array variable> [ <expression> ]
#<array variable> -> <entire variable>
#<entire variable> -> <variable identifier>
#<variable identifier> -> <identifier>
def IndexedVariableCheck(inputList, index):
	#print("indexvar")
	if tokenDictionary.get(inputList[index]) != "Identifier":
		print("identifier expected in indexed variable")
		quit()
	elif inputList[index+1] != "[":
		print("[ expected in indexed variable")
		quit()
	else:
		index = ExpressionCheck(inputList, index+2) 
		if inputList[index] != "]":
			print("] expected in indexed variable")
			quit()
		else:
			index = index +1
	return index

#<expression> -> <simple expression> | <simple expression> <relational operator> <simple expression>
#| not actually in language, just means one or the other
def ExpressionCheck(inputList, index):
	#print("expr")
	index = SimpleExpressionCheck(inputList, index)
	if tokenDictionary.get(inputList[index]) == "Relational Operator":
		index = SimpleExpressionCheck(inputList, index +1)
	return index

#<simple expression> -> <term> {<adding operator> <term>}
#{} are not in language, simply mean any number of what is contained in {}
def SimpleExpressionCheck(inputList, index):
	#print("simpleexpr")
	index = TermCheck(inputList, index)
	multipleTerms = True
	while multipleTerms:
		if tokenDictionary.get(inputList[index]) == "Adding Operator":
			index = TermCheck(inputList, index+1)
		else:
			multipleTerms = False
	return index

#<term> -> <factor> {<mutiplying operator> <factor>}
#{} are not in language, simply mean any number of what is contained in {}
def TermCheck(inputList, index):
	#print("term")
	index = FactorCheck(inputList, index)
	multipleFactors = True
	while multipleFactors:
		if tokenDictionary.get(inputList[index]) == "Multiplying Operator":
			index = FactorCheck(inputList, index+1)
		else:
			multipleFactors = False
	return index

#<factor> -> <variable> | <constant> | ( <expression> ) | not <factor>
#| not actually in language, just means one or the other
def FactorCheck(inputList, index):
	#print("factor")
	if inputList[index] == "(":
		index = ExpressionCheck(inputList, index + 1)
		if inputList[index] != ")":
			print(") expected in factor")
			quit()
		else:
			index = index + 1
	elif inputList[index] == "not":
		index = FactorCheck(inputList, index + 1)
	elif tokenDictionary.get(inputList[index]) == "Integer Constant":
		index = index + 1
	elif tokenDictionary.get(inputList[index]) == "Predefined Identifier":
		index = index + 1
	else:
		index = VariableCheck(inputList, index)
	return index

#<write> -> write ( <output value> )
#<output value> -> <expression>
def WriteStatementCheck(inputList, index):
	#print("writestat")
	if inputList[index] != "write":
		print("write expected in write statement")
		quit()
	elif inputList[index+1] != "(":
		print("( expected in write statement")
		quit()
	else:
		index = ExpressionCheck(inputList, index+2)
		if inputList[index] != ")":
			print(") expected in write statement")
			quit()
		else:
			index = index + 1
	return index

#<assignment statement> -> <variable> := <expression>
def AssignmentStatementCheck(inputList, index):
	#print("assignstat")
	index = VariableCheck(inputList, index)
	if inputList[index] != ":=":
		print(":= expected for assignment statement")
		quit()
	else:
		index = ExpressionCheck(inputList, index+1)
	return index

#<structured statement> -> <compound statement> | <if statement> | <while statment>
#| not actually in language, just means one or the other
def StructuredStatementCheck(inputList, index):
	#print("structstat")
	if inputList[index] == "if":
		index = IfStatementCheck(inputList, index)
	elif inputList[index] == "while":
		index = WhileStatementCheck(inputList, index)
	elif inputList[index] == "begin":
		index = CompoundStatementCheck(inputList, index)
	return index

#<if statement> -> if <expression> then <statement> | if <expression> then <statement> else <statement>
#| not actually in language, just means one or the other
def IfStatementCheck(inputList, index):
	#print("ifstat")
	if inputList[index] != "if":
		print("if expected for if statement")
		quit()
	else:
		index = ExpressionCheck(inputList, index+1)
		if inputList[index] != "then":
			print("then expected for if statement")
			quit()
		else:
			index = StatementCheck(inputList, index+1)
			if inputList[index] == "else":
				index = StatementCheck(inputList, index+1)
	return index

#<while statement> -> while <expression> do <statement>
def WhileStatementCheck(inputList, index):
	#print("whilestat")
	if inputList[index] != "while":
		print("while expected for while statement")
		quit()
	else:
		index = ExpressionCheck(inputList, index+1)
		if inputList[index] != "do":
			print("do expected for while statement")
			quit()
		else:
			index = StatementCheck(inputList, index+1)
	return index

Main()