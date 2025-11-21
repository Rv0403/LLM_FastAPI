from fastapi import APIRouter
from app.utils.file_handler import summary_text, linkdin_text
from app.services.prompt.chat_prompt import chat_system_prompt
from app.services.prompt.evaluation_prompt import evaluator_system_prompt, evaluator_user_prompt
from app.services.llm.llm import openai_chat, gemini_evaluator
from app.schemas.chat_evaluation_schemas import Query

router = APIRouter(
    prefix='/userchat',
    tags=['userchat']
)


@router.post("/chat")
def chat(query: Query):
    # Extract file paths and data from query
    file1_path = query.file1
    file2_path = query.file2
    question = query.question
    name = query.name
    
    # Read files
    summary = summary_text(file2_path)
    linkedin = linkdin_text(file1_path)
    
    # Create chat prompt
    chat_prompt = chat_system_prompt(name, linkedin, summary)
    
    # Get chat response
    response = openai_chat(chat_prompt, query)
    
    # Create evaluator prompts (defined before use)
    evaluator_prompt = evaluator_system_prompt(name, linkedin, summary)
    # For history, we'll use an empty string as there's no conversation history yet
    history = ""
    evaluator_user_prompt_text = evaluator_user_prompt(response, question, history)
    
    # Evaluate the answer (correct parameter order: evaluator_prompt, evaluator_user_prompt)
    evaluated_answer = gemini_evaluator(evaluator_prompt, evaluator_user_prompt_text)
    
    return {
        "Question": question,
        "answer_of_question": response,
        "evaluate_answer": evaluated_answer
    }