from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.utils.file_handler import summary_text, linkdin_text
from app.services.prompt.chat_prompt import chat_system_prompt
from app.services.prompt.evaluation_prompt import (
    evaluator_system_prompt,
    evaluator_user_prompt,
)
from app.services.llm.llm import openai_chat, gemini_evaluator

router = APIRouter(
    prefix='/userchat',
    tags=['userchat']
)


@router.post("/chat")
async def chat(
    question: str = Form(...),
    name: str = Form(...),
    linkedin_file: UploadFile = File(...),
    summary_file: UploadFile = File(...)
):
    try:
        linkedin_bytes = await linkedin_file.read()
        summary_bytes = await summary_file.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Unable to read uploaded files: {exc}")

    try:
        summary = summary_text(summary_bytes, summary_file.filename)
        linkedin = linkdin_text(linkedin_bytes, linkedin_file.filename)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    

    chat_prompt = chat_system_prompt(name, linkedin, summary)
    response = openai_chat(chat_prompt, question)

    evaluator_prompt = evaluator_system_prompt(name, linkedin, summary)
    history = ""
    evaluator_user_prompt_text = evaluator_user_prompt(response, question, history)
    evaluated_answer = gemini_evaluator(evaluator_prompt, evaluator_user_prompt_text)

    return {
        "Question": question,
        "answer_of_question": response,
        "evaluate_answer": evaluated_answer
    }