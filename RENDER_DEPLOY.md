# Medical RAG Chatbot

🏥 AI-powered medical information assistant with RAG (Retrieval-Augmented Generation)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🚀 Quick Deploy to Render (FREE)

### Step 1: Get Free Hugging Face API Key
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name it "medical-chatbot" and select "Read" access
4. Copy the token (starts with `hf_...`)

### Step 2: Deploy to Render
1. Fork this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Add environment variable:
   - Key: `HUGGINGFACE_API_KEY`
   - Value: Your HF token from Step 1
7. Click "Create Web Service"

### Step 3: Wait for Deployment
- First deployment takes 5-10 minutes (installs models)
- Your chatbot will be live at: `https://your-app-name.onrender.com`

## ⚙️ Configuration

The system uses **FREE** resources:
- **LLM**: Hugging Face Inference API (Mistral-7B-Instruct)
- **Embeddings**: sentence-transformers (runs on Render)
- **Vector Store**: FAISS (file-based, persisted)

### Environment Variables

```bash
USE_HUGGINGFACE=true  # Use Hugging Face API (default)
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.2  # Model to use
HUGGINGFACE_API_KEY=hf_xxxxx  # Your HF token
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Alternative Models (All FREE)

Edit `HF_MODEL` in Render dashboard:
- `mistralai/Mistral-7B-Instruct-v0.2` (default, best quality)
- `microsoft/phi-2` (faster, smaller)
- `google/flan-t5-xxl` (good for Q&A)
- `meta-llama/Llama-2-7b-chat-hf` (requires HF approval)

## 📁 Adding Your Dataset

### Option 1: Before Deployment
1. Add your medical documents to `data/raw/`
2. Commit and push to GitHub
3. Deploy to Render

### Option 2: After Deployment
Use Render Shell to upload:
```bash
# In Render Dashboard → Shell
cd data/raw
# Upload files via Render dashboard or API
python /opt/render/project/src/src/ingest.py
```

## 🏃 Local Development

```bash
# Clone repository
git clone <your-repo-url>
cd medical-rag-chatbot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export USE_HUGGINGFACE=true
export HUGGINGFACE_API_KEY=hf_xxxxx

# Add your medical documents
cp your-docs/* data/raw/

# Index documents
python src/ingest.py

# Run chatbot
python src/app_gradio.py
```

Visit: http://localhost:7860

## 📊 Features

✅ **RAG Pipeline**: Citation-backed answers from your medical knowledge base  
✅ **Safety Checks**: Emergency detection, personal advice warnings  
✅ **Medical Disclaimers**: Automatic healthcare provider reminders  
✅ **Source Citations**: Every answer includes document references  
✅ **Multi-format Support**: PDF, TXT, CSV, JSON, DOCX  
✅ **Free Hosting**: Runs on Render free tier

## 🔧 Architecture

```
User Query
    ↓
Semantic Search (FAISS + embeddings)
    ↓
Top-K Document Retrieval
    ↓
Context + Query → Hugging Face API
    ↓
Answer with Citations
```

## 📝 API Endpoints

- `GET /health` - Health check
- `POST /chat` - Submit medical question
- `GET /stats` - System statistics

API docs: `https://your-app.onrender.com/docs`

## 🛠️ Troubleshooting

### Model Loading Slowly
First request may take 30-60 seconds (model cold start). Subsequent requests are faster.

### Rate Limits
Free HF tier has rate limits. Solutions:
1. Get a free HF token (increases limits)
2. Use a smaller model like `microsoft/phi-2`
3. Upgrade to HF Pro ($9/month for unlimited)

### Render Sleep
Free tier sleeps after 15 min inactivity. First request wakes it up (30s delay).

## 📜 License

MIT License - see LICENSE file

## 🔐 Security Note

- Never commit API keys to GitHub
- Always use environment variables
- HF tokens are free but should be kept private

---

**Built for Render Free Tier** | **100% Free & Open Source** | **No Credit Card Required**
