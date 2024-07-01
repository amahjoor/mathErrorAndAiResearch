from equationMethods import preprocessEquation, mathSplitElements, groupParenthesis, groupPower#, identifyAndDo

def solvePemdas(result):
    # Input
    equation = result
    print("Input string: " + equation)
    
    # Preprocessing
    equation = preprocessEquation(equation)
    print("Preprocessed: " + equation)

    # Split Elements
    equation = mathSplitElements(equation)
    print("Elements split: ", end="")
    print(equation)

    # Parenthesis Grouping
    equation = groupParenthesis(equation)
    print("Parenthesis grouped together: ", end="")
    print(equation)

    equation = groupPower(equation)
    print("Power grouped together: ", end ="")
    #print("Identified and computed first expression, result: ", end="")
    print(equation)    
solvePemdas("2^{5}+[30 \\div 9]")
solvePemdas("2^{5}+[30 \\div 9] * 4")
#solvePemdas("3 + 2 * 4^2")