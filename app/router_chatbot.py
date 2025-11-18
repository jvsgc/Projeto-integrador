# app/router_chatbot.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.chatbot import generate_plan, safe_goal_check
import json
import re

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
