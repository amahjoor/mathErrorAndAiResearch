from armanAPI import mathSplitElements, groupParenthesis

def solvePemdas(result):
    equation = result
    equation = groupParenthesis(equation)
    
    print(equation)
solvePemdas("2^{5}+[30 \\div 9]")
