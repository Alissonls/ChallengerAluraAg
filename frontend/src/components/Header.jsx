import React from 'react';
import { Cpu, Cloud, Sun, Moon, Database, ShieldCheck, UserCheck } from 'lucide-react';

const DEPARTMENTS = [
  "Recursos Humanos",
  "Financeiro e Contábil",
  "Operacional",
  "Estratégico",
  "Legal e Compliance",
  "Marketing e Comercial",
  "Dados e Sistemas",
  "Pesquisa e Desenvolvimento",
  "Qualidade",
  "Comunicação Interna",
  "Administrador"
];

export default function Header({ isDark, toggleTheme, userDepartment, onChangeDepartment, stats }) {
  return (
    <header className="header-bar">
      <div className="brand-logo">
        <div className="logo-badge">
          <Cpu size={24} />
        </div>
        <div>
          <h1 className="brand-title">Nexus AI Chatbot</h1>
          <p className="brand-subtitle">Agente Corporativo com Trava de Acesso por Setor (RBAC)</p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', background: 'var(--bg-surface-elevated)', border: '1px solid var(--border-glow)', padding: '0.4rem 0.9rem', borderRadius: 'var(--radius-full)', fontSize: '0.85rem' }}>
        <UserCheck size={16} color="var(--accent-primary)" />
        <span style={{ fontWeight: 600 }}>Setor do Colaborador:</span>
        <select 
          value={userDepartment}
          onChange={(e) => onChangeDepartment(e.target.value)}
          style={{ background: 'transparent', border: 'none', color: 'var(--accent-primary)', fontWeight: 700, outline: 'none', cursor: 'pointer', fontFamily: 'inherit' }}
        >
          {DEPARTMENTS.map(d => (
            <option key={d} value={d} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
              {d === "Administrador" ? "🔑 Administrador" : `👥 ${d}`}
            </option>
          ))}
        </select>
      </div>

      <div className="header-badges">
        <div className="oci-badge" title="Oracle Cloud Infrastructure Integration">
          <Cloud size={16} />
          <span>OCI Cloud (sa-saopaulo-1)</span>
          <span className="oci-pulse-dot" />
        </div>

        <button 
          onClick={toggleTheme}
          style={{
            background: 'var(--bg-surface-elevated)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-primary)',
            padding: '0.45rem',
            borderRadius: 'var(--radius-md)',
            cursor: 'pointer',
            display: 'flex',
            align-items: 'center',
            justify-content: 'center'
          }}
          title={isDark ? "Alternar para Modo Claro" : "Alternar para Modo Escuro"}
        >
          {isDark ? <Sun size={18} color="#f59e0b" /> : <Moon size={18} color="#6366f1" />}
        </button>
      </div>
    </header>
  );
}

