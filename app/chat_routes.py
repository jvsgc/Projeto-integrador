from fastapi import APIRouter
from pydantic import BaseModel

from app.chat_repository import create_conversation, save_message, get_history
from app.chatbot import gerar_resposta



router = APIRouter(prefix="/chat", tags=["Chatbot"])

class MessageRequest(BaseModel):
    user_id: str
    message: str
    conversation_id: str | None = None

@router.post("/send")
async def send_message(data: MessageRequest):
    # Se não passou conversation_id, cria nova
    if data.conversation_id is None:
        conversation_id = create_conversation(data.user_id)
    else:
        conversation_id = data.conversation_id

    # Salva mensagem do usuário
    save_message(conversation_id, "user", data.message)

    # Gera resposta
    bot_reply = gerar_resposta(data.message)

    # Salva resposta do bot
    save_message(conversation_id, "bot", bot_reply)

    # Retorna resposta
    return {
        "conversation_id": conversation_id,
        "reply": bot_reply,
        "history": get_history(conversation_id)
    }
