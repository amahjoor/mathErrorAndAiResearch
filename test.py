from equationMethods import preprocessEquation, mathSplitElements, groupParenthesis, groupPower, groupMultDiv#, identifyAndDo

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

    equation = groupMultDiv(equation)
    print("Power grouped together: ", end ="")
    #print("Identified and computed first expression, result: ", end="")
    print(equation)
#solvePemdas("2^{5}+[30 \\div 9]")
#solvePemdas("2^{5}+[30 \\div 9] * 4")
#print(preprocessEquation("\\begin{array}{l}\n(3+5)^{2}=3^{2}+5^{2}=9+25=34 \\\\\n(3+3) \\times 4^{2}=3+3 \\times 16=3+48=51 \\\\\n(3+3) \\times 4^{2}=(3+3) \\times 16=6 \\times 16=84 \\\\\n(3+3)"))
#solvePemdas("3 + 2 * 4^2")

from config import OPENAI_API_KEY

import openai
from openai import OpenAI

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_gpt_answer(prompt):
    client = OpenAI(
        api_key=OPENAI_API_KEY
    )

    response = client.chat.completions.create(
        model='gpt-4',
        messages=[
            {"role": "user", "content": f"{prompt}\n\nshow me the specific step where this equation went wrong, without writing anything else aside from it, converting it out of latex to normal work."}],
        max_tokens=150,  # Adjust the number of tokens as needed
        n=1,
        stop=None,
        temperature=0.7  # Adjust the temperature for more or less creative responses
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

# Example usage
prompt = "(3+3) \\times 4^{2}=3+3 \\times 16=3+48=51"
#prompt = "(3+3)*4^{2}=51"
answer = get_gpt_answer(prompt)
print(answer)








#prompt = "5 / 2 + 500 * 24 = 2 + 500 * 2.4 = 2 + 1200 = 1202"