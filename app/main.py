from fastapi import FastAPI
from app.api.v1.endpoints import chat

app=FastAPI()

app.include_router(chat.router)