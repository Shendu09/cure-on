# 🚀 Push to GitHub with Git LFS

## ✅ Local Repository Ready!

Your repository is committed with:
- ✅ 50 files
- ✅ 9 medical PDFs (1.6GB) tracked via Git LFS
- ✅ Complete RAG system code
- ✅ Render deployment configuration

---

## 📋 Push to GitHub (2 Steps)

### Step 1: Create GitHub Repository

Go to: **https://github.com/new**

**Settings:**
- Repository name: `medical-rag-chatbot`
- Description: `Medical RAG Chatbot with HackACure Dataset - Citation-backed medical Q&A using Hugging Face API`
- Visibility: ✅ Public (or Private if you prefer)
- ❌ Do NOT initialize with README (we already have one)
- ❌ Do NOT add .gitignore (we already have one)
- ❌ Do NOT add license (we already have one)

Click **"Create repository"**

---

### Step 2: Push Your Code

After creating the repository, run these commands:

```powershell
# Add the remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/medical-rag-chatbot.git

# Rename branch to main (GitHub standard)
git branch -M main

# Push everything (including LFS files)
git push -u origin main
```

**Note**: First push with LFS will take 5-10 minutes (uploading 1.6GB of PDFs)

---

## 📊 What Gets Pushed

### Regular Git Files (~2MB):
- Source code (`src/*.py`)
- Configuration files
- Documentation
- Deployment files

### Git LFS Files (~1.6GB):
- `Anatomy&Physiology.pdf` (90MB)
- `Cardiology.pdf` (179MB)
- `Dentistry.pdf` (181MB)
- `EmergencyMedicine.pdf` (262MB)
- `Gastrology.pdf` (289MB)
- `General.pdf` (59MB)
- `InfectiousDisease.pdf` (6MB)
- `InternalMedicine.pdf` (239MB)
- `Nephrology.pdf` (312MB)

**Git LFS Storage**: GitHub Free tier includes **1GB free LFS storage/month**
- Your PDFs: ~1.6GB (one-time storage)
- Monthly bandwidth: 1GB free (enough for several deployments)

**If you need more**: GitHub Pro ($4/month) includes 50GB LFS storage

---

## 🎯 After Pushing

### Verify LFS Files:
1. Go to your GitHub repo
2. Navigate to `data/raw/`
3. Click on a PDF file
4. You should see "Stored with Git LFS" badge

### Deploy to Render:
1. Go to https://dashboard.render.com/
2. New + → Web Service
3. Connect your GitHub repository
4. Add environment variable: `HUGGINGFACE_API_KEY`
5. Deploy!

**Render will automatically**:
- Clone your repo (including LFS files)
- Install dependencies
- Run `python src/ingest.py` to index PDFs
- Launch your chatbot

**Deployment time**: 15-20 minutes (including PDF indexing)

---

## 🔧 Troubleshooting

### "Git LFS bandwidth exceeded"
**Free tier**: 1GB/month bandwidth
**Solution**: Wait for next month, or upgrade to GitHub Pro

### Push is slow
**Normal**: Uploading 1.6GB takes time
- First push: 5-10 minutes
- Subsequent pushes: Fast (only changed files)

### "Authentication failed"
Use **Personal Access Token** instead of password:
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select: `repo` scope
4. Use token as password when pushing

---

## 📝 Commands Summary

```powershell
# In: C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot

# 1. Create repo on GitHub: https://github.com/new

# 2. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/medical-rag-chatbot.git

# 3. Push to GitHub
git branch -M main
git push -u origin main

# Wait 5-10 minutes for upload...
# ✅ Done! Your repo is live with all PDFs!
```

---

## 🎉 What's Next?

After successful push:
1. ✅ Verify files on GitHub
2. ✅ Check Git LFS files are stored correctly
3. ✅ Deploy to Render (see DEPLOY_GUIDE.md)
4. ✅ Test your chatbot with medical questions
5. ✅ Share your deployed URL!

---

**Ready to push?** Create your GitHub repo and run the commands above! 🚀
