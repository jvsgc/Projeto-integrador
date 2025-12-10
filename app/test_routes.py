from fastapi import APIRouter
from app.chat_repository import get_history
from app.database import get_db, is_mongodb_available

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/mongodb/status")
def mongodb_status():
    """Verifica se MongoDB está rodando e acessível"""
    available = is_mongodb_available()
    
    if not available:
        return {
            "status": "offline",
            "message": "MongoDB não está rodando ou não está acessível",
            "port": "27017",
            "host": "localhost"
        }
    
    try:
        db = get_db()
        if db:
            collections = db.list_collection_names()
            total_conversations = 0
            if "conversations" in collections:
                total_conversations = db.conversations.count_documents({})
            
            return {
                "status": "online",
                "message": "MongoDB está rodando e acessível",
                "database": db.name,
                "collections": collections,
                "total_conversations": total_conversations,
                "port": "27017",
                "host": "localhost"
            }
        else:
            return {
                "status": "error",
                "message": "Conexão estabelecida mas get_db() retornou None"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro ao acessar MongoDB: {str(e)}"
        }


@router.get("/conversations")
def list_conversations():
    """Lista todas as conversas salvas no banco"""
    if not is_mongodb_available():
        return {"error": "MongoDB não está disponível", "conversations": []}
    
    db = get_db()
    if db is None:
        return {"error": "Não foi possível conectar ao banco", "conversations": []}
    
    conversations = list(db.conversations.find({}).sort("started_at", -1).limit(50))
    
    # Converte ObjectId para string
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
        if "started_at" in conv:
            conv["started_at"] = conv["started_at"].isoformat()
        if "messages" in conv:
            for msg in conv["messages"]:
                if "timestamp" in msg:
                    msg["timestamp"] = msg["timestamp"].isoformat()
    
    return {
        "total": len(conversations),
        "conversations": conversations
    }


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    """Busca uma conversa específica pelo ID"""
    if not is_mongodb_available():
        return {"error": "MongoDB não está disponível"}
    
    db = get_db()
    if db is None:
        return {"error": "Não foi possível conectar ao banco"}
    
    conversation = db.conversations.find_one({"_id": conversation_id})
    
    if not conversation:
        return {"error": "Conversa não encontrada"}
    
    # Converte ObjectId e timestamps
    conversation["_id"] = str(conversation["_id"])
    if "started_at" in conversation:
        conversation["started_at"] = conversation["started_at"].isoformat()
    if "messages" in conversation:
        for msg in conversation["messages"]:
            if "timestamp" in msg:
                msg["timestamp"] = msg["timestamp"].isoformat()
    
    return conversation


@router.get("/conversations/user/{user_id}")
def get_user_conversations(user_id: str):
    """Busca todas as conversas de um usuário"""
    if not is_mongodb_available():
        return {"error": "MongoDB não está disponível", "conversations": []}
    
    db = get_db()
    if db is None:
        return {"error": "Não foi possível conectar ao banco", "conversations": []}
    
    conversations = list(db.conversations.find({"user_id": user_id}).sort("started_at", -1))
    
    # Converte ObjectId para string
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
        if "started_at" in conv:
            conv["started_at"] = conv["started_at"].isoformat()
        if "messages" in conv:
            for msg in conv["messages"]:
                if "timestamp" in msg:
                    msg["timestamp"] = msg["timestamp"].isoformat()
    
    return {
        "user_id": user_id,
        "total": len(conversations),
        "conversations": conversations
    }


@router.get("/stats")
def get_stats():
    """Estatísticas gerais do banco de dados"""
    if not is_mongodb_available():
        return {
            "error": "MongoDB não está disponível",
            "total_conversations": 0,
            "total_messages": 0
        }
    
    db = get_db()
    if db is None:
        return {
            "error": "Não foi possível conectar ao banco",
            "total_conversations": 0,
            "total_messages": 0
        }
    
    total_conversations = db.conversations.count_documents({})
    total_messages = db.conversations.aggregate([
        {"$project": {"message_count": {"$size": {"$ifNull": ["$messages", []]}}}},
        {"$group": {"_id": None, "total": {"$sum": "$message_count"}}}
    ])
    
    total_messages_count = 0
    try:
        result = list(total_messages)
        if result:
            total_messages_count = result[0].get("total", 0)
    except:
        pass
    
    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages_count,
        "database": "healthtrack",
        "collection": "conversations"
    }

