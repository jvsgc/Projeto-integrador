from pymongo import MongoClient
import os

# Variável global para verificar se MongoDB está disponível
_mongodb_available = None
_mongodb_client = None

def is_mongodb_available():
    """Verifica se MongoDB está disponível"""
    global _mongodb_available, _mongodb_client
    
    if _mongodb_available is None:
        try:
            # Tenta conectar com timeout curto
            test_client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
            test_client.server_info()  # Força conexão
            _mongodb_client = test_client
            _mongodb_available = True
        except Exception:
            _mongodb_available = False
            _mongodb_client = None
    
    return _mongodb_available

def get_db():
    """Retorna conexão com banco ou None se não disponível"""
    if not is_mongodb_available():
        return None
    
    if _mongodb_client is None:
        try:
            _mongodb_client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        except Exception:
            return None
    
    try:
        return _mongodb_client["healthtrack"]
    except Exception:
        return None
