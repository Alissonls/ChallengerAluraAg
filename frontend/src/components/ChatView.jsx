import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, FileSearch, CheckCircle, ExternalLink } from 'lucide-react';

const SUGGESTIONS = [
  { label: "🎯 OKRs & Estratégia 2026", query: "Quais são as metas e OKRs estratégicos para 2026?", domain: "Estratégico" },
  { label: "💼 Auxílio Home Office RH", query: "Qual é o valor do auxílio home office e dos benefícios de RH?", domain: "Recursos Humanos" },
  { label: "🔒 DPO & Retenção LGPD", query: "Quem é a encarregada DPO e qual a política de retenção de dados da LGPD?", domain: "Legal e Compliance" },
  { label: "💰 Preços e Planos Comercial", query: "Quais são os planos e preços na tabela comercial?", domain: "Marketing e Comercial" },
  { label: "⚙️ SLA de Incidentes de TI", query: "Qual o tempo máximo de resposta para chamados críticos de TI?", domain: "Operacional" }
];

export default function ChatView({ userDepartment, onSelectCitation }) {
  const [messages, setMessages] = useState([
    {
      id: "welcome",
      sender: "agent",
      text: `Olá! Sou o **Nexus AI**, o Chatbot corporativo. Você está conectado como colaborador do setor de **${userDepartment}**.\n\n🔒 *Por política de segurança da empresa, você possui acesso exclusivo aos documentos do seu setor e comunicados internos. Consultas a outros setores serão bloqueadas.*`,
      sources: [],
      timestamp: "Agora"
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText = inputQuery) => {
    const textToSend = queryText.trim();
    if (!textToSend || loading) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: "user",
      text: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    if (queryText === inputQuery) setInputQuery('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: textToSend, user_department: userDepartment })
      });
      const data = await res.json();

      const isRestricted = data.confidence === "Restrito";

      const agentMsg = {
        id: (Date.now() + 1).toString(),
        sender: "agent",
        text: data.answer,
        sources: data.sources || [],
        confidence: data.confidence || "Alta",
        isRestricted: isRestricted,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, agentMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        {
          id: Date.now().toString(),
          sender: "agent",
          text: "Desculpe, ocorreu uma falha ao comunicar com o servidor do Chatbot RAG.",
          sources: [],
          timestamp: "Erro"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="chat-container">
      <div className="chat-messages-scroll">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-row ${msg.sender}`}>
            <div className={`message-avatar ${msg.sender === 'agent' ? 'avatar-agent' : 'avatar-user'}`}>
              {msg.sender === 'agent' ? <Bot size={20} /> : <User size={20} />}
            </div>

            <div className="message-card">
              <div className="message-meta">
                <span>{msg.sender === 'agent' ? 'Nexus AI Agente Corporativo' : 'Você'}</span>
                <span>•</span>
                <span>{msg.timestamp}</span>
                {msg.confidence && (
                  <span style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.2rem', color: '#10b981', fontWeight: 600 }}>
                    <CheckCircle size={12} /> Confiança {msg.confidence}
                  </span>
                )}
              </div>

              <div style={{ whiteSpace: 'pre-line', fontSize: '0.95rem' }}>
                {msg.text}
              </div>

              {msg.sources && msg.sources.length > 0 && (
                <div className="source-citations-list">
                  <span style={{ width: '100%', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                    <FileSearch size={13} /> Fontes da Resposta (RAG):
                  </span>
                  {msg.sources.map((src, idx) => (
                    <button
                      key={idx}
                      className="citation-chip"
                      onClick={() => onSelectCitation(src)}
                    >
                      <ExternalLink size={12} />
                      <span>{src.filename}</span>
                      <span style={{ opacity: 0.7 }}>({src.doc_type})</span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row agent">
            <div className="message-avatar avatar-agent">
              <Sparkles size={20} className="pulse-icon" />
            </div>
            <div className="message-card" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-muted)' }}>
              <div className="oci-pulse-dot" />
              <span>Consultando índice RAG e síntese corporativa...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="prompt-suggestions-row">
          {SUGGESTIONS.map((s, i) => (
            <button
              key={i}
              className="suggestion-pill"
              onClick={() => handleSend(s.query, s.domain)}
            >
              {s.label}
            </button>
          ))}
        </div>

        <div className="input-box-wrapper">
          <input
            type="text"
            className="chat-input-field"
            placeholder={`Faça uma pergunta sobre documentos de ${selectedDomain}...`}
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button 
            className="send-btn" 
            onClick={() => handleSend()}
            disabled={loading}
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
