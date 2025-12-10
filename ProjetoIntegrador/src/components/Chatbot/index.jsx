import "./chatbot.css";

const Chatbot = () => {
  return (
    <div className="app">
      <header className="header">
        <div className="header-left">
          <div className="chatbot-icon">
            <div className="icon-circle">
              <span>🤖</span>
            </div>
            <div className="status-dot"></div>
          </div>
          <div className="header-info">
            <h1>Chatbot</h1>
            <p>Online</p>
          </div>
        </div>
        <div className="header-right">
          <button className="icon-button">🗑️</button>
          <button className="icon-button">✕</button>
        </div>
      </header>

      <main className="chat-area">
        <div className="chatbot-identity">
          <div className="chatbot-icon-small">
            <span>🤖</span>
          </div>
          <span>Chatbot</span>
        </div>

        <div className="message-container">
          <div className="message-bubble">
            <p>Olá! Eu sou o Sr. Chatbot 😎 Prazer em conhecê-lo! 👋</p>
            <span className="timestamp">05 Jun 2023, 18:21</span>
          </div>
          <div className="reaction-buttons">
            <button className="reaction-btn">👍</button>
            <button className="reaction-btn">👎</button>
          </div>
        </div>

        <div className="message-container">
          <div className="message-bubble">
            <p>O que te trouxe aqui hoje?</p>
            <span className="timestamp">05 Jun 2023, 18:21</span>
          </div>
          <div className="reaction-buttons">
            <button className="reaction-btn">👍</button>
            <button className="reaction-btn">👎</button>
          </div>
        </div>
      </main>

      <div className="input-area">
        <input
          type="text"
          placeholder="Digite sua mensagem"
          className="chat-input"
        />
        <button className="send-button">
          <span>✈️</span>
        </button>
      </div>
    </div>
  );
};

export default Chatbot;
