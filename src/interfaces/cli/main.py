import click
import json
from pathlib import Path
from typing import List

from src.rag_pipeline.pipeline import RAGPipeline
from src.rag_pipeline.retriever import Document

@click.group()
def cli():
    """{{ cookiecutter.project_name }} CLI interface."""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def add_documents(file_path: str):
    """Add documents from a JSON file to the RAG pipeline."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Input file must contain a list of documents")
        
        documents = [
            Document(content=item['content'], metadata=item.get('metadata', {}))
            for item in data
        ]
        
        pipeline = RAGPipeline()
        pipeline.add_documents(documents)
        click.echo(f"Successfully added {len(documents)} documents")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('query')
@click.option('--top-k', default=5, help='Number of documents to retrieve')
def query(query: str, top_k: int):
    """Query the RAG pipeline."""
    try:
        pipeline = RAGPipeline()
        response = pipeline.query(query)
        click.echo(response)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli() 