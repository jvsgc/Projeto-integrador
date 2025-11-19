from app.extract import extract_profile_data, profile_is_complete
from app.chatbot import generate_plan


def conversar_autonomo(mensagem: str, estado: dict):
    """
    estado contém:
    - profile (dados coletados)
    - etapa (opcional)
    """

    profile = estado.get("profile", {})

    # Extrair informações da mensagem
    profile = extract_profile_data(mensagem, profile)

    # Atualiza estado
    novo_estado = {"profile": profile}

    # Se ainda falta dados
    if not profile_is_complete(profile):
        faltando = []

        if not profile.get("age"):
            faltando.append("sua idade")
        if not profile.get("height_cm"):
            faltando.append("sua altura em cm")
        if not profile.get("weight_kg"):
            faltando.append("seu peso em kg")
        if not profile.get("activity_level"):
            faltando.append(
                "seu nível de atividade (sedentário, leve, moderado ou intenso)")
        if not profile.get("goal"):
            faltando.append("seu objetivo (perder, ganhar ou manter)")

        texto = ", ".join(faltando)
        resposta = f"Obrigado! Agora me informe: {texto}."
        return {
            "status": "coletando",
            "resposta": resposta,
            "estado": novo_estado
        }

    # Quando estiver completo → gerar plano automaticamente
    plano = generate_plan(profile)

    return {
        "status": "plano_gerado",
        "resposta": "Prontinho! Preparei um plano completo baseado nas suas informações.",
        "plano": plano,
        "estado": novo_estado
    }
