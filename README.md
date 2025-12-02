# Medical RAG Chatbot

A Retrieval-Augmented Generation (RAG) system for medical Q&A that provides accurate, explainable, and citation-backed answers.

## Features

- **RAG Pipeline**: Semantic search over medical documents + GPT-4o-mini generation
- **Citation-Backed Answers**: Every response includes source references with document IDs
- **Multiple Format Support**: PDF, TXT, CSV, JSON ingestion
- **FastAPI Backend**: RESTful API for integration
- **Gradio Web UI**: Simple chat interface for demos
- **Medical Safety**: Built-in disclaimers and fallback for out-of-scope queries
- **Docker Support**: Containerized deployment

## Architecture

```
User Query
    ↓
[Gradio UI / API Endpoint]
    ↓
[Retriever] → FAISS Vector Store (embeddings: OpenAI text-embedding-3-small)
    ↓
Top-K Relevant Chunks (with metadata: source, page, offsets)
    ↓
[LLM Prompt Builder] → Context + Query + Instructions
    ↓
[OpenAI GPT-4o-mini] → Generate Answer + Citations
    ↓
[Response Formatter] → Add sources, disclaimers
    ↓
User receives answer with citations
```

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone/navigate to project**:
   ```powershell
   cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     ```

5. **Prepare dataset** (placeholder included):
   - Place your medical documents in `data/raw/`
   - Supported formats: `.pdf`, `.txt`, `.csv`, `.json`
   - Or use the included sample dataset for testing

6. **Ingest & index documents**:
   ```powershell
   python src/ingest.py
   ```
   This creates the FAISS vector index in `data/vector_store/`

7. **Run the chatbot**:
   
   **Option A - Gradio Web UI** (recommended for demos):
   ```powershell
   python src/app_gradio.py
   ```
   Open http://localhost:7860 in your browser

   **Option B - FastAPI Server**:
   ```powershell
   python src/app_api.py
   ```
   API docs at http://localhost:8000/docs

## Usage

### Web UI (Gradio)

1. Open http://localhost:7860
2. Type your medical question
3. Get answers with citations

### API

**POST /chat**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the symptoms of diabetes?"}'
```

**Response**:
```json
{
  "answer": "Common symptoms of diabetes include...",
  "sources": [
    {
      "source": "diabetes_guide.pdf",
      "page": 3,
      "chunk_text": "Diabetes symptoms include increased thirst..."
    }
  ],
  "disclaimer": "This is for informational purposes only. Consult a healthcare professional."
}
```

## Replacing the Dataset

1. **Remove sample data**:
   ```powershell
   Remove-Item data/raw/* -Force
   ```

2. **Add your documents**:
   - Copy your medical dataset files to `data/raw/`
   - Supported: PDF, TXT, CSV (with 'text' or 'content' column), JSON

3. **Re-index**:
   ```powershell
   python src/ingest.py
   ```
   This will:
   - Parse all documents in `data/raw/`
   - Chunk text (default: 1000 chars, 200 overlap)
   - Generate embeddings (OpenAI text-embedding-3-small)
   - Build FAISS index in `data/vector_store/`

4. **Restart the app** to use the new index

## Configuration

Edit `src/config.py` to customize:

```python
# Chunking
CHUNK_SIZE = 1000          # Characters per chunk
CHUNK_OVERLAP = 200        # Overlap between chunks

# Retrieval
TOP_K = 5                  # Number of chunks to retrieve

# LLM
MODEL = "gpt-4o-mini"      # or "gpt-4o", "gpt-3.5-turbo"
TEMPERATURE = 0.1          # Lower = more deterministic

# Paths
RAW_DATA_DIR = "data/raw"
VECTOR_STORE_DIR = "data/vector_store"
```

## Docker Deployment

### Build and run:
```powershell
docker build -t medical-rag-chatbot .
docker run -p 7860:7860 -p 8000:8000 --env-file .env medical-rag-chatbot
```

### Or use docker-compose:
```powershell
docker-compose up
```

Access:
- Gradio UI: http://localhost:7860
- FastAPI: http://localhost:8000/docs

## Project Structure

```
medical-rag-chatbot/
├── data/
│   ├── raw/                    # Your medical documents
│   └── vector_store/           # FAISS index (generated)
├── src/
│   ├── config.py               # Configuration
│   ├── ingest.py               # Document ingestion & indexing
│   ├── retriever.py            # FAISS semantic search
│   ├── llm.py                  # OpenAI LLM wrapper
│   ├── rag.py                  # Main RAG orchestration
│   ├── app_gradio.py           # Gradio web UI
│   └── app_api.py              # FastAPI server
├── tests/
│   └── test_rag.py             # Unit tests
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container setup
└── README.md                   # This file
```

## Testing

Run unit tests:
```powershell
pytest tests/
```

Test a single query:
```powershell
python -c "from src.rag import RAGSystem; rag = RAGSystem(); print(rag.query('What is hypertension?'))"
```

## Evaluation

The system includes:
- **Citation coverage**: Every answer references source documents
- **Medical disclaimer**: Warns users to consult professionals
- **Fallback handling**: Responds appropriately to out-of-scope queries

To evaluate on your dataset:
1. Create a CSV with test questions and expected answers
2. Run `python tests/evaluate.py`
3. Review metrics: answer relevance, citation recall, safety

## Production Considerations

For production deployment:

1. **Security**:
   - Store API keys in secret manager (Azure Key Vault, AWS Secrets Manager)
   - Add authentication (JWT tokens)
   - Rate limiting

2. **Scalability**:
   - Use managed vector DB (Pinecone, Weaviate)
   - Add Redis caching for frequent queries
   - Load balancing with multiple replicas

3. **Monitoring**:
   - Log all queries and responses
   - Track latency, error rates
   - User feedback loop

4. **Compliance**:
   - If handling PHI, ensure HIPAA compliance
   - Add audit logging
   - Implement data retention policies

5. **RAG Improvements**:
   - Hybrid search (keyword + semantic)
   - Query rewriting
   - Re-ranking with cross-encoder
   - Fine-tune embeddings on medical domain

## Troubleshooting

**"No OpenAI API key found"**:
- Ensure `.env` exists with `OPENAI_API_KEY=sk-...`
- Restart the app after adding the key

**"No vector store found"**:
- Run `python src/ingest.py` to create the index

**Poor answer quality**:
- Increase `TOP_K` in `config.py` to retrieve more context
- Try a more powerful model (`gpt-4o` instead of `gpt-4o-mini`)
- Improve chunking strategy (adjust `CHUNK_SIZE` and `CHUNK_OVERLAP`)

**Out of memory**:
- Reduce batch size in `ingest.py`
- Use a smaller embedding model
- Process documents incrementally

## License

MIT License - see LICENSE file

## Support

For issues or questions, open a GitHub issue or contact the maintainer.

---

**Medical Disclaimer**: This chatbot is for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
