import uuid
from datetime import datetime
from app.database import get_db



# -------------------------------------------------------
# Criar conversa
# -------------------------------------------------------
def create_conversation(user_id):
    db = get_db()
    conversation_id = str(uuid.uuid4())

    db.conversations.insert_one({
        "_id": conversation_id,
        "user_id": user_id,
        "messages": [],
        "started_at": datetime.utcnow()
    })

    return conversation_id


# -------------------------------------------------------
# Salvar mensagens
# -------------------------------------------------------
def save_message(conversation_id, sender, content):
    db = get_db()

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


# -------------------------------------------------------
# Buscar histórico
# -------------------------------------------------------
def get_history(conversation_id):
    db = get_db()

    conv = db.conversations.find_one({"_id": conversation_id})

    if not conv:
        return []

    return conv["messages"]
