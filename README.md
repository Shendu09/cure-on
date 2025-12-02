# 🏥 Medical RAG Chatbot

AI-powered medical Q&A system using **Retrieval-Augmented Generation (RAG)** with comprehensive medical knowledge base covering Cardiology, Emergency Medicine, Nephrology, Gastrology, and more.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## ✨ Features

- 🎯 **High Accuracy**: Optimized embedding model and chunking strategy for medical content
- 📚 **Citation-Backed**: Every answer includes source references from medical literature
- 🚨 **Safety First**: Emergency detection and medical disclaimers built-in
- 🆓 **100% Free**: Runs on Render free tier with Hugging Face API
- 📖 **Comprehensive**: 1.6GB medical knowledge base (9 specialty PDFs)

## 🚀 Quick Deploy (5 minutes)

### 1. Get Hugging Face API Key (FREE)
```
https://huggingface.co/settings/tokens
→ New token → Read access → Copy
```

### 2. Deploy to Render
1. Click "Deploy to Render" button above
2. Connect your GitHub repository
3. Add environment variable:
   - Key: `HUGGINGFACE_API_KEY`
   - Value: Your HF token
4. Click "Create Web Service"

**Deployment takes 15-20 minutes** (includes PDF indexing)

## 📊 Architecture

```
User Query
    ↓
Multi-QA Embeddings (Optimized for Medical Q&A)
    ↓
FAISS Vector Search (Top-7 Results)
    ↓
Mistral-7B-Instruct + Medical Context
    ↓
Answer with Citations + Disclaimer
```

## ⚙️ Optimizations

### Model Configuration
- **Embeddings**: `multi-qa-MiniLM-L6-cos-v1` (optimized for Q&A)
- **LLM**: Mistral-7B-Instruct-v0.2 (medical-grade responses)
- **Chunking**: 1500 chars with 300 overlap (better context)
- **Retrieval**: Top-7 documents (comprehensive answers)
- **Temperature**: 0.2 (balanced accuracy/naturalness)

### Memory Optimizations
- Batch processing (batch_size=8)
- No pip cache during build
- Optimized for Render's 512MB free tier

## 📁 Dataset

**9 Medical Specialties** (1.6GB total):
- Anatomy & Physiology (90MB)
- Cardiology (179MB)
- Dentistry (181MB)
- Emergency Medicine (262MB)
- Gastrology (289MB)
- General Medicine (59MB)
- Infectious Diseases (6MB)
- Internal Medicine (239MB)
- Nephrology (312MB)

## 🧪 Example Questions

- "What are the pathophysiological mechanisms of acute myocardial infarction?"
- "Explain the treatment protocol for diabetic nephropathy"
- "What are the emergency interventions for anaphylactic shock?"
- "Describe the anatomical structure of the cardiovascular system"

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/Shendu09/cure-on.git
cd cure-on

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export USE_HUGGINGFACE=true
export HUGGINGFACE_API_KEY=your_token_here

# Index documents (first time only)
python src/ingest.py

# Run chatbot
python src/app_gradio.py
```

Visit: http://localhost:7860

## 📝 API Documentation

Once deployed, visit `/docs` for interactive API documentation.

**Endpoints:**
- `POST /chat` - Submit medical question
- `GET /health` - System health check
- `GET /stats` - Usage statistics

## 🔒 Safety & Disclaimers

- ✅ Automatic emergency detection
- ✅ Personal medical advice warnings
- ✅ Source citation requirements
- ✅ Professional consultation reminders
- ✅ Medical disclaimers on all responses

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🙏 Acknowledgments

Built for **HackACure** - Medical AI Innovation Challenge

---

**Live Demo**: [Your Render URL]  
**Repository**: https://github.com/Shendu09/cure-on  
**Issues**: https://github.com/Shendu09/cure-on/issues

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
