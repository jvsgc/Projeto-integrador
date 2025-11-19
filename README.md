# 🩺 HealthTrack AI  
### Projeto Integrador — Curso de Análise e Desenvolvimento de Sistemas (ADS)  
**Disciplina:** AED: Projeto Integrador - Desenvolvimento de Aplicação com CI/CD no GitLab  
**Equipe:** Rodrigo Madeira Cervantes, João Vitor Sena  

---

## 1. Nome do Projeto  
**HealthTrack AI — Sistema de recomendação de hábitos saudáveis personalizados**

---

## 2. Problema a ser Resolvido  
Muitas pessoas recebem recomendações genéricas sobre saúde (como alimentação, sono e exercícios) que não consideram suas características individuais — idade, peso, rotina, limitações físicas e objetivos.  
Isso reduz a eficácia e a adesão.  

O **HealthTrack AI** busca oferecer recomendações **personalizadas e práticas**, com base nos dados do usuário e em padrões aprendidos por **modelos de Inteligência Artificial (IA)**.

---

## 3. Descrição da Aplicação  
Aplicação **web em Python** onde o usuário cria um perfil com suas informações (idade, peso, altura, rotina, objetivos, etc.) e recebe:  
- Plano diário ou semanal de **atividades físicas sugeridas**  
- Recomendações de **sono e alimentação**  
- **Sugestões de hábitos comportamentais** e alertas de acompanhamento  

O sistema inclui:  
- Cadastro e autenticação de usuários  
- Dashboard com histórico de progresso  
- Exportação de plano e histórico (PDF/CSV)  
- Módulo de IA que gera recomendações personalizadas  

---

## 4. Tecnologias e Ferramentas  
- **Backend:** FastAPI (Python)  
- **Frontend:** React ou templates Jinja  
- **Banco de Dados:** PostgreSQL / SQLite  
- **IA / ML:** scikit-learn (classificação, regressão, K-NN)  
- **Estruturas de Dados:** KD-Tree e Hash Tables  
- **Segurança:** bcrypt, JWT, validação com Pydantic  
- **CI/CD:** GitLab com estágios `build` e `test` automatizados  
- **Testes:** pytest com cobertura mínima de 70%  

---

## 5. Aplicação dos Pilares Técnicos  

**Estruturas de Dados:**  
- KD-Tree para busca de perfis semelhantes  
- Hash Tables para cache e indexação de usuários  

**Inteligência Artificial:**  
- Modelo híbrido: classificação/regressão + sistema de recomendação K-NN  

**Código Seguro:**  
- Senhas criptografadas com bcrypt  
- Validação de entrada rigorosa com Pydantic  
- Proteções contra injeção SQL e checklist baseado no OWASP Top 10  

---

## 6. CI/CD (GitLab)  
O repositório conterá um pipeline CI/CD com os seguintes estágios:  
- **Build:** instalação de dependências e verificação de linting  
- **Test:** execução de testes com pytest (mínimo 70% de cobertura)  
- **Deploy (opcional):** publicação automática no Render, Heroku ou AWS  

---

## 7. Cronograma (8 Semanas)  
1. Formação da equipe e setup do repositório  
2. Modelagem do banco e autenticação  
3. Implementação do KD-Tree e pipeline de dados (ETL)  
4. Treinamento inicial do modelo de IA  
5. Integração backend + IA  
6. Segurança e testes unitários  
7. CI/CD e documentação do pipeline  
8. Testes finais e apresentação  

---

## 8. Entregáveis  
- Repositório GitLab com código e documentação  
- Pipeline CI/CD funcional (`.gitlab-ci.yml`)  
- Documentação técnica (README, instruções, relatório de segurança)  
- Demonstração e apresentação final  

---

## 9. Critérios de Avaliação  
- Complexidade técnica (KD-Tree + IA híbrida)  
- Aplicação dos conceitos (ED, IA, Código Seguro e CI/CD)  
- Qualidade do código e dos testes  
- Qualidade da documentação e apresentação  

---

## 10. Conclusão  
O **HealthTrack AI** é um projeto viável, tecnicamente sólido e totalmente alinhado aos pilares do curso.  
Ele demonstra a aplicação integrada de **Estruturas de Dados, Inteligência Artificial, Código Seguro** e **CI/CD no GitLab**, resultando em um sistema moderno e escalável voltado para a melhoria da saúde e qualidade de vida dos usuários.
