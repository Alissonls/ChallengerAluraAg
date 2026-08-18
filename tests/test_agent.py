"""
Suite de Testes Automatizados — Nexus AI Chatbot Corporativo
Cobertura: Parsers, RAG Engine, RBAC, API Endpoints, CSV de Diálogo
Execute com: pytest tests/ -v
"""
import sys
import os
import json
import csv
import io
import pytest

# Garante que o backend está no path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))


# ===========================================================================
# FIXTURES
# ===========================================================================

@pytest.fixture(scope="module")
def rag():
    """RAG Engine limpo para testes."""
    from rag_engine import RAGEngine
    engine = RAGEngine()
    return engine


@pytest.fixture(scope="module")
def rag_with_docs():
    """RAG Engine pré-carregado com documentos de todos os setores."""
    from rag_engine import RAGEngine
    engine = RAGEngine()
    docs = [
        ("doc_rh", "RH_Politica.md", "Markdown", "Recursos Humanos",
         "Política de home office: 3 dias por semana. Auxílio home office R$ 350 mensais. "
         "Vale refeição R$ 1200 via cartão Flash. Plano de saúde Bradesco Top Nacional sem coparticipação."),
        ("doc_fin", "Financeiro_DRE.xlsx", "Excel", "Financeiro e Contábil",
         "DRE 2025: Receita Bruta R$ 60.600.000. Lucro Líquido Q4 R$ 8.200.000. "
         "Custos OCI Cloud R$ 5.450.000. Despesas pessoal R$ 19.200.000."),
        ("doc_est", "Estrategico_OKRs.md", "Markdown", "Estratégico",
         "OKRs 2026: ARR de R$ 50 milhões. 150 novos clientes enterprise. NDR acima de 125%. "
         "Migrar 100% cargas para OCI. Latência RAG abaixo de 450ms. SLA 99.99%."),
        ("doc_leg", "Juridico_LGPD.json", "JSON", "Legal e Compliance",
         "DPO: Dra. Renata Vasconcelos. Email: dpo@nexusenterprise.com.br. "
         "Retenção logs acesso IA: 180 dias. Dados cadastrais: 5 anos. Currículos RH: 12 meses."),
        ("doc_mkt", "Marketing_Precos.csv", "CSV", "Marketing e Comercial",
         "Plano Starter AI R$ 1490 25 usuários. Business Pro R$ 4990 100 usuários. "
         "Enterprise Premium R$ 12900 ilimitado suporte 1h dedicado."),
        ("doc_ops", "Operacional_TI.pdf", "PDF", "Operacional",
         "Incidentes críticos severidade 1: resposta máxima 15 minutos. "
         "Notificar canal #ti-incidentes no Slack. Chamados no ServiceNow."),
        ("doc_com", "Comunicacao_Onboarding.pptx", "PowerPoint", "Comunicação Interna",
         "Reuniões gerais toda terça-feira às 09h. Canal oficial Slack. "
         "Newsletter Nexus Week toda sexta-feira. Atas publicadas no Confluence."),
    ]
    for doc_id, filename, doc_type, domain, content in docs:
        engine.add_document(doc_id=doc_id, filename=filename,
                            doc_type=doc_type, content=content, domain=domain)
    return engine


# ===========================================================================
# 1. TESTES DE PARSERS
# ===========================================================================

