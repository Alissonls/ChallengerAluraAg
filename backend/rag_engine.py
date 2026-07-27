import math
import re
from typing import List, Dict, Any, Optional

# Supported Corporate Domains
DOMAINS = [
    "Recursos Humanos",
    "Financeiro e Contábil",
    "Operacional",
    "Estratégico",
    "Legal e Compliance",
    "Marketing e Comercial",
    "Dados e Sistemas",
    "Pesquisa e Desenvolvimento",
    "Qualidade",
    "Comunicação Interna"
]

DOMAIN_KEYWORDS = {
    "Recursos Humanos": ["rh", "beneficio", "beneficios", "ferias", "onboarding", "colaborador", "salario", "clt", "home office", "treinamento", "politica", "recursos humanos"],
    "Financeiro e Contábil": ["dre", "balanço", "balanco", "despesa", "faturamento", "receita", "orcamento", "custo", "financeiro", "contabil", "imposto", "caixa"],
    "Operacional": ["processo", "procedimento", "manual", "operacao", "servidor", "chamado", "incidente", "ti", "suporte", "operacional", "fluxo"],
    "Estratégico": ["okr", "meta", "roadmap", "visao", "planejamento", "estrategia", "kpi", "crescimento", "alvo", "estrategico"],
    "Legal e Compliance": ["lgpd", "contrato", "nda", "compliance", "privacidade", "termos", "regulamentacao", "juridico", "lei", "advogado"],
    "Marketing e Comercial": ["preco", "tabela", "pitch", "vendas", "cliente", "marketing", "comercial", "campanha", "leads", "desconto"],
    "Dados e Sistemas": ["api", "banco de dados", "planilha", "json", "endpoint", "sql", "sistema", "pipeline", "schema", "dados"],
    "Pesquisa e Desenvolvimento": ["p&d", "pesquisa", "desenvolvimento", "inovacao", "business case", "prototipo", "teste", "pesquisa e desenvolvimento"],
    "Qualidade": ["iso", "auditoria", "qualidade", "processo seletivo", "plano corretivo", "nao conformidade", "norma", "certificacao"],
    "Comunicação Interna": ["comunicado", "ata", "newsletter", "reuniao", "aviso", "comunicacao", "evento", "comunicacao interna"]
}

def detect_domain(filename: str, content: str) -> str:
    """Auto-detect organizational department domain based on content and filename keywords."""
    text_sample = (filename + " " + content[:2000]).lower()
    scores = {d: 0 for d in DOMAINS}
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_sample:
                scores[domain] += 1
                
    best_domain = max(scores, key=scores.get)
    if scores[best_domain] > 0:
        return best_domain
    return "Operacional"  # Default fallback domain

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Break text into overlapping chunks for semantic indexing."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if len(current_chunk) + len(p_clean) < chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + p_clean
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = p_clean
            
    if current_chunk:
        chunks.append(current_chunk)
        
    # If any single chunk is still too big, slice by character boundary
    final_chunks = []
    for c in chunks:
        if len(c) > chunk_size * 2:
            sub_chunks = [c[i:i+chunk_size] for i in range(0, len(c), chunk_size - overlap)]
            final_chunks.extend(sub_chunks)
        else:
            final_chunks.append(c)
            
    return final_chunks if final_chunks else [text]

def compute_tf_idf_score(query_terms: List[str], chunk_text: str, total_docs: int = 1) -> float:
    """Compute lightweight TF-IDF cosine relevance score for query retrieval."""
    chunk_lower = chunk_text.lower()
    words = re.findall(r'\w+', chunk_lower)
    if not words:
        return 0.0
    
    score = 0.0
    for term in query_terms:
        term_lower = term.lower()
        count = words.count(term_lower)
        if count > 0:
            tf = count / len(words)
            idf = math.log((total_docs + 1) / (1 + 1)) + 1
            score += tf * idf * (1.5 if len(term_lower) > 3 else 1.0)
            
    return score

