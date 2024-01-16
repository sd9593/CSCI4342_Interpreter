#Description: This program reads in a text file from the command line,
# separates the input on white space, and determines if each input sequence 
# follows the given grammar rules. Additionally it performs processing for 
# variable manipulation not including loops or procedures. All variables 
# given default values upon declaration (0 for Integer, true for Boolean) 
# Arrays included in processing assuming range is inclusive of upper bound 
# and range values cannot be negative.

import sys

identifierDictionary = {} # dictionary to store identifier value assignments
tokenDictionary = {} #dictionary to store lexeme token assignments
integerDictionary = {} #dictionary to store integer identifier value assignments
booleanDictionary = {} #dictionary to store boolean identifier value assignments
integerArrayDictionary = {} #dictionary to store integer array identifer value assignments
booleanArrayDictionary = {} #dictionary to store boolean array indentifier value assignments
procedureIdentifierDictionary = {} #dictionary to store procedure identifiers and their start and end

def Main():
	inputFile = sys.argv[1] #takes file argument from command line
	input = ""
	inputList = []
	input = RemoveTabs_NewLines(inputFile, input)
	inputList = SplitOnSpaces(input)
	LexemeProcessing(inputList)
	Parsing(inputList)
	BasicIteration(inputList)
 
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
				elif (isNumber(item)):
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
# if simple type, add each variable to appropriate dictionary
def TypeCheck(inputList, index):
	#print("type")
	if tokenDictionary.get(inputList[index]) != "Simple Type":
		index = ArrayTypeCheck(inputList, index)
	else:
		if inputList[index] == "Integer":
			if ((not inputList[index-2] in integerDictionary) & (not inputList[index-2] in booleanDictionary)
	   			 & (not inputList[index-2] in integerArrayDictionary) & (not inputList[index-2] in booleanArrayDictionary)):
				integerDictionary[inputList[index-2]] = "0"
				if inputList[index - 3] == ",":
					if ((not inputList[index-4] in integerDictionary) & (not inputList[index-4] in booleanDictionary)
	   					& (not inputList[index-4] in integerArrayDictionary) & (not inputList[index-4] in booleanArrayDictionary)):
						integerDictionary[inputList[index - 4]] = "0"
					else:
						print("variable already exists")
						quit()
					curr = index - 5
					while inputList[curr] == ",":
						if ((not inputList[curr-1] in integerDictionary) & (not inputList[curr-1] in booleanDictionary)
		  					& (not inputList[curr-1] in integerArrayDictionary) & (not inputList[curr-1] in booleanArrayDictionary)):
							integerDictionary[inputList[curr-1]] = "0"
						else:
							print("variable already exists")
							quit()
						curr -= 2
			else:
				print("variable already exists")
				quit()
			#print(integerDictionary)
		if inputList[index] == "Boolean":
			if ((not inputList[index-2] in integerDictionary) & (not inputList[index-2] in booleanDictionary)
	   			 & (not inputList[index-2] in integerArrayDictionary) & (not inputList[index-2] in booleanArrayDictionary)):
				booleanDictionary[inputList[index-2]] = "true"
			else:
				print("variable already exists")
				quit()
			if inputList[index - 3] == ",":
				if ((not inputList[index-4] in integerDictionary) & (not inputList[index-4] in booleanDictionary)
	   				& (not inputList[index-4] in integerArrayDictionary) & (not inputList[index-4] in booleanArrayDictionary)):
					booleanDictionary[inputList[index - 4]] = "true"
				else:
					print("variable already exists")
					quit()
				curr = index - 5
				while inputList[curr] == ",":
					if ((not inputList[curr-1] in integerDictionary) & (not inputList[curr-1] in booleanDictionary)
		  				& (not inputList[curr-1] in integerArrayDictionary) & (not inputList[curr-1] in booleanArrayDictionary)):
						booleanDictionary[inputList[curr-1]] = "true"
					else:
						print("variable already exists")
						quit()
					curr -= 2
			#print(booleanDictionary)
		index = index + 1
	return index

