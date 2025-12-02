# 🚀 Deploy Your Medical RAG Chatbot to Render (100% FREE)

## ✅ What's Been Configured

Your chatbot now uses **100% FREE resources**:
- ✅ **Hugging Face Inference API** (Mistral-7B-Instruct) - FREE tier
- ✅ **Sentence Transformers** embeddings - runs on Render for free
- ✅ **FAISS** vector store - file-based, no database needed
- ✅ **Gradio** web UI - simple, fast, no frontend coding
- ✅ **Render deployment** files - ready to deploy

## 📋 Deployment Steps (5 minutes)

### Step 1: Get Free Hugging Face API Key

1. Go to [Hugging Face Tokens](https://huggingface.co/settings/tokens)
2. Click "**New token**"
3. Name: `medical-chatbot`
4. Type: Select "**Read**" access
5. Click "**Generate**"
6. **Copy the token** (starts with `hf_...`)

### Step 2: Push Your Code to GitHub

```powershell
# Initialize git (if not already done)
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
git init
git add .
git commit -m "Medical RAG Chatbot - Ready for Render"

# Create GitHub repo and push
# Go to https://github.com/new
# Create repo named: medical-rag-chatbot
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/medical-rag-chatbot.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "**New +**" → "**Web Service**"
3. Click "**Connect GitHub**" (or use your existing connection)
4. Select your `medical-rag-chatbot` repository
5. Render will auto-detect `render.yaml` ✅
6. Click "**Apply**" to use the configuration
7. **Add Environment Variable**:
   - Click "**Environment**" tab
   - Add new variable:
     - **Key**: `HUGGINGFACE_API_KEY`
     - **Value**: Your HF token from Step 1 (paste `hf_...`)
8. Click "**Create Web Service**"

### Step 4: Wait for Deployment

- **First build**: 10-15 minutes (installs sentence-transformers models)
- **Status**: Watch the deployment logs
- **When done**: Render shows your URL: `https://medical-rag-chatbot-xxxx.onrender.com`

### Step 5: Test Your Chatbot

Visit your Render URL and ask:
- "What are the symptoms of diabetes?"
- "How is hypertension treated?"
- "What's the difference between a cold and flu?"

---

## 📁 Adding Your HackACure Dataset

### Before Deployment (Recommended)

```powershell
# Copy your dataset to the project
Copy-Item "C:\Users\hp\Downloads\HackACure-Dataset(1)\Dataset\*" `
  C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot\data\raw\

# Commit and push
git add data/raw/*
git commit -m "Add HackACure medical dataset"
git push

# Render will automatically re-index on next deployment
```

### After Deployment

Use Render Shell (in Dashboard):
```bash
# Upload files via Render web interface
# Then run in Shell:
python src/ingest.py
```

---

## ⚙️ Configuration Options

### Change LLM Model

Edit in Render Dashboard → Environment:

**Faster, smaller models:**
```
HF_MODEL=microsoft/phi-2
```

**Better quality:**
```
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.2  # Default
HF_MODEL=meta-llama/Llama-2-7b-chat-hf  # Requires HF approval
```

### Increase Rate Limits

Free HF tier limits: ~1000 requests/hour

**To increase:**
1. Use your HF API key (already done) ✅
2. Upgrade to [HF Pro](https://huggingface.co/pricing) - $9/month for unlimited

---

## 🐛 Troubleshooting

### Model Loading Slowly
**First request may take 30-60 seconds** (model cold start on HF servers)
- Subsequent requests are faster
- This is normal for free tier

### "Service Unavailable" 503 Error
Model is loading on HF servers:
- Wait 30 seconds and retry
- Usually happens after period of inactivity

### Render App Sleeps
Free tier sleeps after 15 min inactivity:
- First request wakes it up (takes ~30s)
- Keep-alive not needed for demo/testing
- For production: Upgrade to paid tier ($7/month)

### Rate Limit Errors
Hit free tier limits:
- **Solution 1**: Add `HUGGINGFACE_API_KEY` (increases limits) ✅
- **Solution 2**: Switch to smaller model (`microsoft/phi-2`)
- **Solution 3**: Upgrade to HF Pro

---

## 📊 Cost Breakdown

| Resource | Cost | Limits |
|----------|------|--------|
| **Render Web Service** | FREE | 750 hrs/month |
| **Hugging Face API** | FREE | ~1000 req/hr with token |
| **Storage (FAISS)** | FREE | Included in Render |
| **Bandwidth** | FREE | 100GB/month |

**Total: $0/month** for demo/testing! 🎉

---

## 🔄 Updates & Maintenance

### Update Dataset
```powershell
# Add new documents to data/raw/
git add data/raw/*
git commit -m "Update medical knowledge base"
git push

# Render auto-deploys and re-indexes
```

### Update Code
```powershell
# Make changes
git add .
git commit -m "Your update description"
git push

# Render auto-deploys
```

### View Logs
Go to Render Dashboard → Your Service → Logs

---

## 🎯 What's Different from Local

| Feature | Local (Ollama) | Cloud (Render + HF) |
|---------|----------------|---------------------|
| **LLM** | Llama 3 (local) | Mistral-7B (API) |
| **Startup** | Instant | 30s cold start |
| **Performance** | Fast | Depends on HF load |
| **Cost** | Free, uses GPU | Free, rate limited |
| **Deployment** | Desktop only | Public URL |

---

## 📧 Support

**Issues?**
1. Check Render logs for errors
2. Verify `HUGGINGFACE_API_KEY` is set correctly
3. Test HF API manually: https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2

**Working?** 
Share your Render URL and start helping users with medical questions! 🏥

---

**Next**: Copy the Render URL and test your chatbot with real medical questions!
