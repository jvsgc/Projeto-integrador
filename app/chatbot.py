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
        "Você é um assistente de saúde altamente conversacional. "
        "Seu papel é guiar o usuário de forma natural, perguntando dados como idade, altura, peso, nível de atividade "
        "e objetivo de saúde ANTES de gerar o plano.\n\n"

        "REGRAS IMPORTANTES:\n"
        "1. Fale como um humano, de forma simples e acolhedora.\n"
        "2. Sempre responda mensagens parciais naturalmente.\n"
        "3. Se faltarem informações importantes, pergunte educadamente.\n"
        "4. Quando tiver todos os dados, produza o plano final em JSON.\n"
        "5. Nunca dê diagnósticos médicos.\n"
        "6. Sempre incentive o usuário com leveza.\n"
        "7. Nunca assuma dados — sempre confirme com o usuário.\n\n"

        "Formato final do plano (apenas quando os dados estiverem completos):\n"
        "{\n"
        "  summary: string,\n"
        "  rules: [string],\n"
        "  sample_day: [{ meal: string, description: string }],\n"
        "  exercise: [string],\n"
        "  warnings: [string]\n"
        "}\n\n"

        "Durante a conversa, você NÃO deve gerar o JSON até ter:\n"
        "- idade\n"
        "- altura\n"
        "- peso\n"
        "- objetivo\n"
        "- nível de atividade\n\n"

        "Se algo estiver faltando, diga exatamente o que falta.\n"
    
    )


def conversational_response(profile, user_message):
    missing = []

    if not profile.get("age"):
        missing.append("idade")
    if not profile.get("height_cm"):
        missing.append("altura")
    if not profile.get("weight_kg"):
        missing.append("peso")
    if not profile.get("activity_level"):
        missing.append(
            "nível de atividade (sedentário, leve, moderado ou intenso)")
    if not profile.get("goal"):
        missing.append("seu objetivo (ex: perder 5kg, ganhar massa)")

    if len(missing) == 0:
        return "Tudo certo! Estou gerando seu plano personalizado..."

    missing_text = ", ".join(missing)
    return f"Obrigado pelas informações! Agora me diga: {missing_text}."


def gerar_resposta(pergunta: str) -> str:
    return f"Você disse: {pergunta}"


