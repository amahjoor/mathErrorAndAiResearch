# armanAPI.py

class MathList(list):
    def appendNotNull(self, item):
        if item:
            self.append(item)

# preprocess equation
def preprocessEquation(equation):
    equation = equation.replace("\\div", "/")
    equation = equation.replace(" ", "")
    return equation

# splits numbers, parenthesis, operators
def mathSplitElements(stringEquation):
    # create result list and string element builder
    result = MathList()
    current = ''
    # preprocess the equation, removing excess space and converting for the right format
    equation = preprocessEquation(stringEquation)

    for i in range(len(equation)):
        char = equation[i]
        print(char)
        if(char in "([{"):
            if char == "(":
                #result.append(current) # idt this and other line are needed,
                result.append("(")
                #current = '' #  since parenthesis will typically be next to an operator
            elif char == "[":
                result.append("[")
            elif char == "{":
                result.append("{")
        elif(char in "])}"):
            if char == ")":
                result.appendNotNull(current)
                result.append(")")
                current = ''
            elif char == "]":
                result.appendNotNull(current)
                result.append("]")
                current = ''
            elif char == "}":
                result.appendNotNull(current)
                result.append("}")
                current = ''
        elif char == "+":
            result.appendNotNull(current)
            result.append("+")
            current = ''
        elif char == "-":
            result.appendNotNull(current)
            result.append("-")
            current = ''
        elif (char == "/"): # prob another one
            result.appendNotNull(current)
            result.append("/")
            current = ''
        elif char == "*": # prob x too
            result.appendNotNull(current)
            result.append("/")
            current = ''
        elif char == "^":
            result.appendNotNull(current)
            result.append("^")
            current = ''
        else:
            current += char
    result.appendNotNull(current)

    return result

def groupParenthesis(stringEquation):
    equation = mathSplitElements(stringEquation)
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