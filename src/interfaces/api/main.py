from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag_pipeline.pipeline import RAGPipeline
from src.rag_pipeline.retriever import Document

app = FastAPI(title="{{ cookiecutter.project_name }}")
pipeline = RAGPipeline()

class DocumentRequest(BaseModel):
    content: str
    metadata: dict = {}

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    response: str

@app.post("/documents")
async def add_documents(documents: List[DocumentRequest]):
    """Add documents to the RAG pipeline."""
    try:
        docs = [Document(content=doc.content, metadata=doc.metadata) for doc in documents]
        pipeline.add_documents(docs)
        return {"message": f"Successfully added {len(docs)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG pipeline."""
    try:
        response = pipeline.query(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 