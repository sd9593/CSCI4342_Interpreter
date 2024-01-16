#Description: This program reads in a text file from the command line,
# separates the input on white space, and determines if each input sequence 
# follows the given grammar rules.

import sys

def Main():
	inputFile = sys.argv[1] #takes file argument from command line
	input = ""
	inputList = []
	identifierDictionary = {} #dictionary to store identifier token assignments
	input = RemoveTabs_NewLines(inputFile, input)
	inputList = SplitOnSpaces(input)
	LexemeProcessing(inputList, identifierDictionary)

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
	#print(inputList)
	return inputList

#determines if input matches valid token and outputs that token (or invalid)
def LexemeProcessing(inputList, identifierDictionary):
	for item in inputList:
		match item:
			case (
				"(" | ")" | "[" | "]" | "." | "," | ";" | ":" | ".." |
		 		 "not" | "if" | "then" | "else" | "of" | "while" | "do" |
				 "begin" |"end" | "read" | "write" | "var" | "array" |
				 "procedure" | "program"
			):
				identifierDictionary[item] = "Special Keyword"
				print(item + " : Special Keyword Token")
			case (":="):
				identifierDictionary[item] = "Assignment Operator"
				print (item + " : Assignment Operator Token")
			case ("=" | "<>" | "<" | "<=" | ">=" | ">"):
				identifierDictionary[item] = "Relational Operator"
				print (item + " : Relational Operator Token")
			case ("+" | "-" | "or"):
				identifierDictionary[item] = "Adding Operator"
				print (item + " : Adding Operator Token")
			case ("*" | "div" | "and"):
				identifierDictionary[item] = "Multiplying Operator"
				print (item + " : Multiplying Operator Token")
			case ("true" | "false"):
				identifierDictionary[item] = "Predefined Identifier"
				print (item + " : Predefined Identifier Token")
			case ("Integer" | "Boolean"):
				identifierDictionary[item] = "Data Type"
				print (item + " : Data Type Token")
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
						identifierDictionary[item] = "Identifier"
						print (item + " : Identifier Token")
					else:
						identifierDictionary[item] = "Invalid Input"
						print (item + " : Invalid Input")
				elif (item.isdigit()):
					identifierDictionary[item] = "Integer Constant"
					print (item + " : Integer Constant Token")
				else:
					identifierDictionary[item] = "Invalid Input"
					print (item + " : Invalid Input")

Main()