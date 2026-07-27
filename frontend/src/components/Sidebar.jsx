import React, { useRef } from 'react';
import { UploadCloud, FolderKanban, FileText, CheckCircle2 } from 'lucide-react';

const DOMAIN_ICONS = {
  "Todos": "🏢",
  "Recursos Humanos": "👥",
  "Financeiro e Contábil": "💰",
  "Operacional": "⚙️",
  "Estratégico": "🎯",
  "Legal e Compliance": "⚖️",
  "Marketing e Comercial": "📈",
  "Dados e Sistemas": "💾",
  "Pesquisa e Desenvolvimento": "🧪",
  "Qualidade": "🏅",
  "Comunicação Interna": "📢"
};

export default function Sidebar({ 
  domains, 
  selectedDomain, 
  onSelectDomain, 
  stats, 
  onFileUpload, 
  uploading 
}) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <aside className="sidebar">
      <div>
        <div className="sidebar-section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <FolderKanban size={14} />
          <span>Setores Corporativos</span>
        </div>

        <div className="domain-pill-list">
          {domains.map((dom) => {
            const count = dom === "Todos" 
              ? stats?.total_documents || 0
              : stats?.domain_counts?.[dom] || 0;
            const isSelected = selectedDomain === dom;

            return (
              <button
                key={dom}
                className={`domain-item ${isSelected ? 'active' : ''}`}
                onClick={() => onSelectDomain(dom)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', overflow: 'hidden' }}>
                  <span>{DOMAIN_ICONS[dom] || "📁"}</span>
                  <span style={{ whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>{dom}</span>
                </div>
                <span className="domain-count-tag">{count}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div style={{ marginTop: 'auto' }}>
        <div className="sidebar-section-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <UploadCloud size={14} />
          <span>Ingestão de Documentos</span>
        </div>

        <input 
          type="file" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.md,.markdown,.csv,.json,.html,.htm"
          onChange={handleFileChange}
        />

        <div 
          className="upload-box"
          onClick={() => fileInputRef.current?.click()}
        >
          <UploadCloud size={28} className="upload-icon" />
          <p className="upload-text">
            {uploading ? "Sincronizando com OCI..." : "Carregar Novo Documento"}
          </p>
          <p className="upload-hint">Clique para selecionar do computador</p>
          
          <div className="format-pills-row">
            <span className="format-badge format-pdf">PDF</span>
            <span className="format-badge format-word">DOCX</span>
            <span className="format-badge format-excel">XLSX</span>
            <span className="format-badge format-ppt">PPTX</span>
            <span className="format-badge format-md">MD</span>
            <span className="format-badge format-csv">CSV</span>
            <span className="format-badge format-json">JSON</span>
            <span className="format-badge format-html">HTML</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
