# 📘 HealthTrackIA – Documentação do Projeto

## 1. Visão Geral do Projeto

O **HealthTrackIA** é uma aplicação acadêmica criada para fornecer ao usuário, de forma simples e rápida, uma **dieta básica** e um **treino personalizado** com base nas informações coletadas por um chatbot com IA.

A solução utiliza:

- Inteligência Artificial (LLM Gemini)  
- Front-end moderno em **React + Vite**  
- Backend em **Python**  
- Estrutura planejada para futura integração com banco de dados  

---

## 🎯 2. Objetivos do Sistema

- Coletar dados do usuário de forma natural via chatbot LLM  
- Gerar automaticamente uma **dieta** e um **treino básico** com base nos dados coletados  
- Entregar uma interface rápida e intuitiva  
- Possibilitar futura autenticação e armazenamento de perfis em banco de dados  

---

## 🧠 3. Funcionalidades Principais

### 3.1 Chatbot Inteligente

- Desenvolvido em Python usando agente **Gemini**  
- Coleta dados como:  
  - Nome  
  - Idade  
  - Peso  
  - Altura  
  - Objetivo (perder peso, ganhar massa etc.)  
- Gera automaticamente:  
  - Plano de dieta simples  
  - Treino básico adaptado ao objetivo  

### 3.2 Interface Front-End

- Construída com **React + Vite**  
- Comunicação com backend via API  
- Exibe:  
  - Conversa com o chatbot  
  - Resultado da dieta  
  - Plano de treino  

### 3.3 Backend e Arquitetura

- Desenvolvido em **Python**  
- Responsável por:  
  - Operar o modelo Gemini  
  - Tratar rotas da API  
  - Gerar recomendações  
  - Estrutura para integração futura com DB  

### 3.4 Futura Integração com Banco de Dados

Planejado para armazenar:

- Perfis de usuários  
- Histórico de chats  
- Dietas e treinos preferidos  

---

## 🏗️ 4. Arquitetura do Sistema

**Frontend (React + Vite)**  
&nbsp;&nbsp;&nbsp;⬇ API REST (JSON)

**Backend (Python)**
- Agente Gemini (LLM)
- Lógica de recomendação
- Futuro banco de dados

## 💬 5. Fluxo de Funcionamento

1. Usuário acessa o front-end em React  
2. Interface inicia conversa com o chatbot  
3. Chatbot coleta informações do usuário  
4. LLM processa e monta dieta + treino  
5. Front-end exibe o resultado  
6. (Futuro) Usuário pode salvar o perfil  

---

## 🛠️ 6. Tecnologias Utilizadas

### **Frontend**
- React  
- Vite  
- Axios / Fetch  
- Tailwind CSS (opcional)

### **Backend**
- Python 3+  
- Google Gemini (LLM)  
- FastAPI ou Flask  

### **Futuro**
- PostgreSQL / MySQL / MongoDB  
- Autenticação JWT  

---

## 📊 7. Apresentação do Projeto (Pitch)

### **Título:** HealthTrackIA – Seu Assistente Inteligente de Treino e Dieta

### 1. Problema
Muitas pessoas querem melhorar a saúde, mas não sabem por onde começar.

### 2. Solução
Um chatbot inteligente que coleta dados do usuário e gera treino + dieta automaticamente.

### 3. Como Funciona
- Converse com o chatbot  
- Informe seus dados  
- Receba dieta e treino personalizados  
- Tudo em segundos  

### 4. Tecnologias
- IA com Gemini  
- Front-end moderno  
- Backend robusto em Python  
- Futuro banco de dados  

### 5. Benefícios
- Rápido  
- Fácil de usar  
- Personalizado  
- Baseado em IA  
- Escalável  

### 6. Público-Alvo
- Universitários  
- Iniciantes em treinos  
- Pessoas buscando iniciar dieta  

### 7. Futuro do Projeto
- Histórico de evolução  
- Recomendações avançadas  
- Versão mobile  

---

## 📄 8. Considerações Finais

O **HealthTrackIA** combina inteligência artificial, front-end moderno e arquitetura preparada para expansão. É ideal como solução funcional e como estudo acadêmico.
