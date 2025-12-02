# Medical RAG Chatbot - Project Summary

## 📋 Project Overview

**Type**: Retrieval-Augmented Generation (RAG) Medical Q&A System  
**Status**: ✅ Complete and Ready to Use  
**Location**: `C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot\`

## 🎯 What This System Does

A production-ready medical chatbot that:
- Answers medical questions with **citation-backed responses**
- Uses **RAG (Retrieval-Augmented Generation)** to ground answers in your dataset
- Provides **source references** for every claim
- Includes **medical disclaimers** and safety warnings
- Supports multiple document formats (PDF, TXT, CSV, JSON)
- Offers both **web UI** (Gradio) and **REST API** (FastAPI)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  User Query: "What are the symptoms of diabetes?"           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  RETRIEVAL PHASE                                             │
│  ┌──────────────┐                                            │
│  │ Query        │ → Embed → Search FAISS Vector Store       │
│  │ Embedding    │           (finds top-5 relevant chunks)   │
│  └──────────────┘                                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ [Retrieved Context with Sources]
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  GENERATION PHASE                                            │
│  ┌──────────────────────────────────────────┐               │
│  │  Prompt Template:                        │               │
│  │  - System: "You are a medical assistant" │               │
│  │  - Context: [Source 1] ... [Source 5]   │               │
│  │  - Query: User's question                │               │
│  └──────────────────┬───────────────────────┘               │
│                     ▼                                        │
│           OpenAI GPT-4o-mini                                │
│                     │                                        │
│                     ▼                                        │
│  ┌──────────────────────────────────────────┐               │
│  │ Answer with [Source X] citations         │               │
│  │ + Medical disclaimer                     │               │
│  │ + Safety warnings (if applicable)        │               │
│  └──────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
medical-rag-chatbot/
├── 📄 README.md                 # Comprehensive documentation
├── 📄 QUICKSTART.md             # 5-minute setup guide
├── 📄 LICENSE                   # MIT license + medical disclaimer
├── 📄 setup.ps1                 # Automated setup script (Windows)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example              # Environment template
├── 📄 .gitignore                # Git ignore rules
├── 🐳 Dockerfile                # Container definition
├── 🐳 docker-compose.yml        # Docker orchestration
│
├── 📂 src/                      # Source code
│   ├── config.py                # Configuration & settings
│   ├── ingest.py                # Document ingestion & indexing
│   ├── retriever.py             # FAISS semantic search
│   ├── llm.py                   # OpenAI LLM wrapper
│   ├── rag.py                   # Main RAG orchestration
│   ├── app_api.py               # FastAPI REST API
│   └── app_gradio.py            # Gradio web UI
│
├── 📂 data/
│   ├── raw/                     # Your medical documents (add here)
│   └── vector_store/            # FAISS index (auto-generated)
│
└── 📂 tests/
    └── test_rag.py              # Unit tests
```

## 🚀 Quick Start (3 Commands)

```powershell
# 1. Run automated setup
.\setup.ps1

# 2. Add your OpenAI key to .env
notepad .env

# 3. Run ingestion & launch UI
python src\ingest.py
python src\app_gradio.py
```

Then open http://localhost:7860 and start chatting!

## 🔑 Key Features Implemented

### 1. **Multi-Format Document Ingestion**
- ✅ PDF support (with page tracking)
- ✅ Plain text files
- ✅ CSV (auto-detects content column)
- ✅ JSON (handles nested structures)
- ✅ Sample data fallback for quick demos

### 2. **Smart Chunking**
- ✅ Recursive character splitting (1000 chars, 200 overlap)
- ✅ Preserves metadata (source, page, category)
- ✅ Configurable chunk sizes

### 3. **Vector Store (FAISS)**
- ✅ Local file-based storage
- ✅ Fast similarity search
- ✅ Persistent index
- ✅ Batch processing for large datasets

### 4. **LLM Integration**
- ✅ OpenAI GPT-4o-mini (configurable)
- ✅ Custom system prompts for medical context
- ✅ Temperature control (0.1 for accuracy)
- ✅ Token limit management

