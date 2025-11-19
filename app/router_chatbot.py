# app/router_chatbot.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot import conversational_response, generate_plan, safe_goal_check
import json
import re
from app.extract import extract_profile_data, profile_is_complete
from app.autonomous import conversar_autonomo


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


class Profile(BaseModel):
    name: str | None = None
    age: int | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    activity_level: str | None = None
    dietary_preferences: str | None = None
    allergies: str | None = None
    goal: str | None = None


@router.post("/gerar-plano")
def gerar_plano(profile: Profile):

    profile_dict = profile.dict()

    ok, msg = safe_goal_check(profile_dict)
    if not ok:
        return {
            "status": "erro",
            "mensagem": msg,
            "detalhe": "Recomendado consultar um profissional antes de prosseguir."
        }

    text = generate_plan(profile_dict)

    # tenta extrair JSON
    try:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            result_json = json.loads(m.group(0))
        else:
            result_json = {"raw": text}
    except Exception:
        result_json = {"raw": text}

    return {"status": "sucesso", "plano": result_json}


@router.post("/mensagem")
def conversar(msg: dict):
    user_text = msg.get("mensagem", "")
    profile = msg.get("profile", {})

    # Atualiza o profile com o que foi detectado na mensagem
    profile = extract_profile_data(user_text, profile)

    # Se o profile ainda não estiver completo → continuar conversa
    if not profile_is_complete(profile):
        resposta = conversational_response(profile, user_text)
        return {
            "status": "conversa",
            "mensagem": resposta,
            "profile_atualizado": profile
        }

    # Se estiver completo → gerar plano
    resposta_ai = generate_plan(profile)

    return {
        "status": "plano_pronto",
        "mensagem": "Seu plano está gerado!",
        "profile_final": profile,
        "plano": resposta_ai
    }


@router.post("/autonomo")
def chat_autonomo(payload: dict):
    mensagem = payload.get("mensagem", "")
    estado = payload.get("estado", {})

    resposta = conversar_autonomo(mensagem, estado)

    return resposta
