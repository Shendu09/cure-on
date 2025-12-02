# 🎉 Your Medical RAG Chatbot is Ready for Render!

## ✅ What's Been Configured

Your chatbot now uses **100% FREE** cloud-ready resources:

### Architecture
```
User Query
    ↓
[Sentence Transformers] → Embeddings (runs on Render)
    ↓
[FAISS Vector Store] → Semantic Search
    ↓
[Hugging Face API] → Mistral-7B-Instruct (FREE tier)
    ↓
Answer with Citations + Medical Disclaimer
```

### Components
- ✅ **LLM**: Hugging Face Inference API (Mistral-7B-Instruct-v0.2)
- ✅ **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- ✅ **Vector Store**: FAISS (file-based, persistent)
- ✅ **Web UI**: Gradio (port 7860)
- ✅ **API**: FastAPI (port 8000)
- ✅ **Deployment**: render.yaml configured

---

## 📁 Project Structure

```
medical-rag-chatbot/
├── src/
│   ├── config.py              ← Hugging Face configuration
│   ├── llm_huggingface.py     ← NEW: HF API client
│   ├── llm_ollama.py          ← For local development
│   ├── ingest.py              ← Document processing
│   ├── retriever.py           ← FAISS semantic search
│   ├── rag.py                 ← Main RAG orchestration
│   ├── app_gradio.py          ← Web UI
│   └── app_api.py             ← REST API
├── data/
│   ├── raw/                   ← Your medical documents
│   └── vector_store/          ← FAISS index
├── requirements.txt           ← Python dependencies
├── render.yaml                ← Render deployment config
├── Dockerfile.render          ← Docker for Render
├── .env.render                ← Environment template
├── DEPLOY_GUIDE.md            ← Full deployment instructions
└── test_deployment.py         ← Pre-deployment test
```

---

## 🚀 Quick Start: Deploy to Render

### 1. Get Free Hugging Face API Key (2 minutes)
```
https://huggingface.co/settings/tokens
→ New token → Read access → Copy token (hf_...)
```

### 2. Push to GitHub (3 minutes)
```powershell
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
git init
git add .
git commit -m "Medical RAG Chatbot for Render"

# Create repo at: https://github.com/new
git remote add origin https://github.com/YOUR_USERNAME/medical-rag-chatbot.git
git push -u origin main
```

### 3. Deploy on Render (1 click)
```
https://dashboard.render.com/
→ New + → Web Service
→ Connect GitHub repo
→ Render auto-detects render.yaml
→ Add environment variable:
   HUGGINGFACE_API_KEY = hf_your_token_here
→ Create Web Service
```

### 4. Wait 10-15 minutes
- Installs sentence-transformers models
- Indexes your documents
- Launches Gradio UI

### 5. Get Your URL
```
https://medical-rag-chatbot-xxxx.onrender.com
```

---

## 🔧 Configuration

### Environment Variables (Set in Render Dashboard)

**Required:**
```bash
HUGGINGFACE_API_KEY=hf_xxxxx  # Get from huggingface.co/settings/tokens
```

**Optional (already set in render.yaml):**
```bash
USE_HUGGINGFACE=true
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.2
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
USE_LOCAL_MODELS=false
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=10000
```

### Alternative Models

Edit `HF_MODEL` in Render dashboard:

| Model | Size | Speed | Quality | Notes |
|-------|------|-------|---------|-------|
| `mistralai/Mistral-7B-Instruct-v0.2` | 7B | Medium | High | **Default** |
| `microsoft/phi-2` | 2.7B | Fast | Good | Faster responses |
| `google/flan-t5-xxl` | 11B | Medium | High | Good for Q&A |
| `meta-llama/Llama-2-7b-chat-hf` | 7B | Medium | High | Requires HF approval |

---

## 📊 Testing Locally (Optional)

### Test Hugging Face Integration
```powershell
$env:USE_HUGGINGFACE="true"
python test_deployment.py
```