#<array type> -> array [ <index range> ] of <simple type>
def ArrayTypeCheck(inputList, index):
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
			if inputList[index + 2] == "Integer":
				if ((not inputList[index-7] in integerArrayDictionary) & (not inputList[index-7] in integerDictionary)
					& (not inputList[index-7] in booleanDictionary) & (not inputList[index-7] in booleanArrayDictionary)):
					integerArrayDictionary[inputList[index-7]] = ["Null"] * (int(inputList[index-1])+1)
					#create array of Null of size max range
					for x in range(int(inputList[index-1])+1):
						if (x >= int(inputList[index-3])) & (x < int(inputList[index-1])+1):
							integerArrayDictionary[inputList[index-7]][x] = "0"
							#initialize in-range indexes to 0
				else:
					print("variable already exists")
					quit()
				if inputList[index - 8] == ",":
					if ((not inputList[index-9] in integerArrayDictionary) & (not inputList[index-9] in integerDictionary)
						& (not inputList[index-9] in booleanDictionary) & (not inputList[index-9] in booleanArrayDictionary)):
						integerArrayDictionary[inputList[index-9]] = ["Null"] * (int(inputList[index-1])+1)
						#create array of Null of size max range
						for x in range(int(inputList[index-1])+1):
							if (x >= int(inputList[index-3])) & (x < (int(inputList[index-1])+1)):
								integerArrayDictionary[inputList[index-9]][x] = "0"
								#initialize in-range indexes to 0
					else:
						print("variable already exists")
						quit()
					curr = index - 10
					while inputList[curr] == ",":
						if ((not inputList[curr-1] in integerArrayDictionary) & (not inputList[curr-1] in integerDictionary) 
		  					& (not inputList[curr-1] in booleanDictionary) & (not inputList[curr-1] in booleanArrayDictionary)):
							integerArrayDictionary[inputList[curr - 1]] = ["Null"] * (int(inputList[index-1])+1)
							#create array of Null of size max range
							for x in range(int(inputList[index-1])+1):
								if (x >= int(inputList[index-3])) & (x < (int(inputList[index-1])+1)):
									integerArrayDictionary[inputList[curr-1]][x] = "0"
									#initialize in-range indexes to 0
						else:
							print("variable already exists")
							quit()
						curr -= 2
				#print(integerArrayDictionary)
			elif inputList[index + 2] == "Boolean":
				if ((not inputList[index-7] in integerArrayDictionary) & (not inputList[index-7] in integerDictionary)
					& (not inputList[index-7] in booleanDictionary) & (not inputList[index-7] in booleanArrayDictionary)):
					booleanArrayDictionary[inputList[index-7]] = ["Null"] * (int(inputList[index-1])+1)
					#create array of Null of size max range
					for x in range(int(inputList[index-1])+1):
						if (x >= int(inputList[index-3])) & (x < (int(inputList[index-1])+1)):
							booleanArrayDictionary[inputList[index-7]][x] = "true"
							#initialize in-range indexes to True
				else:
					print("variable already exists")
					quit()
				if inputList[index - 8] == ",":
					if ((not inputList[index-9] in integerArrayDictionary) & (not inputList[index-9] in integerDictionary)
						& (not inputList[index-9] in booleanDictionary) & (not inputList[index-9] in booleanArrayDictionary)):
						booleanArrayDictionary[inputList[index-9]] = ["Null"] * (int(inputList[index-1])+1)
						#create array of Null of size max range
						for x in range(int(inputList[index-1])+1):
							if (x >= int(inputList[index-3])) & (x < int(inputList[index-1])+1):
								booleanArrayDictionary[inputList[index-9]][x] = "true"
								#initialize in-range indexes to True
					else:
						print("variable already exists")
						quit()
					curr = index - 10
					while inputList[curr] == ",":
						if ((not inputList[curr-1] in integerArrayDictionary) & (not inputList[curr-1] in integerDictionary) 
		  					& (not inputList[curr-1] in booleanDictionary) & (not inputList[curr-1] in booleanArrayDictionary)):
							booleanArrayDictionary[inputList[curr - 1]] = ["Null"] * (int(inputList[index-1])+1)
							#create array of Null of size max range
							for x in range(int(inputList[index-1])+1):
								if (x >= int(inputList[index-3])) & (x < (int(inputList[index-1])+1)):
									booleanArrayDictionary[inputList[curr-1]][x] = "true"
									#initialize in-range indexes to True
						else:
							print("variable already exists")
							quit()
						curr -= 2
				#print(booleanArrayDictionary)
			index = index + 3
	return index

