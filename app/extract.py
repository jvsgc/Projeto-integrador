import re


def extract_profile_data(message: str, current: dict):
    text = message.lower()
    profile = current.copy()

    # Idade
    match = re.search(r"(\d+)\s*anos", text)
    if match:
        profile["age"] = int(match.group(1))

    # Peso (kg)
    match = re.search(r"(\d+)\s*kg", text)
    if match:
        profile["weight_kg"] = int(match.group(1))

    # Altura (cm)
    match = re.search(r"(\d+)\s*cm", text)
    if match:
        profile["height_cm"] = int(match.group(1))

    # Objetivo
    if any(w in text for w in ["perder", "emagrecer"]):
        profile["goal"] = message
    if any(w in text for w in ["ganhar", "massa", "engordar"]):
        profile["goal"] = message
    if "manter" in text:
        profile["goal"] = message

    # Nível de atividade
    if "sedent" in text:
        profile["activity_level"] = "sedentário"
    if "leve" in text:
        profile["activity_level"] = "leve"
    if "moderado" in text:
        profile["activity_level"] = "moderado"
    if "intenso" in text:
        profile["activity_level"] = "intenso"

    return profile


def profile_is_complete(profile: dict):
    required = ["age", "height_cm", "weight_kg", "goal", "activity_level"]
    return all(profile.get(r) for r in required)
