import { useState } from "react";
import "./chatbot.css";
import { useChatbotAPI } from "../API";
import Message from "../MensageRender/Message";

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [estado, setEstado] = useState({ profile: {} });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [userId] = useState(() => {
    // Gera um ID único para o usuário (ou pode usar localStorage)
    const stored = localStorage.getItem("healthtrack_user_id");
    if (stored) return stored;
    const newId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem("healthtrack_user_id", newId);
    return newId;
  });

  const { sendMessage } = useChatbotAPI();

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      text: input,
    };
    setMessages((prev) => [...prev, userMessage]);
    const userInput = input;
    setInput("");
    setError("");
    setIsLoading(true);

    try {
      const data = await sendMessage(userInput, estado, userId, conversationId);

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: data.resposta || "Sem resposta recebida.",
        plano: data.status === "plano_gerado" ? data.plano : null,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Atualiza conversation_id se retornado
      if (data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      if (data.estado) {
        setEstado(data.estado);
      }
    } catch (err) {
      setError(err.message || "Erro inesperado. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chatbot-landing">
      <div className="hero">
        <h1>Tudo pronto? Então vamos lá!</h1>
        <div className="input-row">
          <button
            className="icon ghost"
            type="button"
            aria-label="Nova conversa"
            onClick={() => {
              setMessages([]);
              setEstado({ profile: {} });
              setConversationId(null);
            }}
          >
            +
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Pergunte alguma coisa"
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <div className="actions">
            <button
              className="icon ghost"
              type="button"
              aria-label="Ativar microfone"
            >
              🎤
            </button>
            <button
              className="icon primary"
              type="button"
              aria-label="Enviar mensagem"
              onClick={handleSend}
              disabled={isLoading}
            >
              ⮕
            </button>
          </div>
        </div>

        {error ? <p className="helper error">{error}</p> : null}
        {isLoading ? <p className="helper muted">Gerando resposta...</p> : null}
      </div>

      <div className="chat-area">
        <div className="message-list">
          {messages.map((msg) => (
            <Message
              key={msg.id}
              role={msg.role}
              text={msg.text}
              plano={msg.plano}
            />
          ))}
          {!messages.length ? (
            <p className="empty">Envie uma mensagem para começar a conversa.</p>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
