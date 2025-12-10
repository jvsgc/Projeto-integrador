import { useMemo } from "react";

export const useChatbotAPI = () => {
  const apiBase = useMemo(
    () => import.meta.env.VITE_API_URL || "http://localhost:8000",
    []
  );

  const sendMessage = async (mensagem, estado = {}, userId = "anonymous", conversationId = null) => {
    try {
      const response = await fetch(`${apiBase}/chatbot/autonomo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mensagem,
          estado,
          user_id: userId,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
          `Erro ${response.status}: ${errorText || "Falha ao contatar o servidor do chatbot."}`
        );
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
        throw new Error(
          "Não foi possível conectar ao servidor. Verifique se o backend está rodando em http://localhost:8000"
        );
      }
      throw new Error(error.message || "Erro inesperado. Tente novamente.");
    }
  };

  return { sendMessage, apiBase };
};
