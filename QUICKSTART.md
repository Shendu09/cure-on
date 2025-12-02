# Medical RAG Chatbot - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the Medical RAG Chatbot running quickly.

### Step 1: Set Up Environment

Open PowerShell in the project directory:

```powershell
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
```

Create a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

### Step 2: Configure OpenAI API Key

Create a `.env` file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get a key from: https://platform.openai.com/api-keys

### Step 3: Add Your Dataset (or Use Sample Data)

**Option A: Use sample data (for quick demo)**
- Skip this step - the system will automatically create sample medical documents

**Option B: Use your actual dataset**
- Copy your medical documents to `data/raw/`
- Supported formats: `.txt`, `.pdf`, `.csv`, `.json`

Example:
```powershell
Copy-Item "C:\Users\hp\Downloads\HackACure-Dataset(1)\Dataset\*" data\raw\
```

### Step 4: Ingest & Index Documents

Run the ingestion script:

```powershell
python src/ingest.py
```

This will:
- Load documents from `data/raw/`
- Create chunks with metadata
- Generate embeddings
- Build FAISS vector index
- Save to `data/vector_store/`

Expected output:
```
📂 Loading documents from: data/raw
✂️  Chunking documents...
🔢 Generating embeddings and creating vector store...
💾 Saving vector store...
✅ Ingestion complete!
```

### Step 5: Run the Chatbot

**Option A: Web UI (Gradio) - Recommended**

```powershell
python src/app_gradio.py
```

Open http://localhost:7860 in your browser and start chatting!

**Option B: API Server (FastAPI)**

```powershell
python src/app_api.py
```

API available at http://localhost:8000
API docs at http://localhost:8000/docs

**Option C: Command Line**

```powershell
python src/rag.py
```

Type questions directly in the terminal.

### Step 6: Test It

Try these example questions:
- "What are the symptoms of diabetes?"
- "How is hypertension treated?"
- "What's the difference between a cold and the flu?"

## 📊 Verify Installation

Check that everything works:

```powershell
# Test retrieval
python src/retriever.py

# Test LLM
python src/llm.py

# Run unit tests
pytest tests/
```

## 🔄 Update Your Dataset Later

1. Add new files to `data/raw/`
2. Re-run ingestion:
   ```powershell
   python src/ingest.py
   ```
3. Restart the app

## 🐳 Docker Alternative

If you prefer Docker:

```powershell
# Build image
docker build -t medical-rag-chatbot .

# Run with docker-compose
docker-compose up
```

Access:
- Gradio: http://localhost:7860
- API: http://localhost:8000

## ❌ Troubleshooting

**"No OpenAI API key found"**
- Check that `.env` exists and contains `OPENAI_API_KEY=sk-...`
- Make sure the key starts with `sk-`

**"No vector store found"**
- Run `python src/ingest.py` first

**"Module not found"**
- Activate virtual environment: `.\venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

**Poor answers**
- Check that your dataset contains relevant medical information
- Try increasing `TOP_K` in `src/config.py`
- Use a more powerful model (change `LLM_MODEL` to `gpt-4o` in `.env`)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Review [src/config.py](src/config.py) for customization options
- Check [tests/test_rag.py](tests/test_rag.py) for testing examples
- Explore the API at http://localhost:8000/docs

## 🆘 Need Help?

Check the main README.md or review the code comments for detailed explanations.

---

**Remember**: This is for educational purposes only. Always consult healthcare professionals for medical advice!