### 5. **Citation System**
- ✅ Every answer includes [Source X] references
- ✅ Source metadata (file, page, category)
- ✅ Snippet preview of source content
- ✅ Configurable top-K retrieval

### 6. **Safety Features**
- ✅ Emergency detection (chest pain, can't breathe, etc.)
- ✅ Personal advice warnings (medication, dosage)
- ✅ Medical disclaimer on every response
- ✅ Out-of-scope query handling

### 7. **User Interfaces**
- ✅ **Gradio Web UI**: Chat interface with source display
- ✅ **FastAPI REST API**: Programmatic access with OpenAPI docs
- ✅ **CLI**: Terminal-based interaction
- ✅ CORS enabled for frontend integration

### 8. **Production Ready**
- ✅ Docker support
- ✅ Health check endpoints
- ✅ Comprehensive error handling
- ✅ Environment-based configuration
- ✅ Unit tests with pytest
- ✅ Logging and monitoring hooks

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Core implementation |
| **LLM** | OpenAI GPT-4o-mini | Answer generation |
| **Embeddings** | OpenAI text-embedding-3-small | Semantic search |
| **Vector Store** | FAISS | Document indexing & retrieval |
| **Framework** | LangChain | RAG orchestration |
| **API** | FastAPI | REST endpoints |
| **UI** | Gradio | Web chat interface |
| **Container** | Docker | Deployment |
| **Testing** | pytest | Unit tests |

## 📦 Dependencies Installed

- `openai==1.54.0` - OpenAI API client
- `langchain==0.3.7` - RAG framework
- `faiss-cpu==1.8.0` - Vector similarity search
- `fastapi==0.115.4` - Web API framework
- `gradio==4.44.1` - Web UI
- `pypdf==4.3.1` - PDF processing
- `pandas==2.2.3` - CSV handling
- Plus 10+ supporting libraries

## 🔧 Configuration Options

All settings in `src/config.py` (can override via `.env`):

```python
# LLM Settings
LLM_MODEL = "gpt-4o-mini"           # or "gpt-4o", "gpt-3.5-turbo"
EMBEDDING_MODEL = "text-embedding-3-small"
TEMPERATURE = 0.1                    # Lower = more deterministic
MAX_TOKENS = 1000

# RAG Settings
CHUNK_SIZE = 1000                    # Characters per chunk
CHUNK_OVERLAP = 200                  # Overlap for context
TOP_K = 5                            # Sources to retrieve

# Server Ports
API_PORT = 8000                      # FastAPI
GRADIO_PORT = 7860                   # Gradio UI
```

## 🎨 Usage Examples

### Web UI (Gradio)
```powershell
python src\app_gradio.py
# Open http://localhost:7860
# Type: "What are the symptoms of diabetes?"
```

### REST API (FastAPI)
```powershell
python src\app_api.py
# POST to http://localhost:8000/chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is hypertension?"}'
```

### Command Line
```powershell
python src\rag.py
# Interactive: Type questions, get answers with sources
```

## 📊 Adding Your Dataset

### Step 1: Prepare Files
Place your medical documents in `data/raw/`:
```powershell
Copy-Item "C:\path\to\your\dataset\*" data\raw\
```

### Step 2: Supported Formats

**PDF**: Automatically extracts text and tracks page numbers
**TXT**: Plain text files (markdown OK)
**CSV**: Must have 'text', 'content', or 'description' column
**JSON**: List of objects with 'text'/'content' field

### Step 3: Re-Index
```powershell
python src\ingest.py
```

### Step 4: Restart App
```powershell
python src\app_gradio.py
```

## 🧪 Testing

Run all tests:
```powershell
pytest tests/ -v
```

Test individual components:
```powershell
python src\retriever.py  # Test retrieval
python src\llm.py        # Test LLM
python src\rag.py        # Test end-to-end
```

## 🐳 Docker Deployment

### Quick Docker Run
```powershell
docker build -t medical-rag-chatbot .
docker run -p 7860:7860 -p 8000:8000 --env-file .env medical-rag-chatbot
```

### Docker Compose (Recommended)
```powershell
docker-compose up
```

Access:
- Gradio: http://localhost:7860
- API: http://localhost:8000/docs

## 🔐 Security Notes

- ✅ API keys stored in `.env` (not committed to git)
- ✅ CORS enabled (configure origins for production)
- ⚠️ Add authentication for production use
- ⚠️ If handling PHI, ensure HIPAA compliance
- ⚠️ Rate limiting recommended for public APIs

## 🚀 Production Checklist

Before deploying to production:

- [ ] Replace sample data with your medical dataset
- [ ] Add authentication (JWT tokens)
- [ ] Configure CORS with specific origins
- [ ] Add rate limiting
- [ ] Set up monitoring (logs, metrics)
- [ ] Use managed vector DB (Pinecone/Weaviate) for scale
- [ ] Add Redis caching for frequent queries
- [ ] Implement audit logging
- [ ] Review medical disclaimers with legal team
- [ ] Test with real users
- [ ] Set up CI/CD pipeline

## 📈 Future Enhancements

Ideas for extending the system:

1. **Hybrid Search**: Combine keyword + semantic search
2. **Query Rewriting**: Improve retrieval with question expansion
3. **Re-ranking**: Use cross-encoder for better source selection
4. **Feedback Loop**: Collect user ratings to improve responses
5. **Fine-tuning**: Train embeddings on medical terminology
6. **Multi-language**: Support non-English queries
7. **Voice Interface**: Add speech-to-text input
8. **Admin Dashboard**: Manage documents, view analytics
9. **A/B Testing**: Compare different retrieval strategies
10. **Explainability**: Show why sources were selected

## 📚 Documentation

- **README.md**: Full documentation (architecture, API, deployment)
- **QUICKSTART.md**: 5-minute setup guide
- **This file**: Project summary and overview
- **Code comments**: Inline documentation in all modules
- **API docs**: Auto-generated at http://localhost:8000/docs

## 🆘 Troubleshooting

Common issues and solutions:

**"No OpenAI API key"**
→ Edit `.env` and add `OPENAI_API_KEY=sk-...`

**"No vector store found"**
→ Run `python src\ingest.py` first

**"Module not found"**
→ Activate venv: `.\venv\Scripts\Activate.ps1`

**"Rate limit exceeded"**
→ Reduce batch size in `ingest.py` or wait and retry

**Poor answer quality**
→ Increase `TOP_K`, use `gpt-4o`, improve dataset

## 🎓 Learning Resources

To understand RAG better:
- LangChain docs: https://python.langchain.com/
- OpenAI embeddings guide: https://platform.openai.com/docs/guides/embeddings
- FAISS wiki: https://github.com/facebookresearch/faiss/wiki
- RAG paper: https://arxiv.org/abs/2005.11401

## ✅ What's Complete

All 9 todo items completed:
1. ✅ Requirements clarified (OpenAI, FAISS, Gradio+API)
2. ✅ Dataset handling (sample data + custom support)
3. ✅ Architecture designed (RAG pipeline documented)
4. ✅ Project scaffolded (all files created)
5. ✅ Ingestion implemented (multi-format, chunking, FAISS)
6. ✅ RAG system built (retrieval + LLM + citations)
7. ✅ Testing added (safety checks, unit tests)
8. ✅ Docker configured (Dockerfile, compose, README)
9. ✅ Setup automated (setup.ps1, QUICKSTART.md)

## 🎉 Ready to Use!

Your Medical RAG Chatbot is fully built and ready to go. Just add your OpenAI API key and optionally your dataset.

**Next steps**:
1. Run `.\setup.ps1` for guided setup
2. Or follow `QUICKSTART.md` for manual setup
3. Add your dataset to `data/raw/`
4. Run `python src\ingest.py`
5. Launch `python src\app_gradio.py`

**Need help?** Review the comprehensive `README.md` or inspect the code comments.

---

Built with ❤️ for medical education and information access.

**Remember**: Always consult healthcare professionals for medical advice!
