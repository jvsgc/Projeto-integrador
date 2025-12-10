import React from "react";
import { Link } from "react-router-dom";
import "./home.css";

const benefits = [
  {
    number: "01",
    title: "Plano de treino sob medida",
    description:
      "O chatbot monta séries para cada grupo muscular conforme o tempo e os equipamentos que você possui.",
  },
  {
    number: "02",
    title: "Dieta adaptada ao seu objetivo",
    description:
      "Sugestões simples para emagrecer ou ganhar massa magra sem sair da sua rotina.",
  },
  {
    number: "03",
    title: "Ajustes em tempo real",
    description:
      "Troque exercícios, substitua alimentos e tire dúvidas instantaneamente durante a conversa.",
  },
  {
    number: "04",
    title: "Metas claras e motivação",
    description:
      "Receba lembretes inteligentes e micro passos que mantêm o foco diariamente.",
  },
  {
    number: "05",
    title: "Insights personalizados",
    description:
      "O sistema detecta padrões, indica descansos e mostra onde você pode evoluir primeiro.",
  },
  {
    number: "06",
    title: "Experiência simples e humana",
    description:
      "Nada de planos engessados: cada resposta considera preferências, humor e disponibilidade.",
  },
];

const Home = () => {
  return (
    <div className="home">
      <header className="home__header">
        <p className="home__eyebrow">HealthTrack IA</p>
        <h1>Uma solução simples para unir dieta, treino e rotina</h1>
        <p>
          Converse com o chatbot, compartilhe seus horários e objetivos e receba
          um plano completo com exercícios por grupo muscular e alimentação
          prática, sempre ajustado à sua realidade.
        </p>
      </header>

      <div className="home__content">
        <div className="home__intro">
          <p>
            Todos os dados serão coletados em conversas rápidas com o nosso
            assistente. Ele entende restrições, preferências e nível de energia
            para entregar recomendações que fazem sentido hoje e se adaptam
            amanhã.
          </p>
        </div>

        <div className="home__benefits">
          <h2>Benefícios da HealthTrack IA</h2>
          <p className="home__subtitle">
            Inspirado em hábitos de pessoas supersaudáveis, apresentado de forma
            simples e direta para você.
          </p>

          <div className="home__benefits-grid">
            {benefits.map((benefit) => (
              <div className="home__benefit" key={benefit.number}>
                <span className="home__benefit-number">{benefit.number}</span>
                <div className="home__benefit-copy">
                  <h3>{benefit.title}</h3>
                  <p>{benefit.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="home__cta">
        <div className="home__cta-image" aria-hidden="true" />
        <div className="home__cta-content">
          <p className="home__cta-eyebrow">Converse com o chatbot</p>
          <h2>Crie hábitos alimentares saudáveis</h2>
          <p>
            Compartilhe horários, preferências e objetivos. Em poucos minutos,
            você recebe um plano integrado com exercícios por grupo muscular e
            uma dieta simples, seja para emagrecer ou ganhar massa magra.
          </p>
          <p>
            <span className="home__cta-credit"></span>
          </p>
          <Link to="/chatbot" className="home__cta-button">
            Consulte mais informação
          </Link>
        </div>
      </div>

      <footer className="home__footer">
        <p>Em breve: informações de contato e links importantes.</p>
      </footer>
    </div>
  );
};

export default Home;
