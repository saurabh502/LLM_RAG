# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## 🚀 Features

- Modular and scalable RAG pipeline architecture
- Support for multiple embedding models
- Flexible LLM integration
- Multiple vector store backends
- {% if cookiecutter.include_fastapi == "yes" %}FastAPI interface for API access{% endif %}
- {% if cookiecutter.include_cli == "yes" %}Command-line interface for easy interaction{% endif %}

## 📋 Prerequisites

- Python 3.8+
- Poetry for dependency management
- {% if cookiecutter.llm_model == "mistralai/Mistral-7B-Instruct-v0.1" %}Sufficient GPU memory for running Mistral-7B{% endif %}

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/{{ cookiecutter.project_slug }}.git
cd {{ cookiecutter.project_slug }}
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🏗️ Project Structure

```
{{ cookiecutter.project_slug }}/
├── src/
│   ├── rag_pipeline/
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── pipeline.py
│   ├── data/
│   ├── config/
│   {% if cookiecutter.include_fastapi == "yes" %}
│   ├── interfaces/
│   │   └── api/
│   {% endif %}
│   {% if cookiecutter.include_cli == "yes" %}
│   ├── interfaces/
│   │   └── cli/
│   {% endif %}
├── tests/
├── pyproject.toml
├── poetry.lock
└── Makefile
```

## 🚀 Usage

### Basic Usage

```python
from src.rag_pipeline.pipeline import RAGPipeline

pipeline = RAGPipeline()
response = pipeline.query("Your question here")
print(response)
```

{% if cookiecutter.include_fastapi == "yes" %}
### API Usage

Start the FastAPI server:
```bash
make run-api
```

The API will be available at `http://localhost:8000`
{% endif %}

{% if cookiecutter.include_cli == "yes" %}
### CLI Usage

```bash
python -m src.interfaces.cli.main "Your question here"
```
{% endif %}

## 🧪 Testing

Run tests using:
```bash
make test
```

## 📝 License

This project is licensed under the {{ cookiecutter.open_source_license }} - see the LICENSE file for details.

## 👥 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request 