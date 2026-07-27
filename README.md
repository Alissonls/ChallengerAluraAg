# ⚡ Nexus AI — Agente Corporativo de Conhecimento Multi-Formato em Nuvem Oracle (OCI)

> **Desafio Alura Agentes — Edição Corporativa de IA**  
> Um agente de Inteligência Artificial corporativo acessível a todos os colaboradores, capaz de processar **8 formatos de arquivo** em **10 domínios organizacionais**, fornecendo respostas precisas com citações auditáveis em tempo real.

![Nexus AI na Oracle Cloud Infrastructure (OCI)](docs/nexus_ai_oci_dashboard.png)

---

## 📌 Visão Geral do Projeto

O **Nexus AI** foi idealizado para centralizar o conhecimento corporativo de uma empresa fictícia, eliminando silos de informação entre departamentos. Sem restrições de acesso por perfil, qualquer colaborador pode consultar dados estratégicos, financeiros, operacionais ou jurídicos de forma conversacional.

### 🌟 Diferenciais
- **Acesso Aberto & Centralizado**: Disponível a toda a empresa com interface intuitiva em modo escuro/claro (Glassmorphism).
- **Busca Semântica RAG (Retrieval-Augmented Generation)**: Respostas sintetizadas com indicação exata de fontes, trechos e arquivos.
- **Pronto para Oracle Cloud (OCI)**: Integração nativa com OCI Object Storage e OCI Container Instances.

---

## 📄 Suporte Multi-Formato (8 Formatos Integrados)

O agente compreende e extrai dados estruturados e não-estruturados dos 8 formatos mais comuns do mercado:

| Formato | Extensão | Biblioteca / Extrator | Aplicação Corporativa Exemplo |
| :--- | :--- | :--- | :--- |
| **PDF** | `.pdf` | `pypdf` | Manuais Operacionais e Business Cases |
| **Word** | `.docx`, `.doc` | `python-docx` | Políticas de RH e Contratos |
| **Excel** | `.xlsx`, `.xls` | `openpyxl` / `pandas` | Balanços Financeiros e DRE |
| **PowerPoint** | `.pptx`, `.ppt` | `python-pptx` | Apresentações de Onboarding e Treinamento |
| **Markdown** | `.md` | Raw Parser / `markdown` | Roadmaps Estratégicos e OKRs |
| **CSV** | `.csv` | `pandas` / `csv` | Tabelas de Preços e Listas Comerciais |
| **JSON** | `.json` | `json` Parser | Catálogo de APIs e Conformidade LGPD |
| **HTML** | `.html`, `.htm` | `beautifulsoup4` | Normas de Auditoria e Portais Internos |

---

## 🏢 Domínios Organizacionais Cobertos (10 Setores)

A base de conhecimento foi estruturada para atender 10 grandes áreas de negócio:
1. 👥 **Recursos Humanos**: Políticas de home office, benefícios, férias e onboarding.
2. 💰 **Financeiro e Contábil**: DRE, balanços patrimoniais, fluxo de caixa e políticas de despesas.
3. ⚙️ **Operacional**: Manual de procedimentos de TI, suporte e SLA de chamados.
4. 🎯 **Estratégico**: OKRs 2026, metas corporativas e roadmaps de expansão.
5. ⚖️ **Legal e Compliance**: Diretrizes LGPD, DPO e termos de privacidade.
6. 📈 **Marketing e Comercial**: Tabela de preços, planos corporativos e pitch decks.
7. 💾 **Dados e Sistemas**: Catálogo de APIs, endpoints e schemas de bancos de dados.
8. 🧪 **Pesquisa e Desenvolvimento**: Business cases de IA e protótipos de inovação.
9. 🏅 **Qualidade**: Processos de auditoria ISO 9001 e relatórios de causa raiz.
10. 📢 **Comunicação Interna**: Avisos gerais, reuniões de alinhamento e newsletters.

---

## ☁️ Arquitetura & Implantação na Nuvem Oracle (OCI)

O projeto utiliza o serviço **Oracle Cloud Infrastructure (OCI)** para hospedar e persistir dados:

```
                      +------------------------------------------+
                      |   Frontend (React + Vite + CSS System)   |
                      |   - Filtros por Setores Corporativos     |
                      |   - Chat Conversacional com Citações     |
                      |   - Drawer de Inspeção de Documentos     |
                      +--------------------+---------------------+
                                           |
                                     HTTP / REST API
                                           v
                      +------------------------------------------+
                      |       Backend API (Python FastAPI)       |
                      |   - Parsers de 8 Formatos de Arquivo     |
                      |   - Indexador Vector RAG (In-Memory/Vector)|
                      |   - Cliente OCI SDK (Object Storage)     |
                      +--------------------+---------------------+
                                           |
              +----------------------------+----------------------------+
              |                                                         |
              v                                                         v
  +-----------------------+                                 +-----------------------+
  |  OCI Object Storage   |                                 | OCI Container Instance|
  |  Bucket de Documentos |                                 | Execução Docker em    |
  |  (Nuvem Oracle)       |                                 | Nuvem Oracle          |
  +-----------------------+                                 +-----------------------+
```

### Serviços OCI Utilizados:
- **OCI Object Storage**: Armazenamento em nuvem para arquivos sincronizados.
- **OCI Container Instances / Compute**: Execução da aplicação conteinerizada via Docker.

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.10+
- Node.js 18+ (opcional para desenvolvimento do frontend)

### 1. Iniciar o Backend FastAPI (Porta 8000)
```bash
# Entrar na pasta backend
cd backend

# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor FastAPI
python main.py
```
O servidor estará rodando em `http://localhost:8000`. Os documentos de exemplo em todos os 8 formatos e 10 setores serão indexados automaticamente na inicialização.

### 2. Iniciar o Frontend React (Porta 5173)
```bash
# Entrar na pasta frontend
cd frontend

# Instalar dependências e rodar
npm install
npm run dev
```
Acesse a aplicação web em `http://localhost:5173`.

---

## 🐳 Implantação em Nuvem OCI via Docker

### Executar via Docker Compose
```bash
docker-compose up --build -d
```
Acesse em `http://localhost:8000`.

### Executar via Script Automático de Deploy OCI
```bash
chmod +x oci-deploy.sh
./oci-deploy.sh
```

---

## 🧪 Estrutura de Arquivos do Repositório

```
ChallengerAluraAg/
├── backend/
│   ├── main.py                  # API FastAPI (Endpoints REST & CORS)
│   ├── parsers.py               # Processador de 8 formatos de arquivos
│   ├── rag_engine.py            # Mecanismo de busca RAG & síntese IA
│   ├── oci_service.py           # Gestor de integração OCI Cloud
│   ├── generate_samples.py      # Gerador de documentos de exemplo
│   ├── requirements.txt         # Dependências Python
│   └── data/sample_docs/        # Arquivos de exemplo (8 formatos, 10 setores)
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx              # Componente principal React
│       ├── index.css            # Sistema de design (Glassmorphism / Neon)
│       └── components/          # Componentes de UI (Chat, Docs, OCI Dashboard)
├── docs/
│   └── nexus_ai_oci_dashboard.png # Imagem do agente em execução na Nuvem OCI
├── Dockerfile                   # Build multi-stage para nuvem
├── docker-compose.yml           # Orquestração do contêiner
├── oci-deploy.sh                # Script de deploy em nuvem Oracle
└── README.md                    # Documentação do projeto
```

---

## 🤝 Créditos & Licença

Desenvolvido para o **Desafio Alura Agentes** usando Python, React, FastAPI e Oracle Cloud Infrastructure.  
Licença MIT — Aberto para uso corporativo livre.
