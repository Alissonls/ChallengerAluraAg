import React from 'react';
import { X, FileText, Tag, Hash, BookOpen } from 'lucide-react';

export default function SourceDrawer({ selectedItem, onClose }) {
  if (!selectedItem) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      right: 0,
      bottom: 0,
      width: '420px',
      maxWidth: '90vw',
      background: 'var(--bg-surface)',
      borderLeft: '1px solid var(--border-glow)',
      boxShadow: '-10px 0 40px rgba(0,0,0,0.5)',
      zIndex: 100,
      display: 'flex',
      flexDirection: 'column',
      padding: '1.5rem',
      overflowY: 'auto',
      animation: 'slideIn 0.25s ease-out'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <BookOpen size={20} color="var(--accent-primary)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Inspecionar Fonte RAG</h3>
        </div>
        <button 
          onClick={onClose}
          style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
        >
          <X size={20} />
        </button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ background: 'var(--bg-surface-elevated)', padding: '1rem', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>Nome do Arquivo</div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)', marginTop: '0.2rem' }}>
            {selectedItem.filename}
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
          <div style={{ background: 'var(--bg-surface-elevated)', padding: '0.85rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <Tag size={12} /> Setor
            </div>
            <div style={{ fontWeight: 600, fontSize: '0.88rem', marginTop: '0.2rem', color: 'var(--accent-secondary)' }}>
              {selectedItem.domain}
            </div>
          </div>

          <div style={{ background: 'var(--bg-surface-elevated)', padding: '0.85rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
              <FileText size={12} /> Formato
            </div>
            <div style={{ fontWeight: 600, fontSize: '0.88rem', marginTop: '0.2rem' }}>
              {selectedItem.doc_type}
            </div>
          </div>
        </div>

        {selectedItem.snippet && (
          <div style={{ marginTop: '0.5rem' }}>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              Trecho Extraído (Chunk #{selectedItem.chunk_index}):
            </div>
            <div style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.82rem',
              background: 'var(--bg-main)',
              padding: '1rem',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-subtle)',
              whiteSpace: 'pre-wrap',
              maxHeight: '300px',
              overflowY: 'auto'
            }}>
              {selectedItem.snippet}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