def responder_pergunta_geral(mensagem: str):
    """Detecta e responde perguntas gerais sobre o chatbot"""
    texto = mensagem.lower()
    
    # Palavras-chave para perguntas sobre funcionamento
    palavras_funcionamento = ["como funciona", "como trabalha", "como você trabalha", "como você funciona", 
                              "como funciona o chatbot", "como você ajuda", "o que você faz"]
    
    # Palavras-chave para benefícios
    palavras_beneficios = ["benefícios", "beneficio", "vantagens", "vantagem", "por que usar", 
                           "porque usar", "para que serve", "o que oferece", "o que você oferece"]
    
    # Palavras-chave para o que é/características
    palavras_sobre = ["o que é", "quem é você", "quem é voce", "o que você é", "você é", "voce é",
                      "me fale sobre", "me conte sobre", "fale sobre", "conte sobre"]
    
    # Respostas sobre funcionamento
    if any(palavra in texto for palavra in palavras_funcionamento):
        respostas = [
            "🤖 Olha, eu trabalho assim: você me conta seus dados (idade, altura, peso, nível de atividade e objetivo), e eu crio um plano personalizado de dieta e exercícios só para você! 💪\n\nÉ bem simples: você conversa comigo naturalmente, eu entendo suas informações e no final te entrego um plano completo! ✨",
            "💡 Funciono assim: você me passa suas informações de saúde e objetivos, e eu gero um plano personalizado com dieta e exercícios! 🎯\n\nA gente conversa de forma natural, eu vou coletando seus dados e quando tiver tudo, crio seu plano completo! 🚀",
            "🌟 É simples! Você me conta sobre você (idade, altura, peso, atividade física e objetivo), e eu preparo um plano de alimentação e exercícios personalizado! 📋\n\nConversamos de forma natural e no final você recebe tudo organizado! ✨"
        ]
        import random
        return random.choice(respostas)
    
    # Respostas sobre benefícios
    if any(palavra in texto for palavra in palavras_beneficios):
        respostas = [
            "🎯 Os benefícios são muitos! Comigo você:\n\n✅ Recebe um plano personalizado só seu\n✅ Tem dieta e exercícios adaptados ao seu objetivo\n✅ Economiza tempo (não precisa pesquisar tudo sozinho)\n✅ Tem orientações práticas e fáceis de seguir\n✅ Pode ajustar conforme sua rotina\n\nBasicamente, eu simplifico sua jornada de saúde! 💪✨",
            "💪 Os principais benefícios:\n\n🌟 Plano 100% personalizado para você\n🍎 Sugestões de dieta práticas e realistas\n🏋️ Exercícios adaptados ao seu nível\n⏰ Economia de tempo e pesquisa\n📱 Acesso fácil e rápido\n🎯 Foco no seu objetivo específico\n\nResumindo: facilidade + personalização = resultados melhores! 🚀",
            "✨ Vantagens de usar o chatbot:\n\n🎯 Personalização total (plano só seu)\n🍽️ Dieta adaptada ao seu dia a dia\n💪 Treino adequado ao seu nível\n📊 Tudo organizado e fácil de seguir\n⚡ Respostas rápidas e práticas\n🔄 Pode ajustar quando quiser\n\nÉ como ter um personal trainer e nutricionista sempre disponível! 🌟"
        ]
        import random
        return random.choice(respostas)
    
    # Respostas sobre o que é
    if any(palavra in texto for palavra in palavras_sobre):
        respostas = [
            "👋 Olá! Eu sou o assistente de saúde da HealthTrack IA! 🤖\n\nMeu trabalho é ajudar você a criar um plano personalizado de dieta e exercícios baseado nas suas informações e objetivos! 💪\n\nSou como um personal trainer e nutricionista digital - sempre aqui para te ajudar! ✨",
            "🌟 Eu sou o chatbot da HealthTrack IA! 🚀\n\nSou especializado em criar planos personalizados de saúde: dieta + exercícios adaptados especialmente para você! 🎯\n\nPense em mim como seu assistente de saúde 24/7, sempre pronto para ajudar! 💪✨",
            "💡 Eu sou o assistente inteligente da HealthTrack IA! 🤖\n\nMinha missão é te ajudar a alcançar seus objetivos de saúde criando um plano completo e personalizado! 📋\n\nSou focado em tornar sua jornada de saúde mais simples e eficiente! 🌟"
        ]
        import random
        return random.choice(respostas)
    
    return None


