# Deploying Medical RAG Chatbot to Render

## 🚀 Quick Deploy (3 Steps)

### Prerequisites
- GitHub account
- Render account (free at https://render.com)
- Your code pushed to GitHub

---

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
git init

# Create .gitignore
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore

# Add and commit
git add .
git commit -m "Initial commit: Medical RAG Chatbot"

# Create GitHub repo and push
# (Create repo at github.com/new first, then:)
git remote add origin https://github.com/YOUR_USERNAME/medical-rag-chatbot.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Blueprint"**
3. **Connect your GitHub repository**
4. **Render will auto-detect `render.yaml`** and configure everything
5. **Click "Apply"** to deploy

### Option B: Manual Setup

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name**: `medical-rag-chatbot`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `bash start.sh`
   - **Plan**: `Starter` (Free)

5. **Add Environment Variables:**
   - `PYTHON_VERSION` = `3.11.0`
   - `USE_LOCAL_MODELS` = `true`
   - `GRADIO_SERVER_NAME` = `0.0.0.0`

6. **Add Disk (for persistent vector store):**
   - **Name**: `vector-store`
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: `1 GB`

7. **Click "Create Web Service"**

---

## Step 3: Wait for Deployment

Render will:
1. ✅ Clone your repository
2. ✅ Run `build.sh` (install dependencies, download models)
3. ✅ Run `start.sh` (create vector store, launch Gradio)
4. ✅ Provide you with a live URL: `https://your-app-name.onrender.com`

**First deployment takes 5-10 minutes** (downloading models)

---

## 📊 After Deployment

### Your Live App
- **URL**: `https://medical-rag-chatbot-XXXX.onrender.com`
- **Status**: Check at Render dashboard
- **Logs**: Available in Render dashboard

### Add Your Real Dataset

1. **SSH into Render** (or use Render Shell):
   ```bash
   # Upload your dataset files
   # Option 1: Use Render's file upload in dashboard
   # Option 2: Store in GitHub and pull during build
   ```

2. **Re-index**:
   - Render will auto-restart and run `start.sh`
   - This will detect new files and re-index

---

## ⚠️ Important Notes for Render

### Free Tier Limitations
- ❌ **No Ollama support** (Ollama requires persistent background process)
- ✅ **Solution**: Use OpenAI API instead on Render
- **Free tier**: Service spins down after 15 min of inactivity
- **Disk**: 1GB persistent storage included

### Switching to OpenAI for Production

Since Render free tier doesn't support Ollama, update `.env` for deployment:

```bash
# In Render Environment Variables (or .env)
USE_LOCAL_MODELS=false
OPENAI_API_KEY=your-api-key-here
```

Or keep local models for dev, OpenAI for production:
- Local development: Use Ollama (free, unlimited)
- Render deployment: Use OpenAI API (pay-per-use, $0.001 per request)

---

## 🔧 Troubleshooting

### Issue: Service won't start
- **Check Logs** in Render dashboard
- Common fixes:
  - Ensure `build.sh` and `start.sh` have execution permissions
  - Check Python version compatibility
  - Verify all requirements install successfully

### Issue: Out of memory
- **Upgrade plan** to higher tier
- Or reduce model size (use smaller embedding model)

### Issue: Slow first request
- **Normal!** Free tier spins down after inactivity
- **Upgrade** to paid plan for always-on service

---

## 💡 Alternative: Deploy with OpenAI

If you want to use the free Render tier, I can help you switch back to OpenAI:

```bash
# Update src/config.py
USE_LOCAL_MODELS=false

# Add to Render env vars
OPENAI_API_KEY=sk-your-key-here
```

This will work perfectly on Render's free tier!

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Gradio on Render**: https://gradio.app/guides/sharing-your-app/#deploying-to-render
- **Logs**: Check Render dashboard for detailed errors
