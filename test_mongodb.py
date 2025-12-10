#!/usr/bin/env python3
"""
Script de teste para verificar se as conversas estão sendo salvas no MongoDB
"""

from app.database import get_db
from app.chat_repository import create_conversation, save_message, get_history
from datetime import datetime

def test_mongodb():
    print("=" * 60)
    print("TESTE DE CONEXÃO COM MONGODB")
    print("=" * 60)
    
    try:
        # Testa conexão
        db = get_db()
        print("✓ Conexão com MongoDB estabelecida!")
        print(f"  Database: {db.name}")
        
        # Conta conversas existentes
        total = db.conversations.count_documents({})
        print(f"✓ Total de conversas no banco: {total}")
        
        # Lista últimas 5 conversas
        print("\n" + "-" * 60)
        print("ÚLTIMAS 5 CONVERSAS:")
        print("-" * 60)
        
        conversations = list(db.conversations.find({}).sort("started_at", -1).limit(5))
        
        if not conversations:
            print("  Nenhuma conversa encontrada ainda.")
        else:
            for i, conv in enumerate(conversations, 1):
                print(f"\n{i}. Conversa ID: {conv['_id']}")
                print(f"   User ID: {conv.get('user_id', 'N/A')}")
                print(f"   Iniciada em: {conv.get('started_at', 'N/A')}")
                messages = conv.get('messages', [])
                print(f"   Total de mensagens: {len(messages)}")
                
                if messages:
                    print("   Últimas mensagens:")
                    for msg in messages[-3:]:  # Mostra últimas 3
                        sender = msg.get('sender', 'unknown')
                        content = msg.get('content', '')[:50]  # Primeiros 50 chars
                        print(f"     [{sender}]: {content}...")
        
        # Testa criação de conversa de teste
        print("\n" + "-" * 60)
        print("TESTE DE CRIAÇÃO DE CONVERSA:")
        print("-" * 60)
        
        test_user_id = "test_user_" + str(int(datetime.now().timestamp()))
        conv_id = create_conversation(test_user_id)
        print(f"✓ Conversa de teste criada: {conv_id}")
        
        # Salva mensagens de teste
        save_message(conv_id, "user", "Olá, esta é uma mensagem de teste!")
        save_message(conv_id, "assistant", "Olá! Como posso ajudar?")
        save_message(conv_id, "user", "Quero testar o MongoDB")
        save_message(conv_id, "assistant", "Perfeito! O MongoDB está funcionando corretamente.")
        
        print("✓ 4 mensagens de teste salvas")
        
        # Busca histórico
        history = get_history(conv_id)
        print(f"✓ Histórico recuperado: {len(history)} mensagens")
        
        print("\n" + "-" * 60)
        print("HISTÓRICO DA CONVERSA DE TESTE:")
        print("-" * 60)
        for msg in history:
            print(f"  [{msg.get('sender', 'unknown')}]: {msg.get('content', '')}")
        
        print("\n" + "=" * 60)
        print("✓ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nVerifique se:")
        print("  1. MongoDB está rodando (mongod)")
        print("  2. A conexão está correta em app/database.py")
        print("  3. O banco 'healthtrack' existe")
        return False
    
    return True

if __name__ == "__main__":
    test_mongodb()

