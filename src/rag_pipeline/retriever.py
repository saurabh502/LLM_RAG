from abc import ABC, abstractmethod
from typing import List, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

class Document(BaseModel):
    """Represents a document chunk with its content and metadata."""
    content: str
    metadata: dict = {}

class Retriever(ABC):
    """Abstract base class for document retrievers."""
    
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the retriever's index."""
        pass
    
    @abstractmethod
    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve k most relevant documents for the given query."""
        pass

class FAISSRetriever(Retriever):
    """FAISS-based document retriever using sentence transformers for embeddings."""
    
    def __init__(
        self,
        embedding_model_name: str = "{{ cookiecutter.embedding_model }}",
        dimension: int = 384,  # Default for all-MiniLM-L6-v2
    ):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents: List[Document] = []
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the FAISS index."""
        if not documents:
            return
        
        # Generate embeddings for all documents
        texts = [doc.content for doc in documents]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to FAISS index
        self.index.add(np.array(embeddings).astype('float32'))
        self.documents.extend(documents)
    
    def retrieve(self, query: str, k: int = 5) -> List[Document]:
        """Retrieve k most relevant documents for the given query."""
        if not self.documents:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), k
        )
        
        # Return corresponding documents
        return [self.documents[idx] for idx in indices[0] if idx < len(self.documents)] 