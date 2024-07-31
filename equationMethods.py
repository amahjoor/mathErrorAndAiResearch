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

# Preprocess the equation by removing excess space and converting symbols to the correct format.

def preprocessEquation(equation):
    print("Before preprocessing:")
    print(equation)
    equation = equation.replace("\[", "")
    equation = equation.replace("\]", "")
    equation = equation.replace("\\div", "/")
    equation = equation.replace("x", "*")
    equation = equation.replace("\\times", "*")
    equation = equation.replace(" ", "")
    equation = equation.replace("\\cdot", "*")
    equation = equation.replace(":", "=")
    equation = equation.replace("&", "")
    equation = equation.replace("\n", "")
    equation = equation.replace("\(", "")
    equation = equation.replace("\)", "")
    if("\hline" in equation):
        equation = equation.replace("\hline", "=")
        equation.replace("\\\\", "")
    else:
        equation = equation.replace("\\\\", "=")
    equation = equation.replace("\\", "")
    equation = equation.replace("end{array}", "")
    equation = equation.replace("end{aligned}", "")
    equation = equation.replace("==", "=")
    #equation = equation.replace("^", "**")
    equation = equation.replace("{", "(")
    equation = equation.replace("}", ")")
    equation = equation.replace("quad", "")

    print("After preprocessing: ")
    print(equation)

    result = {}
    
    # check for a description to the equation (problem description)
    if("begin{array}{l}" in equation and equation.split("begin{array}{l}")[0] != ""):    
        equation = equation.split("begin(array){l}")

        result["word_problem"] = equation[0]
        result["given_problem"] = equation[1][0]
        result["student_answer"] = equation[1][-1]

        work = []
        for i in range(len(equation[1]) - 1):
            if(equation[1][i+1] != None):
                work.append(equation[1][i]+"="+equation[1][i+1])
        result["work"] = work
    else:
        print(equation)
        equation = equation.replace("begin(array)(r)", "") # clean equation
        equation = equation.replace("begin(array)(l)", "")
        equation = equation.replace("begin(aligned)", "")
        equation = equation.split("=")
        
        print("equation after splitting: ")
        print(equation)

        result["given_problem"] = equation[0]
        result["student_answer"] = equation[-1]
        work = []
        for i in range(len(equation) - 1):
            if(equation[i+1] != None):
                work.append(equation[i]+"="+equation[i+1])
        result["work"] = work
    
    return result

def checkCorrect(equation):
    if(len(equation["work"]) > 1 or "=" in equation["work"][0]):        
        # if there is a variable x (or any var in general...), use simpy method
        if("x" in equation["given_problem"]):
            if(solve(equation["given_problem"]) == solve(equation["student_answer"])):
                return "Correct"
        else: # no variable, use eval
            temp_given = equation["given_problem"]
            if("^" in temp_given):
                temp_given = temp_given.replace("^", "**")

            temp_answer = equation["student_answer"]
            if("^" in temp_answer):
                temp_answer = temp_answer.replace("^", "**")
            print(temp_given)
            print(temp_answer)
            if(eval(temp_given) == eval(temp_answer)):
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
            {"role": "user", "content": f"{equation}\n\n if 'student_answer' = eval(given_problem), say 'CORRECT ^_^', otherwise return a python list with the following: \n[0] the specific step where this equation went wrong, without writing anything else aside from it.\n[1] which line does the error occur (just write the number, nothing else)\n[2] Explaination of how the student did it wrong\n[3] Explain the basic steps to do it correctly [4] Attempt the correct computation\n"}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )    
    answer = response.choices[0].message.content.strip() # clean the answer
    if(answer != "CORRECT ^_^"):
        try:
            import ast
            answer = ast.literal_eval(answer)
        except:
            return gptErrorCheck(equation)
    return answer

