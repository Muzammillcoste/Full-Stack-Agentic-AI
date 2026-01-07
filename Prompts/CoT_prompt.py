import json
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Chain of Thought Prompt
SYSTEM_PROMPT = """You are a helpful assistant in resolving user queries using chain of thoughts.
You work in START, PLAN and OUTPUT step.
You need to first PLAN what need to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, fianlly you can give an OUTPUT.

RULES:
 - Strickly follow the given JSON output Format
 - Only run one step at a time.
 - The sequence of steps is START (where user give the input), PLAN (That can be multiple steps)
 and finally OUTPUT (which going to display to user)

JSON OUTPUT FORMAT:
 {"step":START | PLAN | OUTPUT, "content":"string"}

 EXAMPLES:

    Example 1:

    START: Hey, can you solve 2+3*5/10
    PLAN: {"step":"PLAN","content":"The user is asking to solve a mathematical expression."}
    PLAN: {"step":"PLAN","content":"Identify the correct order of operations to evaluate the expression."}
    PLAN: {"step":"PLAN","content":"Apply the BODMAS rule to determine the correct calculation sequence."}
    PLAN: {"step":"PLAN","content":"Compute multiplication and division before addition."}

    OUTPUT: {"step":"OUTPUT","content":"Using BODMAS, first compute 3*5 = 15, then 15÷10 = 1.5, and finally add 2. The final answer is 3.5."}
    
    Example 2:

    START: Explain imaginary numbers
    PLAN: {"step":"PLAN","content":"The user wants an explanation of imaginary numbers."}
    PLAN: {"step":"PLAN","content":"Recall the definition of imaginary numbers in mathematics."}
    PLAN: {"step":"PLAN","content":"Explain the imaginary unit and its defining property."}
    PLAN: {"step":"PLAN","content":"Prepare a simple example to make the explanation clearer."}
    OUTPUT: {"step":"OUTPUT","content":"Imaginary numbers involve the imaginary unit i, where i² = -1. They are used to represent solutions to equations that have no real-number solutions, such as √-1, which is written as i."}
"""

message_history= [
    {   "role": "system","content": SYSTEM_PROMPT},
]

user_query=input('How can I help you:   ')
message_history.append({"role":"user","content":user_query})

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=json.loads(raw_result)

    if parsed_result.get("step")=="START":
        print("--",parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="PLAN":
        print('--',parsed_result.get("content"))
        continue
    if parsed_result.get("step")=="OUTPUT":
        print('--',parsed_result.get("content"))
        break

