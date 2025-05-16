from typing import List, Optional

from .retriever import Document, Retriever, FAISSRetriever
from .generator import Generator
{% if cookiecutter.llm_model == "mistralai/Mistral-7B-Instruct-v0.1" %}
from .generator import MistralGenerator
{% endif %}
{% if cookiecutter.llm_model in ["gpt-3.5-turbo", "gpt-4"] %}
from .generator import OpenAIGenerator
{% endif %}

class RAGPipeline:
    """End-to-end RAG pipeline that combines retrieval and generation."""
    
    def __init__(
        self,
        retriever: Optional[Retriever] = None,
        generator: Optional[Generator] = None,
        top_k: int = 5
    ):
        self.retriever = retriever or FAISSRetriever()
        self.generator = generator or (
            {% if cookiecutter.llm_model == "mistralai/Mistral-7B-Instruct-v0.1" %}
            MistralGenerator()
            {% endif %}
            {% if cookiecutter.llm_model in ["gpt-3.5-turbo", "gpt-4"] %}
            OpenAIGenerator()
            {% endif %}
        )
        self.top_k = top_k
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the retriever's index."""
        self.retriever.add_documents(documents)
    
    def query(self, query: str) -> str:
        """Process a query through the RAG pipeline."""
        # Retrieve relevant documents
        context = self.retriever.retrieve(query, k=self.top_k)
        
        # Generate response
        response = self.generator.generate(query, context)
        
        return response 