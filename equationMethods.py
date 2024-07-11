"""
This module provides functionality for parsing and processing mathematical equations.
It includes methods for preprocessing equations, splitting them into components, 
grouping parenthesis, handling power operations, and grouping multiplication/division operations.
"""

class MathList(list):
    # helper method to append non-null items to the list.
    def appendNotNull(self, item): 
        if item:
            self.append(item)

# preprocess the equation, removing excess space and converting for the right format
# Preprocess the equation by removing excess space and converting symbols to the correct format.
# Replaces \div with / and \times with *.


# 'text': 'Solve for \\( x \\).\n\\[\n\\begin{array}{l}\n2 x-4 \\cdot 2=9 \\\\\n2 x-8=9 \\\\\n2 x=17 \\\\\nx=8\n\\end{array}\n\\]
# 'text': '\\( \\begin{array}{l}2 x-4 \\cdot 2=9 \\\\ 2 x-8=9 \\\\ 2 x=17 \\\\ x=8\\end{array} \\)

def preprocessEquation(equation):
    #print(equation)
    equation = equation.replace("\\div", "/")
    equation = equation.replace("\\times", "*")
    equation = equation.replace(" ", "")
    equation = equation.replace("\\cdot", "*")
    equation = equation.replace(":", "=")
    equation = equation.replace("\n", "")

    equation = equation.split("\\begin{array}{l}")
    equation[1] = equation[1].replace("\\end{array}", "")

    result = {}
    equation[1] = equation[1].split("\\\\") # split each new line
    
    result["given_problem"] = equation[0]
    result["equation"] = equation[1]
    return result

def checkCorrect(equation):
    if(len(equation) > 1):
        if(eval(equation[0]) == equation[-1]):
            return "Correct"
        else:
            return gptErrorCheck(equation)
        
from config import OPENAI_API_KEY

import openai
from openai import OpenAI

openai.api_key = OPENAI_API_KEY

def gptErrorCheck(equation):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "user", "content": f"{equation}\n\nreturn a list with the following: \n1) the specific step where this equation went wrong, without writing anything else aside from it.\n2) which line does the error occur (just write the number, nothing else)\n3) how to rectify the error\n"}],
        max_tokens=150,  # Adjust the number of tokens as needed
        n=1,
        stop=None,
        temperature=0.7  # Adjust the temperature for more or less creative responses
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

