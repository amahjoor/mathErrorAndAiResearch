# armanAPI.py

class MathList(list):
    def appendNotNull(self, item): # helper method to append non-null items
        if item:
            self.append(item)

# preprocess the equation, removing excess space and converting for the right format
def preprocessEquation(equation):
    equation = equation.replace("\\div", "/")
    equation = equation.replace("\\times", "*")
    equation = equation.replace(" ", "")
    return equation

# splits numbers, parenthesis, operators into a list
def mathSplitElements(equation):
    # create result list and string element builder
    result = MathList()
    current = ''

    operators = {'+', '-', '*', '/', '^'}
    opening_parenthesis = {'(', '[', '{'}
    closing_parenthesis = {')', ']', '}'}

    for char in equation:
        if char in opening_parenthesis or char in closing_parenthesis or char in operators:
            result.appendNotNull(current)
            result.append(char)
            current = ''
        else:
            current += char

    result.appendNotNull(current)

    return result

# method to group parenthesis within list
def groupParenthesis(equation):
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
    
# method to group a power operation within the list
def groupPower(equation):
    i = 0
    result = MathList()

    while i < len(equation):
        if(equation[i] == "^"):
            if(i > 0 and i < len(equation) - 1): # if the "^" is not the very last character or the very first character
                result.pop() # removes last item
                result.append([equation[i - 1], equation[i], equation[i+1]])
                i+=2
        else:
            result.append(equation[i])
            i+=1
    return result

# method to group multiplication and division operations
def groupMultDiv(equation):
    i = 0
    result = MathList()

    while i < len(equation):
        if(equation[i] == "*" or equation[i] == "/"):
            if i > 0 and i < len(equation) - 1:
                result.pop()
                result.append([equation[i - 1], equation[i], equation[i+1]])
                i+=2
        else:
            result.append(equation[i])
            i+=1
    return result
# POT. APPROACHES
# 1: digging through and finding the highest priority operation, do that, repeat
# 2: build a stack with lowest priority operations at bottom, highest at top
#    for example 2 + 3 * 4 ^ 2 -> [2 + [3 * [4 ^ 2]]]
#                                   top: 4 ^ 2
#                                   then: 3 * abv
#                                   then @ bot: 2 + abv
#    or lets say 2 * 3 ^ 2 + 2 + 3 * 4 ^ 2 -> [2 * [3 ^ 2]] + [2] + [3 * [4 ^ 2]
#                      pot build 3 stacks:     1 here,      1 here,    1 here.             



# BELOW: Scratched approaches for identifying what operation to do on equation.
# - I think it's more effective to group equation into lists,
#   and to use the nested lists to identify the order of operations. 

'''
# identify highest priority operation, and computes it
def identifyAndDo(equation):
    operators = {'+', '-', '*', '/', '^'}

    while(len(equation) > 1): # keep on identifying and doing until only 1 number
        
        for i in range(len(equation)):
            if len(equation[i]) > 1:
                equation[i].replace(equation[i], identifyAndDo(equation[i]))
                print(equation)
            if equation[i] in operators and len(equation) >= 2 and i > 0:
                if(equation[i] == "^"):
                    temp = [equation[i - 1], equation[i], equation[i+1]]
                    temp = "".join(temp).replace("^", "**")
                    print(temp)
                    result = eval(temp)
                    print(result)
                    return
                
                
        return 
'''
# identify lowest priority operation and add to bottom of stack
#def createStack(equation):
    # check if there's + and -
    #   store indexes of values operated by plus and minus

# keep on identify and doing until only one number 
