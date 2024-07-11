"""
This module provides functionality for parsing and processing mathematical equations.
It includes methods for preprocessing equations, splitting them into components, 
grouping parenthesis, handling power operations, and grouping multiplication/division operations.
"""
from sympy import solve

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
    print(equation)
    equation = equation.replace("\[", "")
    equation = equation.replace("\]", "")
    equation = equation.replace("\\div", "/")
    equation = equation.replace("\\times", "*")
    equation = equation.replace(" ", "")
    equation = equation.replace("\\cdot", "*")
    equation = equation.replace(":", "=")
    equation = equation.replace("\n", "")
    equation = equation.replace("\(", "")
    equation = equation.replace("\)", "")
    equation = equation.replace("\hline", "=")
    #equation = equation.replace("\\", "")
    equation = equation.replace("end{array}", "")

    result = {}
    
    # if there is a description to the equation.
    if("begin{array}{l}" in equation):
        equation = equation.split("begin{array}{l}")    
        #equation[1] = equation[1].split("\\\\") # split each new line
        equation[1] = equation[1].split("\\\\") # split each new line

        result["word_problem"] = equation[0]
        result["given_problem"] = equation[1][0]
        result["student_answer"] = equation[1][-1]

        work = []
        for i in range(len(equation[1]) - 1):
            if(equation[1][i+1] != None):
                work.append(equation[1][i]+"="+equation[1][i+1])
        result["work"] = work
    else:
        equation = equation.replace("begin{array}{r}", "") # clean equation
        
        equation = equation.split("=")
        result["given_problem"] = equation[0]
        result["student_answer"] = equation[-1]
        work = []
        for i in range(len(equation) - 1):
            if(equation[i+1] != None):
                work.append(equation[i]+"="+equation[i+1])
        result["work"] = work
    return result

def checkCorrect(equation):
    if(len(equation["work"]) > 1):
        #print(equation["given_problem"])
        
        # if there is a variable x (or any var in general...), use simpy method
        if("x" in equation["given_problem"]):
            if(solve(equation["given_problem"]) == solve(equation["student_answer"])):
                return "Correct"
        else: # no variable, use eval
            if(eval(equation["given_problem"]) == eval(equation["student_answer"])):
                return "Correct"
        return gptErrorCheck(equation)
    else:
        return "Seems like this is only the given problem (or there's something wrong on my end)."
# import stuff for OpenAI        
from config import OPENAI_API_KEY
import openai
from openai import OpenAI

openai.api_key = OPENAI_API_KEY

def gptErrorCheck(equation):
    # set up client
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )
    # set up and prompt gpt response
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "user", "content": f"{equation}\n\n if 'student_answer' = eval(given_problem), say CORRECT ^_^, otherwise return a list with the following: \n1) the specific step where this equation went wrong, without writing anything else aside from it.\n2) which line does the error occur (just write the number, nothing else)\n3) how to rectify the error.\n"}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )    
    answer = response.choices[0].message.content.strip() # clean the answer
    return answer