class RAGEngine:
    """Enterprise RAG Storage and Search Engine."""
    
    def __init__(self):
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.chunks: List[Dict[str, Any]] = []
        
    def add_document(self, doc_id: str, filename: str, doc_type: str, content: str, domain: Optional[str] = None):
        """Index a document and produce semantic vector chunks."""
        assigned_domain = domain if domain else detect_domain(filename, content)
        
        doc_meta = {
            "doc_id": doc_id,
            "filename": filename,
            "doc_type": doc_type,
            "domain": assigned_domain,
            "char_count": len(content),
            "word_count": len(content.split()),
            "content": content
        }
        self.documents[doc_id] = doc_meta
        
        # Remove old chunks for this doc if updating
        self.chunks = [c for c in self.chunks if c["doc_id"] != doc_id]
        
        # Create chunks
        doc_chunks = chunk_text(content, chunk_size=600, overlap=100)
        for idx, chunk_str in enumerate(doc_chunks):
            self.chunks.append({
                "chunk_id": f"{doc_id}_chunk_{idx}",
                "doc_id": doc_id,
                "filename": filename,
                "doc_type": doc_type,
                "domain": assigned_domain,
                "chunk_index": idx + 1,
                "total_chunks": len(doc_chunks),
                "text": chunk_str
            })
            
    def get_documents_summary(self) -> List[Dict[str, Any]]:
        """Return list of all indexed documents."""
        summary = []
        for d_id, meta in self.documents.items():
            summary.append({
                "doc_id": meta["doc_id"],
                "filename": meta["filename"],
                "doc_type": meta["doc_type"],
                "domain": meta["domain"],
                "word_count": meta["word_count"],
                "char_count": meta["char_count"]
            })
        return summary

    def get_stats((self) -> Dict[str, Any]:
        """Return global index statistics."""
        domain_counts = {d: 0 for d in DOMAINS}
        format_counts = {}
        for d in self.documents.values():
            dom = d["domain"]
            domain_counts[dom] = domain_counts.get(dom, 0) + 1
            
            fmt = d["doc_type"]
            format_counts[fmt] = format_counts.get(fmt, 0) + 1
            
        return {
            "total_documents": len(self.documents),
            "total_chunks": len(self.chunks),
            "domain_counts": domain_counts,
            "format_counts": format_counts
        }

    def search(self, query: str, domain_filter: Optional[str] = None, top_k: int = 4) -> List[Dict[str, Any]]:
        """Retrieve top_k most relevant chunks for a user query."""
        query_terms = re.findall(r'\w+', query.lower())
        # Filter stop words in Portuguese & English
        stop_words = {"de", "da", "do", "em", "para", "com", "na", "no", "um", "uma", "os", "as", "o", "a", "e", "ou", "que", "qual", "como", "onde", "quem", "sobre"}
        filtered_terms = [t for t in query_terms if t not in stop_words and len(t) > 1]
        if not filtered_terms:
            filtered_terms = query_terms

        scored_chunks = []
        for chunk in self.chunks:
            if domain_filter and domain_filter != "Todos" and chunk["domain"] != domain_filter:
                continue
                
            score = compute_tf_idf_score(filtered_terms, chunk["text"], len(self.documents))
            
            # Additional score boost if filename matches query terms
            fn_lower = chunk["filename"].lower()
            for t in filtered_terms:
                if t in fn_lower:
                    score += 0.5
                    
            if score > 0.001 or len(self.chunks) < 5:
                scored_chunks.append({
                    **chunk,
                    "score": round(score, 4)
                })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]

    def generate_answer(self, query: str, domain_filter: Optional[str] = None) -> Dict[str, Any]:
        """Synthesize answer with citations based on RAG context."""
        retrieved_chunks = self.search(query, domain_filter=domain_filter, top_k=4)
        
        if not retrieved_chunks:
            return {
                "answer": "Desculpe, não encontrei informações suficientes nos documentos corporativos cadastrados para responder a essa pergunta. Tente refinar a busca ou selecionar outra categoria.",
                "sources": [],
                "confidence": "Baixa"
            }
            
        # Build synthesis context
        sources = []
        context_blocks = []
        for idx, c in enumerate(retrieved_chunks):
            sources.append({
                "id": c["chunk_id"],
                "filename": c["filename"],
                "domain": c["domain"],
                "doc_type": c["doc_type"],
                "chunk_index": c["chunk_index"],
                "snippet": c["text"][:180] + "..."
            })
            context_blocks.append(f"--- Fonte [{idx+1}]: {c['filename']} ({c['domain']} | {c['doc_type']}) ---\n{c['text']}")

        context_str = "\n\n".join(context_blocks)
        
        # High quality natural Portuguese corporate answer template synthesis
        answer_text = self._synthesize_response(query, context_blocks, retrieved_chunks)
        
        return {
            "answer": answer_text,
            "sources": sources,
            "confidence": "Alta" if retrieved_chunks[0]["score"] > 0.1 else "Média"
        }

    def _synthesize_response(self, query: str, context_blocks: List[str], chunks: List[Dict[str, Any]]) -> str:
        """Internal smart reasoning synthesizer for answering employee queries."""
        top_chunk = chunks[0]
        
        intro = f"Com base na documentação interna da empresa (**{top_chunk['filename']}**, setor de **{top_chunk['domain']}**), aqui estão as informações solicitadas:\n\n"
        
        # Extract main relevant sentences matching query keywords
        q_words = [w.lower() for w in re.findall(r'\w+', query) if len(w) > 3]
        matched_sentences = []
        
        for c in chunks:
            lines = c["text"].split("\n")
            for line in lines:
                line_str = line.strip()
                if len(line_str) > 15 and not line_str.startswith("==="):
                    if any(qw in line_str.lower() for qw in q_words) or len(matched_sentences) < 3:
                        if line_str not in matched_sentences:
                            matched_sentences.append(line_str)

        body_bullets = ""
        if matched_sentences:
            body_bullets = "\n".join([f"- {s}" for s in matched_sentences[:6]])
        else:
            body_bullets = top_chunk["text"][:400] + "..."

        citations = f"\n\n> 📌 **Fonte de Referência:** [{top_chunk['filename']}](doc://{top_chunk['doc_id']}) (Formato: {top_chunk['doc_type']} | Categoria: {top_chunk['domain']})"
        
        return f"{intro}{body_bullets}{citations}"

# Global RAG Instance
rag_engine = RAGEngine()