#<index range> -> <integer constant> .. <integer constant>
#throws error if upper bound is less than or equal to lower bound
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
		#array range cannot contain negative numbers and upper bound must be greater or equal
		if (int(inputList[index+2]) < int(inputList[index])) | (int(inputList[index+2]) < 0) | (int(inputList[index]) < 0):
			print("invalid index range for array")
			quit()
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
#adds procedure identifier to procedureIdentifierArray with start and end index
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
		procedureIdentifierDictionary[inputList[index+1]] = [inputList[index+3], BlockCheck(inputList, index+3)]
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
		if inputList[index] in procedureIdentifierDictionary:
			index = ProcedureStatementCheck(inputList, index)
		else:
			index = AssignmentStatementCheck(inputList, index)
	return index

#<procedure statement> -> <procedure identifier>
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

#<factor> -> <variable> | <integer constant> | ( <expression> ) | not <factor>
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

#Handles basic iteration (no loops, conditionals, or procedures)
def BasicIteration(inputList):
	location = 0
	while location < len(inputList):
		currentExpression = []
		readValue = ""
		result = ""
		arrayIndexExpression = []
		if inputList[location] == "read":
		#user can enter expression as input value
			if inputList[location+2] in integerDictionary:
				currentExpression = input().split()
				readValue = ExpressionEvaluation(currentExpression)
				if isNumber(readValue) == False:
					print("Invalid assignment: non-integer to integer")
					quit()
				else:
					integerDictionary[inputList[location+2]] = readValue
			elif inputList[location+2] in booleanDictionary:
				readValue = ExpressionEvaluation(input().split())
				if (isBoolean(readValue) == False):
					print("Invalid assignment: non-boolean to boolean")
					quit()
				else:
					booleanDictionary[inputList[location+2]] = readValue
			elif inputList[location + 2] in integerArrayDictionary:
				i = location + 4
				while inputList[i] != "]":
					arrayIndexExpression.append(inputList[i])
					i += 1
				arrayIndex = ExpressionEvaluation(arrayIndexExpression)
				if isNumber(arrayIndex):
					if (int(arrayIndex) >= len(integerArrayDictionary[inputList[location+2]])) | (int(arrayIndex) < 0):
						print("index out of range for array")
						quit()
					elif integerArrayDictionary[inputList[location+2]][int(arrayIndex)] == "Null":
						print("index out of range for array")
						quit()
					else:
						readValue = ExpressionEvaluation(input().split())
						if isNumber(readValue) == False:
							print("Invalid assignment: non-integer to integer")
							quit()
						else:
							integerArrayDictionary[inputList[location+2]][int(arrayIndex)] = readValue
			elif inputList[location + 2] in booleanArrayDictionary:
				i = location + 4
				while inputList[i] != "]":
					arrayIndexExpression.append(inputList[i])
					i += 1
				arrayIndex = ExpressionEvaluation(arrayIndexExpression)
				if isNumber(arrayIndex):
					if (int(arrayIndex) >= len(booleanArrayDictionary[inputList[location+2]])) | (int(arrayIndex) < 0):
						print("index out of range for array")
						quit()
					elif booleanArrayDictionary[inputList[location+2]][int(arrayIndex)] == "Null":
						print("index out of range for array")
						quit()
					else:
						readValue = ExpressionEvaluation(input().split())
						if isBoolean(readValue) == False:
							print("Invalid assignment: non-boolean to boolean")
							quit()
						else:
							booleanArrayDictionary[inputList[location+2]][int(arrayIndex)] = readValue
			else:
				print("Variable does not exist")
				quit()
		if inputList[location] == ":=":
			i = location + 1
			while inputList[i] != ";":
				currentExpression.append(inputList[i])
				i += 1
			if inputList[location-1] in integerDictionary:
				result = ExpressionEvaluation(currentExpression)
				if isNumber(result) == False:
					print("Invalid assignment: non-integer to integer")
					quit()
				else:
					integerDictionary[inputList[location - 1]] = result
			elif inputList[location-1] in booleanDictionary:
				result = ExpressionEvaluation(currentExpression)
				if (isBoolean(result) == False):
					print("Invalid assignment")
					quit()
				else:
					booleanDictionary[inputList[location -1]] = result
			elif inputList[location-1] =="]":
				i = location - 2
				while inputList[i] != "[":
					arrayIndexExpression.insert(0,inputList[i])
					#insert used to maintain correct order of expression
					i -= 1
				arrayIndex = ExpressionEvaluation(arrayIndexExpression)
				if inputList[i-1] in integerArrayDictionary:
					if isNumber(arrayIndex):
						if (int(arrayIndex) >= len(integerArrayDictionary[inputList[i-1]])) | (int(arrayIndex) < 0):
							print("index out of range for array")
							quit()
						elif integerArrayDictionary[inputList[i-1]][int(arrayIndex)] == "Null":
							print("index out of range for array")
							quit()
						else:
							result = ExpressionEvaluation(currentExpression)
							if isNumber(result) == False:
								print("Invalid assignment: non-integer to integer")
								quit()
							else:
								integerArrayDictionary[inputList[i-1]][int(arrayIndex)] = result
				if inputList[i-1] in booleanArrayDictionary:
					if isNumber(arrayIndex):
						if (int(arrayIndex) >= len(booleanArrayDictionary[inputList[i-1]])) | (int(arrayIndex) < 0):
							print("index out of range for array")
							quit()
						elif booleanArrayDictionary[inputList[i-1]][int(arrayIndex)] == "Null":
							print("index out of range for array")
							quit()
						else:
							result = ExpressionEvaluation(currentExpression)
							if isBoolean(result) == False:
								print("Invalid assignment: non-boolean to boolean")
								quit()
							else:
								booleanArrayDictionary[inputList[i-1]][int(arrayIndex)] = result
		if inputList[location] == "write":
			i = location + 2
			while inputList[i] != ";":
				currentExpression.append(inputList[i])
				i += 1
			currentExpression.pop()
			result = ExpressionEvaluation(currentExpression)
			#print("write")
			print(result)
		location += 1
	#print(booleanDictionary)
	#print(integerDictionary)
	