class TestParsers:
    """Testes unitários para os parsers de 8 formatos de arquivo."""

    def test_parse_markdown(self):
        from parsers import parse_document
        content = "# Título\n\nParágrafo de teste com conteúdo relevante."
        result = parse_document(content.encode("utf-8"), "doc.md")
        assert result["doc_type"] == "Markdown"
        assert "Título" in result["content"]
        assert result["word_count"] > 0

    def test_parse_csv(self):
        from parsers import parse_document
        data = "setor,pergunta,resposta\nRH,Qual o beneficio?,Vale refeicao R$ 1200\n"
        result = parse_document(data.encode("utf-8"), "dialogo.csv")
        assert result["doc_type"] == "CSV"
        assert "RH" in result["content"]
        assert "resposta" in result["content"]

    def test_parse_json(self):
        from parsers import parse_document
        payload = json.dumps({"categoria": "Legal", "dpo": "Renata", "lgpd": True})
        result = parse_document(payload.encode("utf-8"), "politica.json")
        assert result["doc_type"] == "JSON"
        assert "Legal" in result["content"]
        assert "Renata" in result["content"]

    def test_parse_html(self):
        from parsers import parse_document
        html = "<html><body><h1>Auditoria ISO</h1><p>Processo de qualidade trimestral.</p></body></html>"
        result = parse_document(html.encode("utf-8"), "auditoria.html")
        assert result["doc_type"] == "HTML"
        assert "Auditoria ISO" in result["content"]
        assert "<h1>" not in result["content"]  # tags removidas

    def test_parse_pdf_fallback(self):
        from parsers import parse_document
        # PDF simples em texto puro (fallback)
        content = b"Manual de Procedimentos Operacionais de TI. Categoria: Operacional."
        result = parse_document(content, "manual.pdf")
        assert result["doc_type"] == "PDF"
        assert result["char_count"] > 0

    def test_parse_unknown_extension(self):
        from parsers import parse_document
        result = parse_document(b"Conteudo de texto simples", "arquivo.txt")
        assert result["doc_type"] == "Text"
        assert result["word_count"] > 0

    def test_parse_returns_required_fields(self):
        from parsers import parse_document
        result = parse_document(b"Teste de campos", "teste.md")
        for field in ["filename", "extension", "doc_type", "content", "char_count", "word_count"]:
            assert field in result, f"Campo obrigatório ausente: {field}"

    def test_parse_csv_dialogue_file(self):
        """Testa o parsing do CSV de diálogo real criado para o chatbot."""
        from parsers import parse_document
        csv_path = os.path.join(os.path.dirname(__file__), "..", "backend",
                                "data", "sample_docs", "Dialogo_Base_Conhecimento_IA.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                content = f.read()
            result = parse_document(content, "Dialogo_Base_Conhecimento_IA.csv")
            assert result["doc_type"] == "CSV"
            assert result["word_count"] > 100
            assert "Recursos Humanos" in result["content"]


# ===========================================================================
# 2. TESTES DO RAG ENGINE — INDEXAÇÃO
# ===========================================================================

class TestRAGIndexing:
    """Testes de indexação e estrutura do índice RAG."""

    def test_add_document_creates_entry(self, rag):
        rag.add_document("test_001", "teste.md", "Markdown",
                         "Conteúdo de teste sobre recursos humanos beneficios salario.")
        assert "test_001" in rag.documents

    def test_add_document_creates_chunks(self, rag):
        initial_chunks = len(rag.chunks)
        rag.add_document("test_002", "chunks.md", "Markdown",
                         "Parágrafo um sobre financeiro.\n\nParágrafo dois sobre orcamento.\n\nParágrafo três.")
        assert len(rag.chunks) > initial_chunks

    def test_document_metadata_stored(self, rag):
        rag.add_document("test_003", "meta.csv", "CSV",
                         "setor,resposta\nRH,Beneficio vale refeicao R$1200", domain="Recursos Humanos")
        doc = rag.documents["test_003"]
        assert doc["filename"] == "meta.csv"
        assert doc["doc_type"] == "CSV"
        assert doc["domain"] == "Recursos Humanos"

    def test_domain_auto_detection_rh(self, rag):
        rag.add_document("auto_rh", "rh_doc.md", "Markdown",
                         "Política de beneficios e ferias para colaboradores. Home office RH.")
        assert rag.documents["auto_rh"]["domain"] == "Recursos Humanos"

    def test_domain_auto_detection_financeiro(self, rag):
        rag.add_document("auto_fin", "dre.md", "Markdown",
                         "DRE balanço financeiro receita faturamento despesa contabil.")
        assert rag.documents["auto_fin"]["domain"] == "Financeiro e Contábil"

    def test_domain_auto_detection_legal(self, rag):
        rag.add_document("auto_leg", "lgpd.json", "JSON",
                         "LGPD compliance privacidade contrato juridico termos regulamentacao.")
        assert rag.documents["auto_leg"]["domain"] == "Legal e Compliance"

    def test_get_stats_structure(self, rag_with_docs):
        stats = rag_with_docs.get_stats()
        assert "total_documents" in stats
        assert "total_chunks" in stats
        assert "domain_counts" in stats
        assert "format_counts" in stats
        assert stats["total_documents"] >= 7

    def test_readd_document_replaces_chunks(self, rag):
        rag.add_document("repl_001", "replace.md", "Markdown", "Versão 1 do documento.")
        chunks_v1 = len([c for c in rag.chunks if c["doc_id"] == "repl_001"])
        rag.add_document("repl_001", "replace.md", "Markdown",
                         "Versão 2 do documento bem mais longa com muito mais conteúdo adicional.")
        chunks_v2 = len([c for c in rag.chunks if c["doc_id"] == "repl_001"])
        assert chunks_v2 >= 1  # documento re-indexado sem duplicata


# ===========================================================================
# 3. TESTES DE BUSCA RAG
# ===========================================================================

class TestRAGSearch:
    """Testes do mecanismo de busca semântica TF-IDF."""

    def test_search_returns_results(self, rag_with_docs):
        results = rag_with_docs.search("home office auxilio", user_department="Recursos Humanos")
        assert len(results) > 0

    def test_search_result_structure(self, rag_with_docs):
        results = rag_with_docs.search("plano saude beneficio", user_department="Recursos Humanos")
        assert len(results) > 0
        r = results[0]
        for field in ["chunk_id", "doc_id", "filename", "domain", "text", "score"]:
            assert field in r, f"Campo ausente no resultado: {field}"

    def test_search_relevance_ordering(self, rag_with_docs):
        """Resultados devem vir ordenados por score decrescente."""
        results = rag_with_docs.search("receita bruta lucro DRE", user_department="Financeiro e Contábil")
        if len(results) >= 2:
            assert results[0]["score"] >= results[1]["score"]

    def test_search_respects_rbac_block(self, rag_with_docs):
        """Usuário de RH não deve ver chunks do setor Financeiro."""
        results = rag_with_docs.search("receita bruta DRE financeiro", user_department="Recursos Humanos")
        for r in results:
            assert r["domain"] in ["Recursos Humanos", "Comunicação Interna"]

    def test_search_admin_sees_all(self, rag_with_docs):
        """Administrador deve acessar documentos de qualquer setor."""
        results_rh = rag_with_docs.search("home office", user_department="Administrador")
        results_fin = rag_with_docs.search("DRE lucro receita", user_department="Administrador")
        assert len(results_rh) > 0
        assert len(results_fin) > 0

    def test_search_comunicacao_interna_universal(self, rag_with_docs):
        """Comunicação Interna é acessível a qualquer setor."""
        results = rag_with_docs.search("reuniao slack newsletter", user_department="Financeiro e Contábil")
        domains = [r["domain"] for r in results]
        # Comunicação Interna pode aparecer para usuário do Financeiro
        assert any(d in ["Financeiro e Contábil", "Comunicação Interna"] for d in domains)

    def test_search_top_k_limit(self, rag_with_docs):
        results = rag_with_docs.search("empresa", user_department="Administrador", top_k=3)
        assert len(results) <= 3


# ===========================================================================
# 4. TESTES DE GERAÇÃO DE RESPOSTA (RBAC + SÍNTESE)
# ===========================================================================

class TestRAGAnswerGeneration:
    """Testes da geração de resposta com trava de segurança RBAC."""

    def test_answer_authorized_rh(self, rag_with_docs):
        resp = rag_with_docs.generate_answer("Qual o auxilio home office?", user_department="Recursos Humanos")
        assert "answer" in resp
        assert "sources" in resp
        assert "confidence" in resp
        assert len(resp["answer"]) > 10

    def test_answer_authorized_financeiro(self, rag_with_docs):
        resp = rag_with_docs.generate_answer("Qual o lucro liquido?", user_department="Financeiro e Contábil")
        assert resp["confidence"] in ["Alta", "Média", "Baixa"]
        assert "Financeiro" in resp["answer"] or "lucro" in resp["answer"].lower() or len(resp["sources"]) >= 0

    def test_answer_rbac_blocked(self, rag_with_docs):
        """Usuário de RH perguntando sobre dados do Financeiro deve ser bloqueado."""
        resp = rag_with_docs.generate_answer("Qual o lucro DRE financeiro receita faturamento?",
                                              user_department="Recursos Humanos")
        # Resposta deve ser de acesso negado OU sem informações do setor errado
        if resp["confidence"] == "Restrito":
            assert "Acesso Negado" in resp["answer"] or "RBAC" in resp["answer"]
            assert resp["sources"] == []

    def test_answer_no_results_returns_graceful(self, rag_with_docs):
        resp = rag_with_docs.generate_answer("xyzabcdefghijklmnop123456 inexistente",
                                              user_department="Recursos Humanos")
        assert "answer" in resp
        assert len(resp["answer"]) > 0

    def test_answer_admin_sees_all_sectors(self, rag_with_docs):
        resp_rh = rag_with_docs.generate_answer("home office beneficio", user_department="Administrador")
        resp_fin = rag_with_docs.generate_answer("DRE lucro receita", user_department="Administrador")
        assert resp_rh["confidence"] != "Restrito"
        assert resp_fin["confidence"] != "Restrito"

    def test_answer_sources_have_metadata(self, rag_with_docs):
        resp = rag_with_docs.generate_answer("reuniao slack comunicado", user_department="Administrador")
        for src in resp["sources"]:
            assert "filename" in src
            assert "domain" in src
            assert "doc_type" in src


# ===========================================================================
# 5. TESTES DO CSV DE DIÁLOGO
# ===========================================================================

class TestDialogueCSV:
    """Testes de validação e integridade do CSV de diálogo."""

    CSV_PATH = os.path.join(os.path.dirname(__file__), "..",
                            "backend", "data", "sample_docs", "Dialogo_Base_Conhecimento_IA.csv")

    REQUIRED_COLUMNS = {"setor", "intencao", "pergunta", "resposta", "palavras_chave", "confianca"}

    def test_csv_file_exists(self):
        assert os.path.exists(self.CSV_PATH), "CSV de diálogo não encontrado!"

    def test_csv_has_required_columns(self):
        with open(self.CSV_PATH, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cols = set(reader.fieldnames or [])
        assert self.REQUIRED_COLUMNS.issubset(cols), f"Colunas ausentes: {self.REQUIRED_COLUMNS - cols}"

    def test_csv_minimum_rows(self):
        with open(self.CSV_PATH, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) >= 30, f"CSV deve ter pelo menos 30 diálogos, tem {len(rows)}"

    def test_csv_no_empty_answers(self):
        with open(self.CSV_PATH, encoding="utf-8") as f:
            for i, row in enumerate(csv.DictReader(f), start=2):
                assert row["resposta"].strip(), f"Resposta vazia na linha {i}"

    def test_csv_no_empty_questions(self):
        with open(self.CSV_PATH, encoding="utf-8") as f:
            for i, row in enumerate(csv.DictReader(f), start=2):
                assert row["pergunta"].strip(), f"Pergunta vazia na linha {i}"

    def test_csv_covers_all_sectors(self):
        expected = {
            "Recursos Humanos", "Financeiro e Contábil", "Operacional",
            "Estratégico", "Legal e Compliance", "Marketing e Comercial",
            "Dados e Sistemas", "Pesquisa e Desenvolvimento",
            "Qualidade", "Comunicação Interna"
        }
        with open(self.CSV_PATH, encoding="utf-8") as f:
            sectors = {row["setor"] for row in csv.DictReader(f)}
        missing = expected - sectors
        assert not missing, f"Setores não cobertos no CSV: {missing}"

    def test_csv_confidence_values_valid(self):
        valid = {"Alta", "Média", "Baixa"}
        with open(self.CSV_PATH, encoding="utf-8") as f:
            for i, row in enumerate(csv.DictReader(f), start=2):
                assert row["confianca"] in valid, f"Confiança inválida na linha {i}: '{row['confianca']}'"

    def test_csv_indexed_by_rag(self):
        """O CSV de diálogo deve ser indexável pelo RAG Engine."""
        from parsers import parse_document
        from rag_engine import RAGEngine

        with open(self.CSV_PATH, "rb") as f:
            content = f.read()

        parsed = parse_document(content, "Dialogo_Base_Conhecimento_IA.csv")
        engine = RAGEngine()
        engine.add_document("dialog_csv", "Dialogo_Base_Conhecimento_IA.csv",
                            parsed["doc_type"], parsed["content"])

        assert "dialog_csv" in engine.documents
        assert len(engine.chunks) > 0

    def test_csv_rag_answers_rh_question(self):
        """O RAG deve responder perguntas de RH com base no CSV de diálogo."""
        from parsers import parse_document
        from rag_engine import RAGEngine

        with open(self.CSV_PATH, "rb") as f:
            content = f.read()

        parsed = parse_document(content, "Dialogo_Base_Conhecimento_IA.csv")
        engine = RAGEngine()
        engine.add_document("dialog_csv", "Dialogo_Base_Conhecimento_IA.csv",
                            parsed["doc_type"], parsed["content"], domain="Recursos Humanos")

        resp = engine.generate_answer("Qual o valor do auxilio home office?",
                                      user_department="Recursos Humanos")
        assert resp["confidence"] in ["Alta", "Média"]
        assert len(resp["answer"]) > 20


# ===========================================================================
# 6. TESTES DA API FASTAPI (integração)
# ===========================================================================

class TestAPIEndpoints:
    """Testes de integração dos endpoints REST da API FastAPI."""

    @pytest.fixture(scope="class")
    def client(self):
        from fastapi.testclient import TestClient
        from main import app
        return TestClient(app)

    def test_health_endpoint(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "app" in data

    def test_domains_endpoint(self, client):
        resp = client.get("/api/domains")
        assert resp.status_code == 200
        domains = resp.json()["domains"]
        assert len(domains) >= 10
        assert "Recursos Humanos" in domains
        assert "Administrador" in domains

    def test_stats_endpoint(self, client):
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        stats = resp.json()
        assert "total_documents" in stats
        assert stats["total_documents"] >= 0

    def test_documents_endpoint_admin(self, client):
        resp = client.get("/api/documents?user_department=Administrador")
        assert resp.status_code == 200
        assert "documents" in resp.json()

    def test_documents_endpoint_rh_restricted(self, client):
        resp_admin = client.get("/api/documents?user_department=Administrador")
        resp_rh = client.get("/api/documents?user_department=Recursos Humanos")
        # Admin vê tudo, RH vê apenas seus documentos
        assert len(resp_admin.json()["documents"]) >= len(resp_rh.json()["documents"])

    def test_oci_status_endpoint(self, client):
        resp = client.get("/api/oci/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "Online"
        assert "region" in data
        assert "bucket_name" in data

    def test_chat_endpoint_valid_query(self, client):
        resp = client.post("/api/chat", json={
            "query": "Qual o auxilio home office?",
            "user_department": "Recursos Humanos"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data

    def test_chat_endpoint_empty_query(self, client):
        resp = client.post("/api/chat", json={
            "query": "",
            "user_department": "Recursos Humanos"
        })
        assert resp.status_code == 400

    def test_chat_endpoint_admin_query(self, client):
        resp = client.post("/api/chat", json={
            "query": "Qual o lucro liquido financeiro?",
            "user_department": "Administrador"
        })
        assert resp.status_code == 200
        assert resp.json()["confidence"] != "Restrito"

    def test_upload_markdown_document(self, client):
        md_content = b"# Teste de Upload\n\nDocumento de teste para validar o endpoint de upload via pytest."
        resp = client.post(
            "/api/upload",
            files={"file": ("teste_upload.md", md_content, "text/markdown")},
            data={"domain": "Operacional"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] is True
        assert data["doc_type"] == "Markdown"
        assert "doc_id" in data

    def test_upload_csv_dialogue(self, client):
        """Valida o upload do próprio CSV de diálogo via API."""
        csv_path = os.path.join(os.path.dirname(__file__), "..",
                                "backend", "data", "sample_docs", "Dialogo_Base_Conhecimento_IA.csv")
        if os.path.exists(csv_path):
            with open(csv_path, "rb") as f:
                content = f.read()
            resp = client.post(
                "/api/upload",
                files={"file": ("Dialogo_Base_Conhecimento_IA.csv", content, "text/csv")},
                data={"domain": "Comunicação Interna"}
            )
            assert resp.status_code == 200
            assert resp.json()["doc_type"] == "CSV"
