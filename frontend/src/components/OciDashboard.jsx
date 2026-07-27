import React from 'react';
import { Cloud, Server, Shield, CheckCircle, Database, Cpu, Layers } from 'lucide-react';

export default function OciDashboard({ ociStatus, stats }) {
  return (
    <div className="oci-dashboard-view">
      <div>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <Cloud size={28} color="#00758f" />
          <span>Oracle Cloud Infrastructure (OCI) Status & Metrics</span>
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '0.2rem' }}>
          Monitoramento do Agente Corporativo hospedado e integrado com os serviços da Nuvem Oracle.
        </p>
      </div>

      <div className="metrics-row">
        <div className="metric-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span className="metric-lbl">Status da Instância OCI</span>
            <Server size={18} color="#10b981" />
          </div>
          <span className="metric-val" style={{ color: '#10b981', WebkitTextFillColor: 'initial' }}>Online</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Região: sa-saopaulo-1</span>
        </div>

        <div className="metric-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span className="metric-lbl">Documentos em OCI Bucket</span>
            <Database size={18} color="#6366f1" />
          </div>
          <span className="metric-val">{stats?.total_documents || 0}</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Bucket: alura-agentes-knowledge-bucket</span>
        </div>

        <div className="metric-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span className="metric-lbl">Total de Chunks Semânticos</span>
            <Layers size={18} color="#8b5cf6" />
          </div>
          <span className="metric-val">{stats?.total_chunks || 0}</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Índice Vector RAG</span>
        </div>

        <div className="metric-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <span className="metric-lbl">Formatos de Arquivo</span>
            <Cpu size={18} color="#ec4899" />
          </div>
          <span className="metric-val">8 / 8</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>PDF, Word, Excel, PPT, MD, CSV, JSON, HTML</span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Shield size={18} color="#00758f" /> Servidores OCI Integrados
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {(ociStatus?.services_active || [
              "OCI Object Storage (Bucket de Documentos Corporativos)",
              "OCI Container Instances (Deploy da Aplicação em Nuvem)",
              "OCI Generative AI (Modelo de Inferência RAG)"
            ]).map((serv, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.88rem' }}>
                <CheckCircle size={16} color="#10b981" />
                <span>{serv}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-md)', padding: '1.5rem' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '1rem' }}>
            Cobertura por Setores Corporativos
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {Object.entries(stats?.domain_counts || {}).map(([domain, count]) => (
              <div key={domain} style={{ padding: '0.4rem 0.8rem', borderRadius: 'var(--radius-sm)', background: 'var(--bg-surface-elevated)', border: '1px solid var(--border-subtle)', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                <span style={{ fontWeight: 600 }}>{domain}:</span>
                <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>{count} doc(s)</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
