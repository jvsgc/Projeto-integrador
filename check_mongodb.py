#!/usr/bin/env python3
"""
Script rápido para verificar se MongoDB está rodando
"""

from app.database import is_mongodb_available, get_db

def check_mongodb():
    print("=" * 60)
    print("VERIFICAÇÃO DO MONGODB")
    print("=" * 60)
    
    print("\n🔍 Verificando conexão...")
    
    if is_mongodb_available():
        print("✅ MongoDB está RODANDO e acessível!")
        
        try:
            db = get_db()
            if db:
                # Testa algumas operações básicas
                collections = db.list_collection_names()
                print(f"\n📊 Database: {db.name}")
                print(f"📁 Collections encontradas: {len(collections)}")
                
                if collections:
                    print("   - " + "\n   - ".join(collections))
                
                # Conta documentos na collection conversations
                if "conversations" in collections:
                    total = db.conversations.count_documents({})
                    print(f"\n💬 Total de conversas salvas: {total}")
                
                print("\n✅ Tudo funcionando perfeitamente!")
            else:
                print("⚠️ Conexão estabelecida mas get_db() retornou None")
        except Exception as e:
            print(f"⚠️ Erro ao acessar banco: {e}")
    else:
        print("❌ MongoDB NÃO está rodando ou não está acessível!")
        print("\n📝 Para iniciar o MongoDB:")
        print("   1. Windows: Abra o MongoDB Compass ou inicie o serviço")
        print("   2. Ou execute: mongod (no terminal)")
        print("   3. Verifique se está na porta padrão: localhost:27017")
        print("\n💡 O chatbot funcionará normalmente mesmo sem MongoDB,")
        print("   mas as conversas não serão salvas.")

if __name__ == "__main__":
    check_mongodb()

