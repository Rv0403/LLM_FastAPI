from fastapi import FastAPI
from api.v1.endpoints import chat

app=FastAPI()

app.include_router(chat.router)