def gerar_resposta_humanizada(mensagem_usuario: str, profile: dict, dados_coletados: list = None):
    """Gera uma resposta humanizada - versão simplificada e focada."""
    
    faltando = []
    # Nome sempre primeiro
    if not profile.get("name"):
        faltando.append("seu nome")
    if not profile.get("age"):
        faltando.append("sua idade")
    if not profile.get("height_cm"):
        faltando.append("sua altura (em cm ou metros)")
    if not profile.get("weight_kg"):
        faltando.append("seu peso (em kg)")
    if not profile.get("activity_level"):
        faltando.append("seu nível de atividade física (sedentário, leve, moderado ou intenso)")
    if not profile.get("goal"):
        faltando.append("seu objetivo (ex: perder peso, ganhar massa, manter o peso)")

    # Respostas pré-definidas mais variadas e humanizadas (com emojis)
    respostas_reconhecimento = [
        "Ótimo! ✅ Anotei sua {dado}.",
        "Perfeito! ✨ Já tenho sua {dado} aqui.",
        "Entendido! 📝 Sua {dado} está registrada.",
        "Show! 🎯 Anotei sua {dado}.",
        "Perfeito! 💪 Registrei sua {dado}.",
    ]
    
    respostas_multiplas = [
        "Perfeito! ✨ Anotei: {dados}.",
        "Ótimo! ✅ Já tenho: {dados}.",
        "Show! 🎯 Registrei: {dados}.",
        "Excelente! 💪 Anotei: {dados}.",
    ]

    # Se coletou algo nesta mensagem, reconhece de forma variada
    reconhecimento = ""
    nome_usuario = profile.get("name", "")
    tratamento = f", {nome_usuario}" if nome_usuario else ""
    
    if dados_coletados:
        import random
        if len(dados_coletados) == 1:
            template = random.choice(respostas_reconhecimento)
            reconhecimento = template.format(dado=dados_coletados[0])
        else:
            template = random.choice(respostas_multiplas)
            dados_str = ', '.join(dados_coletados[:-1]) + f' e {dados_coletados[-1]}'
            reconhecimento = template.format(dados=dados_str)

    # Fallback: respostas pré-definidas variadas e humanizadas (simplificado)
    import random
    
    if dados_coletados:
        if len(faltando) == 0:
            finalizacoes = [
                "🎉 Perfeito! Agora tenho todas as informações. Vou criar seu plano personalizado! ⏳",
                "✨ Excelente! Com essas informações vou montar um plano perfeito para você! 💪",
                "🚀 Ótimo! Estou preparando seu plano personalizado agora mesmo! 📋",
                "🎯 Perfeito! Tenho tudo que preciso. Criando seu plano agora! ⚡",
            ]
            return random.choice(finalizacoes)
        elif len(faltando) == 1:
            perguntas = [
                f"{reconhecimento} Só falta me contar {faltando[0]}. 😊",
                f"{reconhecimento} Agora me diga {faltando[0]}. 💬",
                f"{reconhecimento} Falta só {faltando[0]}. ✨",
                f"{reconhecimento} Me conte {faltando[0]}. 📝",
            ]
            return random.choice(perguntas)
        elif len(faltando) == 2:
            perguntas = [
                f"{reconhecimento} Ainda preciso saber {faltando[0]} e {faltando[1]}. 😊",
                f"{reconhecimento} Me conte também {faltando[0]} e {faltando[1]}. 💬",
                f"{reconhecimento} Falta {faltando[0]} e {faltando[1]}. ✨",
                f"{reconhecimento} Agora me diga {faltando[0]} e {faltando[1]}. 📝",
            ]
            return random.choice(perguntas)
        else:
            return f"{reconhecimento} Me conte também {faltando[0]} e {faltando[1]}. 😊"
    else:
        # Primeira mensagem - sempre começa pelo nome
        if not profile.get("name"):
            saudacoes = [
                f"👋 Olá{tratamento}! Prazer em conhecê-lo! 😊\n\nPara começar, qual é o seu nome?",
                f"🌟 Oi{tratamento}! Que bom ter você aqui! ✨\n\nMe diga seu nome para começarmos:",
                f"👋 Olá{tratamento}! Vamos criar seu plano personalizado! 💪\n\nPrimeiro, qual é o seu nome?",
            ]
            return random.choice(saudacoes)
        elif len(faltando) == 1:
            saudacoes = [
                f"👋 Olá{tratamento}! Para criar seu plano personalizado, preciso saber {faltando[0]}. 💪",
                f"😊 Oi{tratamento}! Me conte {faltando[0]} para continuarmos. ✨",
                f"👋 Olá{tratamento}! Agora preciso saber {faltando[0]}. 🎯",
            ]
            return random.choice(saudacoes)
        elif len(faltando) == 2:
            saudacoes = [
                f"👋 Olá{tratamento}! Me conte {faltando[0]} e {faltando[1]}. 😊",
                f"🌟 Oi{tratamento}! Preciso saber {faltando[0]} e {faltando[1]}. ✨",
                f"👋 Olá{tratamento}! Me diga {faltando[0]} e {faltando[1]}. 💪",
            ]
            return random.choice(saudacoes)
        elif len(faltando) >= 3:
            # Pede apenas 2 por vez
            saudacoes = [
                f"👋 Olá{tratamento}! Para continuar, me conte {faltando[0]} e {faltando[1]}. 😊",
                f"🌟 Oi{tratamento}! Vamos continuar? Me diga {faltando[0]} e {faltando[1]}. ✨",
                f"👋 Olá{tratamento}! Agora preciso saber {faltando[0]} e {faltando[1]}. 💪",
            ]
            return random.choice(saudacoes)
        else:
            saudacoes = [
                f"👋 Olá{tratamento}! Como posso ajudar você hoje? 😊",
                f"🌟 Oi{tratamento}! Em que posso ajudar? ✨",
                f"👋 Olá{tratamento}! Estou aqui para ajudar você! 💪",
            ]
            return random.choice(saudacoes)


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
