import "./message.css";

const Message = ({ role, text, plano }) => {
  return (
    <div className={`message ${role}`}>
      <span className="role">{role === "assistant" ? "IA" : "Você"}</span>
      <p>{text}</p>
      {plano && <PlanView plano={plano} />}
    </div>
  );
};

const PlanView = ({ plano }) => {
  // Tenta parsear se for string JSON
  let planData = plano;
  if (typeof plano === "string") {
    try {
      // Tenta extrair JSON da string se houver
      const jsonMatch = plano.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        planData = JSON.parse(jsonMatch[0]);
      }
    } catch (e) {
      // Se não conseguir parsear, mantém como texto
      planData = plano;
    }
  }

  // Se for objeto, renderiza estruturado
  if (typeof planData === "object" && planData !== null) {
    return (
      <div className="plan-container">
        {planData.summary && (
          <div className="plan-section">
            <h3>Resumo</h3>
            <p>{planData.summary}</p>
          </div>
        )}
        {planData.rules && (
          <div className="plan-section">
            <h3>Regras Dietéticas</h3>
            <ul>
              {Array.isArray(planData.rules)
                ? planData.rules.map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))
                : Object.values(planData.rules).map((rule, idx) => (
                    <li key={idx}>{rule}</li>
                  ))}
            </ul>
          </div>
        )}
        {planData.sample_day && (
          <div className="plan-section">
            <h3>Exemplo de Plano Alimentar (1 dia)</h3>
            {Array.isArray(planData.sample_day) ? (
              <ul>
                {planData.sample_day.map((meal, idx) => (
                  <li key={idx}>
                    <strong>{meal.meal || meal.name || `Refeição ${idx + 1}`}:</strong>{" "}
                    {meal.food || meal.content || JSON.stringify(meal)}
                  </li>
                ))}
              </ul>
            ) : (
              <pre>{JSON.stringify(planData.sample_day, null, 2)}</pre>
            )}
          </div>
        )}
        {planData.exercise && (
          <div className="plan-section">
            <h3>Atividade Física Semanal</h3>
            <ul>
              {Array.isArray(planData.exercise)
                ? planData.exercise.map((ex, idx) => <li key={idx}>{ex}</li>)
                : Object.values(planData.exercise).map((ex, idx) => (
                    <li key={idx}>{ex}</li>
                  ))}
            </ul>
          </div>
        )}
        {planData.warnings && (
          <div className="plan-section warnings">
            <h3>⚠️ Sinais que Exigem Consulta Médica</h3>
            <ul>
              {Array.isArray(planData.warnings)
                ? planData.warnings.map((warning, idx) => (
                    <li key={idx}>{warning}</li>
                  ))
                : Object.values(planData.warnings).map((warning, idx) => (
                    <li key={idx}>{warning}</li>
                  ))}
            </ul>
          </div>
        )}
        {planData.raw && (
          <div className="plan-section">
            <pre className="plan-raw">{planData.raw}</pre>
          </div>
        )}
      </div>
    );
  }

  // Se for texto simples, renderiza como pre-formatado
  return (
    <div className="plan-container">
      <pre className="plan-raw">{plano}</pre>
    </div>
  );
};

export default Message;

