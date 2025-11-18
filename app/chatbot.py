# app/chatbot.py
from google import genai
from app.config import settings
import os
import json
from tabulate import tabulate

# Inicializa cliente com chave do .env
client = genai.Client(api_key=settings.GEMINI_API_KEY)
MODEL = "gemini-2.5-flash"


# --- Utilitários ---

# Cálculo de IMC


def bmi(weight_kg, height_cm):
    h = height_cm / 100.0
    return weight_kg / (h * h)


def safe_goal_check(profile):
    """Checagens simples de segurança. Retorna (ok:bool, msg:str)."""
    age = profile.get("age")
    weight = profile.get("weight_kg")
    height = profile.get("height_cm")
    goal = profile.get("goal", "")

    if age is not None and (age < 13 or age > 120):
        return False, "Idade fora do intervalo típico (menor que 13 ou maior que 120). Consulte um profissional."
    if weight is not None and (weight <= 20 or weight > 500):
        return False, "Peso com valor incomum — verifique os dados."
    if height is not None and (height < 100 or height > 250):
        return False, "Altura com valor incomum — verifique os dados."

    if weight and height:
        imc = bmi(weight, height)
        # metas de perda de peso muito rápidas: recusar
        if "perder" in goal.lower():
            # se objetivo textual contém quanto quer perder, tentamos detectar número aproximado
            import re
            m = re.search(r"(\d+\s*(kg|quil?os?))", goal.lower())
            if m:
                kilos = int(re.findall(r"\d+", m.group(0))[0])
                # se meta >20 kg num curto prazo, recusar
                if kilos > 20:
                    return False, "Meta de perda de peso muito grande solicitada — recomenda-se acompanhamento médico/nutricional."
        # IMC extremo
        if imc < 15 or imc > 45:
            return False, f"IMC extremo detectado ({imc:.1f}). Recomendado avaliação médica com urgência."

    return True, "ok"


# --- Prompt / geração ---

def build_system_prompt():
    return (
        "Você é um assistente de saúde e nutrição focado em sugestões práticas e seguras. "
        "Forneça planos alimentares gerais, sugestões de mudanças de estilo de vida e justificativas simples. "
        "Nunca forneça diagnósticos médicos ou prescreva medicamentos. Sempre inclua um aviso para procurar um profissional de saúde quando aplicável. "
        "Se detectar sinais de perigo (IMC extremo, objetivos irreais, sintomas de emergência), recuse-se a fornecer um plano detalhado e oriente o usuário a procurar atendimento médico."
    )


def generate_plan(profile, history=None):
    """Chama o Gemini para gerar um plano. Retorna texto gerado."""
    # Monta instruções do usuário em formato estruturado
    user_content = (
        "Usuário Profile JSON:\n" +
        json.dumps(profile, ensure_ascii=False) + "\n\n"
        "Tarefa: com base nos dados acima, gere:\n"
        "1) Resumo objetivo do estado atual do usuário (1-2 frases).\n"
        "2) Regras dietéticas práticas e fáceis de seguir (máx 8 itens).\n"
        "3) Um exemplo de plano alimentar de 1 dia (café, almoço, jantar, 2 lanches) com porções.\n"
        "4) Sugestões de atividade física semanal simples (máx 6 itens).\n"
        "5) Quais sinais exigiriam consulta médica imediata.\n"
        "Formato de saída: JSON com chaves: summary, rules, sample_day (list of meals), exercise, warnings."
    )

    system = build_system_prompt()

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            {"text": system},
            {"text": user_content}
        ]
    )

    # O objeto de resposta pode ter .text ou estrutura; tentamos extrair .text
    text = getattr(response, 'text', None)
    if text is None:
        # fallback: algumas SDKs retornam candidates
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception:
            text = str(response)

    return text


# --- Interface simples de CLI ---

def gather_user_profile_cli():
    print("--- Coleta rápida de dados do usuário (deixe vazio para ignorar) ---")
    profile = {}
    try:
        profile['name'] = input('Nome: ').strip() or None
        profile['age'] = int(input('Idade (anos): ') or 0) or None
    except ValueError:
        profile['age'] = None
    try:
        profile['height_cm'] = float(input('Altura (cm): ') or 0) or None
    except ValueError:
        profile['height_cm'] = None
    try:
        profile['weight_kg'] = float(input('Peso (kg): ') or 0) or None
    except ValueError:
        profile['weight_kg'] = None

    profile['activity_level'] = input(
        'Nível de atividade (sedentário, leve, moderado, intenso): ').strip() or None
    profile['dietary_preferences'] = input(
        'Preferências alimentares (ex: vegetariano, vegano, omnivore) ou restrições: ').strip() or None
    profile['allergies'] = input(
        'Alergias / intolerâncias (separadas por vírgula): ').strip() or None
    profile['goal'] = input(
        'Objetivo principal (ex: perder 5 kg, ganhar massa, manter peso, melhorar sono): ').strip() or None

    return profile


def pretty_print_json_like(text):
    # tenta extrair JSON do texto; se não, imprime como está
    import re
    m = re.search(r"\{[\s\S]*\}", text)
    if m:
        try:
            j = json.loads(m.group(0))
            print('\n' + json.dumps(j, indent=2, ensure_ascii=False))
            return
        except Exception:
            pass
    print('\n' + text)


def main():
    print("Agente de Saúde (CLI)")
    profile = gather_user_profile_cli()

    ok, msg = safe_goal_check(profile)
    if not ok:
        print('\nATENÇÃO: ' + msg)
        print('Por segurança, recomendo consultar um profissional antes de prosseguir.')
        return

    print('\nGerando plano...')
    plan_text = generate_plan(profile)

    print('\n--- Resultado gerado pela IA ---')
    pretty_print_json_like(plan_text)
    print('\nLembrete: essas são diretrizes gerais. Consulte um profissional para recomendações personalizadas.')


if __name__ == '__main__':
    main()
