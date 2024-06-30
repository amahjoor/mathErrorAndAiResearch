from equationMethods import preprocessEquation, mathSplitElements, groupParenthesis

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
    
solvePemdas("2^{5}+[30 \\div 9]")