#Processes expressions 
def ExpressionEvaluation(currentExpression):
	index = 0
	nestedExpression = []
	# parse for nested expressions: (<expression>)
	while index < len(currentExpression):
		nestedExpression = []
		if currentExpression[index] == "(":
			i = index + 1
			while i < len(currentExpression):
				if currentExpression[i] == "(":
					#allows multi-nested expressions
					j = i
					while (j < len(currentExpression)):
						if currentExpression[j] != ")":
							nestedExpression.append(currentExpression[j])
							del currentExpression[j]
							j = j - 1
						else:
							del currentExpression[j]
							j = j - 1
							break
						j = j + 1
				if currentExpression[i] == ")":
					del currentExpression[i]
					i = i - 1
					break
				elif currentExpression[i] != ")":
					nestedExpression.append(currentExpression[i])
					del currentExpression[i]
					i = i - 1
				i = i + 1
			currentExpression[index] = ExpressionEvaluation(nestedExpression)
		index += 1
	index = 0
	# parse all identifiers into integers or booleans
	while index < len(currentExpression):
		if currentExpression[index] in tokenDictionary:
			if tokenDictionary[currentExpression[index]] == "Identifier":
				if currentExpression[index] in integerDictionary:
					currentExpression[index] = integerDictionary[currentExpression[index]]				
				elif currentExpression[index] in booleanDictionary:
					currentExpression[index] = booleanDictionary[currentExpression[index]]
				elif currentExpression[index] in integerArrayDictionary:
					if currentExpression[index+1] == "[":
						del currentExpression[index+1]
						i = index + 1
						while i < len(currentExpression):
							if currentExpression[i] == "]":
								del currentExpression[i]
								break
							elif currentExpression[i] != "]":
								nestedExpression.append(currentExpression[i])
								del currentExpression[i]
								i = i - 1
							i = i + 1
						arrayIndex = ExpressionEvaluation(nestedExpression)
						if isNumber(arrayIndex):
							if (int(arrayIndex) >= len(integerArrayDictionary[currentExpression[index]])) | (int(arrayIndex) < 0):
								print("index out of range for array")
								quit()
							elif integerArrayDictionary[currentExpression[index]][int(arrayIndex)] == "Null":
								print("index out of range for array")
								quit()
							else:
								currentExpression[index] = integerArrayDictionary[currentExpression[index]][int(arrayIndex)]
				elif currentExpression[index] in booleanArrayDictionary:
					if currentExpression[index+1] == "[":
						del currentExpression[index+1]
						i = index + 1
						while i < len(currentExpression):
							if currentExpression[i] == "]":
								del currentExpression[i]
								break
							elif currentExpression[i] != "]":
								nestedExpression.append(currentExpression[i])
								del currentExpression[i]
								i = i - 1
							i = i + 1
						arrayIndex = ExpressionEvaluation(nestedExpression)
						if isNumber(arrayIndex):
							if (int(arrayIndex) >= len(booleanArrayDictionary[currentExpression[index]])) | (int(arrayIndex) < 0):
								print("index out of range for array")
								quit()
							elif booleanArrayDictionary[currentExpression[index]][int(arrayIndex)] == "Null":
								print("index out of range for array")
								quit()
							else:
								currentExpression[index] = booleanArrayDictionary[currentExpression[index]][int(arrayIndex)]
						else:
							print("only integers can address array index")
							quit()
		index += 1
	index = 0
	nestedExpression = []
	# parse for not <factor>
	while index < len(currentExpression):
		nottedVariable = "true"
		if currentExpression[index] == "not":
			nestedExpression.append(currentExpression[index])
			i = index + 1
			while i < len(currentExpression):
				if currentExpression[i] == "not":
					nestedExpression.append(currentExpression[i])
					del currentExpression[i]
					i = i - 1
				else:
					if isBoolean(currentExpression[i]):
						nottedVariable = PythonBooleanValue(currentExpression[i])
						del currentExpression[i]
						i = i - 1
					else:
						print("Cannot apply not to non-boolean")
						quit()
					break
				i = i + 1
			i = 0
			while i < len(nestedExpression):
				if nestedExpression[i] == "not":
					nottedVariable = not (nottedVariable)
				i = i + 1
			currentExpression[index] = SFAscalBooleanValue(nottedVariable)
		index = index + 1
	index = 0
	# parse and compute multiplication/division/and
	# precedence is left-to-right
	while index < len(currentExpression):
		if currentExpression[index] == "*":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = int(currentExpression[index - 1]) * int(currentExpression[index + 1])
				del currentExpression[index] # removes *
				del currentExpression[index] # removes second number
				index = index - 1
			else:
				print("Non-integer variable not allowed in multiplication")
				quit()
		if currentExpression[index] == "div":
			# if result is not integer, round to next lower integer
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = int(int(currentExpression[index - 1]) / int(currentExpression[index + 1]))
				del currentExpression[index] # removes div
				del currentExpression[index] # removes second number
				index = index - 1
			else:
				print("Non-integer variable not allowed in division")
				quit()
		if currentExpression[index] == "and":
			if ((isBoolean(str(currentExpression[index - 1]))) &
				(isBoolean(str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(PythonBooleanValue(currentExpression[index - 1]) & PythonBooleanValue(currentExpression[index + 1]))
				del currentExpression[index] # removes and
				del currentExpression[index] # removes second boolean
				index = index - 1
			else:
				print("Non-boolean variable not allowed in and")
				quit()
		index = index + 1
	index = 0
	# parse and compute addition/subtraction/or
	# precedence is left-to-right
	while index < len(currentExpression):
		if currentExpression[index] == "+":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = int(currentExpression[index - 1]) + int(currentExpression[index + 1])
				del currentExpression[index] # removes +
				del currentExpression[index] # removes second number
				index = index - 1
			else:
				print("Non-integer variable not allowed in addition")
		if currentExpression[index] == "-":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = int(currentExpression[index - 1]) - int(currentExpression[index + 1])
				del currentExpression[index] # removes -
				del currentExpression[index] # removes second number
				index = index - 1
			else:
				print("Non-integer variable not allowed in subtraction")
				quit()
		if currentExpression[index] == "or":
			if ((isBoolean(str(currentExpression[index - 1]))) &
				(isBoolean(str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(PythonBooleanValue(currentExpression[index - 1]) | PythonBooleanValue(currentExpression[index + 1]))
				del currentExpression[index] # removes or
				del currentExpression[index] # removes second boolean
				index = index - 1
			else:
				print("Non-boolean variable not allowed in and")
				quit()
		index = index + 1
	index = 0
	# parse and compute relational operators
	# precedence is left-to-right
	while index < len(currentExpression):
		if currentExpression[index] == "=":
			# types on either side don't matter, only equality
			currentExpression[index - 1] = SFAscalBooleanValue(str(currentExpression[index - 1]) == str(currentExpression[index + 1]))
			del currentExpression[index] # removes =
			del currentExpression[index] # removes second value
			index = index - 1
		if currentExpression[index] == "<>": # same as !=
			# types on either side don't matter, only equality
			currentExpression[index - 1] = SFAscalBooleanValue(str(currentExpression[index - 1]) != str(currentExpression[index + 1]))
			del currentExpression[index] # removes =
			del currentExpression[index] # removes second value
			index = index - 1
		if currentExpression[index] == "<":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(int(currentExpression[index - 1]) < int(currentExpression[index + 1]))
				del currentExpression[index] # removes <
				del currentExpression[index] # removes second number
				index = index - 1
		if currentExpression[index] == "<=":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(int(currentExpression[index - 1]) <= int(currentExpression[index + 1]))
				del currentExpression[index] # removes <=
				del currentExpression[index] # removes second number
				index = index - 1
		if currentExpression[index] == ">=":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(int(currentExpression[index - 1]) >= int(currentExpression[index + 1]))
				del currentExpression[index] # removes >=
				del currentExpression[index] # removes second number
				index = index - 1
		if currentExpression[index] == ">":
			if (isNumber((str(currentExpression[index - 1]))) &
				isNumber((str(currentExpression[index + 1])))):
				currentExpression[index - 1] = SFAscalBooleanValue(int(currentExpression[index - 1]) > int(currentExpression[index + 1]))
				del currentExpression[index] # removes >
				del currentExpression[index] # removes second number
				index = index - 1
		index = index + 1

	# final case after all computation
	if (len(currentExpression) == 1):
		return str(currentExpression[0])

# determines whether a value is an integer
def isNumber(input):
	try:
		int(input)
	except:
		return False
	return True

# determines whether current value is a boolean in the language
def isBoolean(currentInput):
	isBoolean = True
	if ((currentInput != "false") & (currentInput != "true")):
		isBoolean = False
	return isBoolean

# Translates current boolean input from SFAscal to Python's boolean
def PythonBooleanValue(currentInput):
	booleanValue = False
	if currentInput == "true":
		booleanValue = True
	return booleanValue

# Translates current boolean Input from Python to SFAscal
def SFAscalBooleanValue(currentInput):
	booleanValue = "false"
	if currentInput == True:
		booleanValue = "true"
	return booleanValue

Main()