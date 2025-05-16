from abc import ABC, abstractmethod
from typing import List, Optional

from pydantic import BaseModel

{% if cookiecutter.llm_model == "mistralai/Mistral-7B-Instruct-v0.1" %}
from transformers import AutoModelForCausalLM, AutoTokenizer
{% endif %}
{% if cookiecutter.llm_model in ["gpt-3.5-turbo", "gpt-4"] %}
import openai
{% endif %}

from .retriever import Document

class Generator(ABC):
    """Abstract base class for text generators."""
    
    @abstractmethod
    def generate(self, query: str, context: List[Document]) -> str:
        """Generate a response based on the query and context."""
        pass

{% if cookiecutter.llm_model == "mistralai/Mistral-7B-Instruct-v0.1" %}
class MistralGenerator(Generator):
    """Mistral-based text generator."""
    
    def __init__(self, model_name: str = "{{ cookiecutter.llm_model }}"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16
        )
    
    def generate(self, query: str, context: List[Document]) -> str:
        # Prepare context
        context_text = "\n".join([doc.content for doc in context])
        
        # Create prompt
        prompt = f"""Context information is below.
---------------------
{context_text}
---------------------
Given the context information, please answer the question: {query}
Answer:"""
        
        # Generate response
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.7,
            top_p=0.95,
            do_sample=True
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
{% endif %}

{% if cookiecutter.llm_model in ["gpt-3.5-turbo", "gpt-4"] %}
class OpenAIGenerator(Generator):
    """OpenAI-based text generator."""
    
    def __init__(self, model_name: str = "{{ cookiecutter.llm_model }}"):
        self.model_name = model_name
    
    def generate(self, query: str, context: List[Document]) -> str:
        # Prepare context
        context_text = "\n".join([doc.content for doc in context])
        
        # Create messages
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context."
            },
            {
                "role": "user",
                "content": f"""Context information is below.
---------------------
{context_text}
---------------------
Given the context information, please answer the question: {query}"""
            }
        ]
        
        # Generate response
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=512
        )
        
        return response.choices[0].message.content
{% endif %} 