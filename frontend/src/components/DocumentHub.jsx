import React, { useState } from 'react';
import { Search, FileText, Filter, CheckCircle2, HardDrive } from 'lucide-react';

const FORMAT_CLASS_MAP = {
  'PDF': 'format-pdf',
  'Word': 'format-word',
  'Excel': 'format-excel',
  'PowerPoint': 'format-ppt',
  'Markdown': 'format-md',
  'CSV': 'format-csv',
  'JSON': 'format-json',
  'HTML': 'format-html'
};

export default function DocumentHub({ documents, selectedDomain, onSelectDocument }) {
  const [searchFilter, setSearchFilter] = useState('');

  const filteredDocs = documents.filter(doc => {
    const matchesDomain = selectedDomain === "Todos" || doc.domain === selectedDomain;
    const matchesSearch = doc.filename.toLowerCase().includes(searchFilter.toLowerCase()) ||
                          doc.domain.toLowerCase().includes(searchFilter.toLowerCase()) ||
                          doc.doc_type.toLowerCase().includes(searchFilter.toLowerCase());
    return matchesDomain && matchesSearch;
  });

  return (
    <div style={{ padding: '1.75rem', overflowY: 'auto', flex: 1 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Base de Conhecimento Centralizada</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Exibindo {filteredDocs.length} de {documents.length} documentos indexados
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', background: 'var(--bg-surface)', border: '1px solid var(--border-subtle)', padding: '0.5rem 1rem', borderRadius: 'var(--radius-md)', minWidth: '280px' }}>
          <Search size={16} color="var(--text-muted)" />
          <input
            type="text"
            placeholder="Buscar por nome, formato ou setor..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            style={{ background: 'transparent', border: 'none', outline: 'none', color: 'var(--text-primary)', width: '100%', fontSize: '0.85rem' }}
          />
        </div>
      </div>

      <div className="documents-grid">
        {filteredDocs.map((doc) => {
          const badgeClass = FORMAT_CLASS_MAP[doc.doc_type] || 'format-word';
          return (
            <div 
              key={doc.doc_id} 
              className="doc-card"
              onClick={() => onSelectDocument(doc)}
            >
              <div className="doc-card-header">
                <span className={`format-badge ${badgeClass}`}>{doc.doc_type}</span>
                <span style={{ fontSize: '0.75rem', color: 'var(--accent-secondary)', fontWeight: 600 }}>
                  {doc.domain}
                </span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', margin: '0.2rem 0' }}>
                <FileText size={20} color="var(--accent-primary)" />
                <h3 className="doc-card-title">{doc.filename}</h3>
              </div>

              <div className="doc-card-meta">
                <span>{doc.word_count} palavras</span>
                <span>OCI Object Storage</span>
              </div>
            </div>
          );
        })}

        {filteredDocs.length === 0 && (
          <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '4rem', color: 'var(--text-muted)' }}>
            <HardDrive size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
            <p style={{ fontWeight: 600 }}>Nenhum documento encontrado para este filtro.</p>
          </div>
        )}
      </div>
    </div>
  );
}