### Run Locally with HF API
```powershell
$env:USE_HUGGINGFACE="true"
$env:HUGGINGFACE_API_KEY="hf_your_token"
python src\app_gradio.py
```

### Run Locally with Ollama (No HF needed)
```powershell
$env:USE_LOCAL_MODELS="true"
$env:USE_HUGGINGFACE="false"
python src\app_gradio.py
```

---

## 📁 Adding Your HackACure Dataset

### Before Deployment (Recommended)
```powershell
# Copy dataset
Copy-Item "C:\Users\hp\Downloads\HackACure-Dataset(1)\Dataset\*" `
  data\raw\

# Commit
git add data/raw/*
git commit -m "Add HackACure dataset"
git push

# Render auto-deploys and indexes
```

### After Deployment
Use Render Shell:
```bash
python src/ingest.py
```

---

## 💰 Cost Breakdown

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| Render Web Service | Free | $0 | 750 hrs/month, sleeps after 15min |
| Hugging Face API | Free | $0 | ~1000 requests/hour with token |
| Storage (FAISS) | Included | $0 | Persistent disk included |
| Bandwidth | Included | $0 | 100GB/month |

**Total: $0/month** 🎉

### Upgrade Options (Optional)
- **Render Starter**: $7/month → No sleep, always-on
- **Hugging Face Pro**: $9/month → Unlimited API requests

---

## 🐛 Troubleshooting

### "Model is loading" (503 Error)
**Normal on first request after inactivity**
- Wait 30-60 seconds
- Model cold-starts on HF servers
- Subsequent requests are fast

### Rate Limit (429 Error)
**Hit free tier limits**
- Verify `HUGGINGFACE_API_KEY` is set
- Free tier with token: ~1000 req/hr
- Without token: ~30 req/hr
- Upgrade to HF Pro for unlimited

### Render Service Sleeps
**Free tier sleeps after 15 min inactivity**
- First request wakes it (~30s delay)
- Upgrade to Starter ($7/month) for always-on

### Deployment Failed
**Check Render logs**
- Verify `requirements.txt` has `huggingface-hub`
- Check `HUGGINGFACE_API_KEY` is set correctly
- Ensure `render.yaml` is in root directory

---

## 📚 API Documentation

Once deployed, visit:
```
https://your-app.onrender.com/docs
```

### Endpoints

**POST /chat**
```json
{
  "query": "What are the symptoms of diabetes?"
}
```

Response:
```json
{
  "answer": "...",
  "sources": [...],
  "warning": false
}
```

**GET /health**
```json
{
  "status": "healthy",
  "model": "mistralai/Mistral-7B-Instruct-v0.2"
}
```

---

## 🔒 Security

- ✅ API keys stored in Render environment (not in code)
- ✅ Medical disclaimers on all responses
- ✅ Emergency detection and warnings
- ✅ Personal advice detection

---

## 📈 Next Steps

1. **Deploy**: Follow DEPLOY_GUIDE.md
2. **Test**: Ask medical questions
3. **Add Dataset**: Upload your HackACure documents
4. **Share**: Give URL to users/testers
5. **Monitor**: Check Render logs for usage

---

## 📝 Files Updated for Render

- ✅ `src/llm_huggingface.py` - NEW HF API client
- ✅ `src/config.py` - Added HF configuration
- ✅ `src/rag.py` - Auto-selects HF or Ollama
- ✅ `requirements.txt` - Added huggingface-hub
- ✅ `render.yaml` - Deployment configuration
- ✅ `Dockerfile.render` - Container config
- ✅ `.env.render` - Environment template

---

## ✅ Pre-Deployment Checklist

- [ ] Get Hugging Face API key
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Connect GitHub to Render
- [ ] Add `HUGGINGFACE_API_KEY` in Render
- [ ] Deploy and wait for build
- [ ] Test deployed URL
- [ ] Add your medical dataset
- [ ] Share with users!

---

**Ready to deploy?** See **DEPLOY_GUIDE.md** for detailed step-by-step instructions! 🚀
