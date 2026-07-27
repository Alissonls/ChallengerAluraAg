import os
import glob
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from parsers import parse_document
from rag_engine import rag_engine, DOMAINS
from oci_service import oci_service

app = FastAPI(
    title="Nexus AI - Agente Corporativo de Conhecimento",
    description="Agente de Inteligência Artificial Corporativo para busca em múltiplos formatos de documentos (PDF, Word, Excel, PowerPoint, Markdown, CSV, JSON, HTML) em Nuvem Oracle Cloud (OCI).",
    version="1.0.0"
)

# Enable CORS for frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQueryRequest(BaseModel):
    query: str
    domain: Optional[str] = "Todos"

@app.on_event("startup")
def load_sample_documents():
    """Generate and auto-index pre-loaded corporate sample documents."""
    try:
        from generate_samples import create_sample_files, SAMPLE_DIR
        create_sample_files()
        
        sample_files = glob.glob(os.path.join(SAMPLE_DIR, "*"))
        for file_path in sample_files:
            filename = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                content_bytes = f.read()
                
            parsed = parse_document(content_bytes, filename)
            doc_id = f"doc_{hash(filename) & 0xffffffff:08x}"
            rag_engine.add_document(
                doc_id=doc_id,
                filename=filename,
                doc_type=parsed["doc_type"],
                content=parsed["content"]
            )
            oci_service.sync_document_to_oci(filename, content_bytes)
            
        print(f"Startup complete: Indexed {len(sample_files)} corporate sample documents.")
    except Exception as e:
        print(f"Error initializing sample documents: {e}")

@app.get("/api/health")
def health_check():
    """Service health check endpoint."""
    return {"status": "ok", "app": "Nexus AI Agente Corporativo", "oci": "Connected"}

@app.get("/api/domains")
def get_domains():
    """Return available corporate department categories."""
    return {"domains": ["Todos"] + DOMAINS}

@app.get("/api/documents")
def list_documents():
    """Return list of indexed corporate documents."""
    return {"documents": rag_engine.get_documents_summary()}

@app.get("/api/stats")
def get_stats():
    """Return system & index metrics."""
    return rag_engine.get_stats()

@app.get("/api/oci/status")
def get_oci_status():
    """Return Oracle Cloud Infrastructure deployment and storage status."""
    return oci_service.get_status()

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...), domain: Optional[str] = Form(None)):
    """Upload and index a new document in PDF, DOCX, XLSX, PPTX, MD, CSV, JSON, or HTML format."""
    try:
        content_bytes = await file.read()
        filename = file.filename
        
        parsed = parse_document(content_bytes, filename)
        doc_id = f"doc_{hash(filename + str(len(content_bytes))) & 0xffffffff:08x}"
        
        rag_engine.add_document(
            doc_id=doc_id,
            filename=filename,
            doc_type=parsed["doc_type"],
            content=parsed["content"],
            domain=domain if domain and domain != "Todos" else None
        )
        
        # Sync to Oracle Cloud Object Storage
        oci_result = oci_service.sync_document_to_oci(filename, content_bytes)
        
        return {
            "success": True,
            "doc_id": doc_id,
            "filename": filename,
            "doc_type": parsed["doc_type"],
            "word_count": parsed["word_count"],
            "oci_status": oci_result["message"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento do arquivo: {str(e)}")

@app.post("/api/chat")
def chat_query(req: ChatQueryRequest):
    """Query the corporate AI agent using RAG document retrieval."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="A pergunta não pode estar vazia.")
        
    response = rag_engine.generate_answer(req.query, domain_filter=req.domain)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
