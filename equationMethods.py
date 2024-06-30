# armanAPI.py

class MathList(list):
    def appendNotNull(self, item): # helper method to append non-null items
        if item:
            self.append(item)

# preprocess the equation, removing excess space and converting for the right format
def preprocessEquation(equation):
    equation = equation.replace("\\div", "/")
    equation = equation.replace(" ", "")
    return equation

# splits numbers, parenthesis, operators
def mathSplitElements(equation):
    # create result list and string element builder
    result = MathList()
    current = ''
    #equation = preprocessEquation(stringEquation)

    operators = {'+', '-', '*', '/', '^'}
    opening_parenthesis = {'(', '[', '{'}
    closing_parenthesis = {')', ']', '}'}

    for char in equation:
        if(char in opening_parenthesis or char in closing_parenthesis or char in operators):
            result.appendNotNull(current)
            result.append(char)
            current = ''
        else:
            current += char
    result.appendNotNull(current)

    return result

def groupParenthesis(equation):
    #equation = mathSplitElements(stringEquation)
    result = MathList()
    
    def findEndParenthesis(index):
        parenthesis = MathList()
        if equation[index] == "(":
            find = ")"
        elif equation[index] == "[":
            find = "]"
        elif equation[index] == "{":
            find = "}"
        index += 1
        while index < len(equation):
            if equation[index] in "([{":
                parenthesis.append(findEndParenthesis(index))
            elif equation[index] == find:
                return (parenthesis, index)
            else:
                parenthesis.append(equation[index])
            index+=1

        return (parenthesis, index)

    i = 0
    while i < (len(equation)):
        if(equation[i] == "(" or equation[i] == "[" or equation[i] == "{"):
            par, i = findEndParenthesis(i)
            result.append(par)
        else:
            result.append(equation[i])
        i+=1
    if(len(result) == 1):
        return result[0]
    return result