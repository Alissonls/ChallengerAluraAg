import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatView from './components/ChatView';
import DocumentHub from './components/DocumentHub';
import OciDashboard from './components/OciDashboard';
import SourceDrawer from './components/SourceDrawer';
import { MessageSquare, Library, Cloud } from 'lucide-react';

export default function App() {
  const [isDark, setIsDark] = useState(true);
  const [activeTab, setActiveTab] = useState('chat'); // 'chat' | 'docs' | 'oci'
  const [domains, setDomains] = useState(["Todos"]);
  const [selectedDomain, setSelectedDomain] = useState("Todos");
  const [stats, setStats] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [ociStatus, setOciStatus] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [inspectedItem, setInspectedItem] = useState(null);

  const toggleTheme = () => {
    setIsDark(!isDark);
    if (!isDark) {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.add('light');
      document.documentElement.classList.remove('dark');
    }
  };

  const fetchAppData = async () => {
    try {
      const [domRes, statsRes, docsRes, ociRes] = await Promise.all([
        fetch('/api/domains').then(r => r.json()),
        fetch('/api/stats').then(r => r.json()),
        fetch('/api/documents').then(r => r.json()),
        fetch('/api/oci/status').then(r => r.json())
      ]);

      setDomains(domRes.domains || ["Todos"]);
      setStats(statsRes);
      setDocuments(docsRes.documents || []);
      setOciStatus(ociRes);
    } catch (err) {
      console.error("Falha ao carregar dados iniciais da API:", err);
    }
  };

  useEffect(() => {
    fetchAppData();
  }, []);

  const handleFileUpload = async (file) => {
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('domain', selectedDomain);

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        await fetchAppData();
      } else {
        alert("Erro ao realizar o upload do arquivo.");
      }
    } catch (err) {
      alert("Falha de conexão durante o upload.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="app-container">
      <Header 
        isDark={isDark} 
        toggleTheme={toggleTheme} 
        userDepartment={selectedDomain}
        onChangeDepartment={setSelectedDomain}
        ociStatus={ociStatus}
        stats={stats}
      />

      <div className="main-wrapper">
        <Sidebar 
          domains={domains}
          selectedDomain={selectedDomain}
          onSelectDomain={setSelectedDomain}
          stats={stats}
          onFileUpload={handleFileUpload}
          uploading={uploading}
        />

        <main className="content-area">
          <nav className="view-tabs-header">
            <button 
              className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              <MessageSquare size={16} />
              <span>Agente de IA Conversacional</span>
            </button>

            <button 
              className={`tab-btn ${activeTab === 'docs' ? 'active' : ''}`}
              onClick={() => setActiveTab('docs')}
            >
              <Library size={16} />
              <span>Base de Documentos ({documents.length})</span>
            </button>

            <button 
              className={`tab-btn ${activeTab === 'oci' ? 'active' : ''}`}
              onClick={() => setActiveTab('oci')}
            >
              <Cloud size={16} />
              <span>Status Oracle Cloud (OCI)</span>
            </button>
          </nav>

          {activeTab === 'chat' && (
            <ChatView 
              userDepartment={selectedDomain} 
              onSelectCitation={(citation) => setInspectedItem(citation)}
            />
          )}

          {activeTab === 'docs' && (
            <DocumentHub 
              documents={documents} 
              selectedDomain={selectedDomain}
              onSelectDocument={(doc) => setInspectedItem(doc)}
            />
          )}

          {activeTab === 'oci' && (
            <OciDashboard 
              ociStatus={ociStatus} 
              stats={stats} 
            />
          )}
        </main>
      </div>

      <SourceDrawer 
        selectedItem={inspectedItem} 
        onClose={() => setInspectedItem(null)} 
      />
    </div>
  );
}

