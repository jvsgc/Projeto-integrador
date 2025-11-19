# app/main.py
from fastapi import FastAPI
from app.router_chatbot import router as chatbot_router

app = FastAPI(
    title="API Projeto Integrador",
    version="1.0.0"
)

# inclui rotas
app.include_router(chatbot_router)


@app.get("/")
def home():
    return {"status": "online", "mensagem": "API funcionando!"}
