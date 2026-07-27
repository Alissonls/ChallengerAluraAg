import React from 'react';
import { Cpu, Cloud, Sun, Moon, ShieldCheck, Database } from 'lucide-react';

export default function Header({ isDark, toggleTheme, ociStatus, stats }) {
  return (
    <header className="header-bar">
      <div className="brand-logo">
        <div className="logo-badge">
          <Cpu size={24} />
        </div>
        <div>
          <h1 className="brand-title">Nexus AI</h1>
          <p className="brand-subtitle">Agente Corporativo de Conhecimento Multi-Formato</p>
        </div>
      </div>

      <div className="header-badges">
        <div className="oci-badge" title="Oracle Cloud Infrastructure Integration">
          <Cloud size={16} />
          <span>OCI Cloud (sa-saopaulo-1)</span>
          <span className="oci-pulse-dot" />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--bg-surface-elevated)', padding: '0.4rem 0.8rem', borderRadius: 'var(--radius-full)', fontSize: '0.8rem', border: '1px solid var(--border-subtle)' }}>
          <Database size={14} color="#8b5cf6" />
          <span>{stats?.total_documents || 0} Docs / {stats?.total_chunks || 0} Chunks</span>
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
