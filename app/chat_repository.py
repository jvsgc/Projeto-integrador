import uuid
from datetime import datetime
from app.database import get_db, is_mongodb_available



# -------------------------------------------------------
# Criar conversa
# -------------------------------------------------------
def create_conversation(user_id):
    if not is_mongodb_available():
        # Retorna ID mesmo sem salvar se MongoDB não estiver disponível
        return str(uuid.uuid4())
    
    db = get_db()
    if db is None:
        return str(uuid.uuid4())
    
    try:
        conversation_id = str(uuid.uuid4())
        db.conversations.insert_one({
            "_id": conversation_id,
            "user_id": user_id,
            "messages": [],
            "started_at": datetime.utcnow()
        })
        return conversation_id
    except Exception:
        # Se falhar, retorna ID mesmo assim
        return str(uuid.uuid4())


# -------------------------------------------------------
# Salvar mensagens
# -------------------------------------------------------
def save_message(conversation_id, sender, content):
    if not is_mongodb_available():
        return  # Silenciosamente ignora se MongoDB não estiver disponível
    
    db = get_db()
    if db is None:
        return
    
    try:
        db.conversations.update_one(
            {"_id": conversation_id},
            {"$push": {
                "messages": {
                    "sender": sender,
                    "content": content,
                    "timestamp": datetime.utcnow()
                }
            }}
        )
    except Exception:
        pass  # Silenciosamente ignora erros


# -------------------------------------------------------
# Buscar histórico
# -------------------------------------------------------
def get_history(conversation_id):
    db = get_db()

    conv = db.conversations.find_one({"_id": conversation_id})

    if not conv:
        return []

    return conv["messages"]
