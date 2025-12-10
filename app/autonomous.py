from app.extract import extract_profile_data, profile_is_complete
from app.chatbot import generate_plan, gerar_resposta_humanizada, responder_pergunta_geral


def conversar_autonomo(mensagem: str, estado: dict):
    """
    estado contém:
    - profile (dados coletados)
    - etapa (opcional)
    """

    profile = estado.get("profile", {})

    # Verifica se é uma pergunta geral sobre o chatbot (antes de processar profile)
    resposta_geral = responder_pergunta_geral(mensagem)
    if resposta_geral:
        return {
            "status": "conversa",
            "resposta": resposta_geral,
            "estado": {"profile": profile}  # Mantém o profile atual
        }

    # Extrair informações da mensagem
    profile_anterior = profile.copy()
    profile = extract_profile_data(mensagem, profile)

    # Atualiza estado
    novo_estado = {"profile": profile}

    # Se ainda falta dados
    if not profile_is_complete(profile):
        # Verifica o que foi coletado nesta mensagem
        dados_coletados = []
        if not profile_anterior.get("name") and profile.get("name"):
            dados_coletados.append("nome")
        if not profile_anterior.get("age") and profile.get("age"):
            dados_coletados.append("idade")
        if not profile_anterior.get("height_cm") and profile.get("height_cm"):
            dados_coletados.append("altura")
        if not profile_anterior.get("weight_kg") and profile.get("weight_kg"):
            dados_coletados.append("peso")
        if not profile_anterior.get("activity_level") and profile.get("activity_level"):
            dados_coletados.append("nível de atividade")
        if not profile_anterior.get("goal") and profile.get("goal"):
            dados_coletados.append("objetivo")

        # Gera resposta humanizada usando IA
        resposta = gerar_resposta_humanizada(mensagem, profile, dados_coletados)
        
        return {
            "status": "coletando",
            "resposta": resposta,
            "estado": novo_estado
        }

    # Quando estiver completo → gerar plano automaticamente
    plano = generate_plan(profile)

    return {
        "status": "plano_gerado",
        "resposta": "🎉 Perfeito! Agora que tenho todas as informações, vou criar um plano personalizado para você. Isso pode levar alguns segundos... ⏳",
        "plano": plano,
        "estado": novo_estado
    }
