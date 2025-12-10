import re


def extract_profile_data(message: str, current: dict):
    text = message.lower()
    profile = current.copy()

    # Nome - sempre primeiro
    if not profile.get("name"):
        # "meu nome é", "eu sou", "me chamo", "sou o", "sou a"
        match = re.search(r"(?:meu\s+nome\s+é|eu\s+sou|me\s+chamo|sou\s+o|sou\s+a)\s+([a-záàâãéêíóôõúç\s]+)", text)
        if match:
            name = match.group(1).strip()
            if len(name) > 1 and len(name) < 50:
                profile["name"] = name.title()
        # Também tenta se começar direto com nome próprio
        elif re.match(r"^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+(?:\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ][a-záàâãéêíóôõúç]+)?$", message.strip()):
            if len(message.strip().split()) <= 3:  # Máximo 3 palavras
                profile["name"] = message.strip().title()

    # Idade - múltiplos padrões
    if not profile.get("age"):
        # "tenho 19 anos", "19 anos", "idade 19", "tenho 19"
        match = re.search(r"(?:tenho|idade|tenho\s+)?(\d{1,3})\s*anos?", text)
        if match:
            age = int(match.group(1))
            if 13 <= age <= 120:  # Validação básica
                profile["age"] = age

    # Peso (kg) - múltiplos padrões
    if not profile.get("weight_kg"):
        # "peso 62kg", "62kg", "62 kg", "peso 62"
        match = re.search(r"(?:peso|peso\s+de|peso\s+é)?\s*(\d{1,3}(?:[.,]\d+)?)\s*(?:kg|quil[oó]s?|quilos?)", text)
        if match:
            weight = float(match.group(1).replace(",", "."))
            if 20 < weight < 500:  # Validação básica
                profile["weight_kg"] = int(weight)

    # Altura (cm) - múltiplos padrões
    if not profile.get("height_cm"):
        # "175cm", "175 cm", "altura 175", "tenho 175", "1,75m", "175 de altura"
        match = re.search(r"(?:altura|tenho|tenho\s+)?\s*(\d{1,3}(?:[.,]\d+)?)\s*(?:cm|metros?|m|de\s+altura)?", text)
        if match:
            height = float(match.group(1).replace(",", "."))
            # Se parece ser em metros (1.50 a 2.50), converte para cm
            if height < 3:
                height = height * 100
            if 100 <= height <= 250:  # Validação básica
                profile["height_cm"] = int(height)
        # Também tenta padrão "1 metro e 75" ou "1,75"
        match = re.search(r"(\d+)\s*(?:metro|m)[\s,]+(?:e\s+)?(\d+)", text)
        if match and not profile.get("height_cm"):
            height = int(match.group(1)) * 100 + int(match.group(2))
            if 100 <= height <= 250:
                profile["height_cm"] = height

    # Objetivo - melhor detecção
    if not profile.get("goal"):
        goal_text = None
        if any(w in text for w in ["perder", "emagrecer", "reduzir peso", "diminuir"]):
            goal_text = message
        elif any(w in text for w in ["ganhar", "massa", "engordar", "aumentar peso", "crescer"]):
            goal_text = message
        elif any(w in text for w in ["manter", "manter peso", "estabilizar"]):
            goal_text = message
        
        if goal_text:
            profile["goal"] = goal_text

    # Nível de atividade - melhor detecção
    if not profile.get("activity_level"):
        if any(w in text for w in ["sedent", "não faço", "não pratico", "pouco exercício"]):
            profile["activity_level"] = "sedentário"
        elif any(w in text for w in ["leve", "pouco", "caminhada", "caminho"]):
            profile["activity_level"] = "leve"
        elif any(w in text for w in ["moderado", "moderada", "moderadamente", "regular", "regularmente"]):
            profile["activity_level"] = "moderado"
        elif any(w in text for w in ["intenso", "intensa", "muito", "treino", "academia", "frequente"]):
            profile["activity_level"] = "intenso"

    return profile


def profile_is_complete(profile: dict):
    required = ["name", "age", "height_cm", "weight_kg", "goal", "activity_level"]
    return all(profile.get(r) for r in required)
