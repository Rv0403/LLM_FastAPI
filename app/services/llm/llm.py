import os
from dotenv import load_dotenv
from openai import OpenAI
from app.schemas.chat_evaluation_schemas import Query, Evaluation

load_dotenv(override=True)
openai = OpenAI()

gemini = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Initialize OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def openai_chat(chat_prompt: str, query: Query):
    messages = [{"role": "system", "content": chat_prompt}, {"role": "user", "content": query.question}]
    response = openai_client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    chat_answer = response.choices[0].message.content  
    return chat_answer


def gemini_evaluator(evaluator_prompt: str, evaluator_user_prompt: str):
    messages = [{"role": "system", "content": evaluator_prompt}, {"role": "user", "content": evaluator_user_prompt}]
    response = gemini.beta.chat.completions.parse(model="gemini-2.0-flash", messages=messages, response_format=Evaluation)
    evaluation_answer = response.choices[0].message.parsed
    return evaluation_answer