import pytest
from src.rag_pipeline.pipeline import RAGPipeline
from src.rag_pipeline.retriever import Document

def test_pipeline_initialization():
    pipeline = RAGPipeline()
    assert pipeline is not None
    assert pipeline.top_k == 5

def test_add_documents():
    pipeline = RAGPipeline()
    documents = [
        Document(content="This is a test document about AI."),
        Document(content="Another document about machine learning.")
    ]
    pipeline.add_documents(documents)
    # Note: We can't easily test the internal state of FAISS index
    # This is more of a smoke test

def test_query():
    pipeline = RAGPipeline()
    documents = [
        Document(content="Python is a programming language."),
        Document(content="Python is known for its simplicity and readability.")
    ]
    pipeline.add_documents(documents)
    
    response = pipeline.query("What is Python?")
    assert isinstance(response, str)
    assert len(response) > 0 