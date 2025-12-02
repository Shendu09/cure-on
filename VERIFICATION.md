# 🏥 Medical RAG Chatbot - Complete Setup Verification

## ✅ File Structure Check

Run this command to verify all files are present:

```powershell
Get-ChildItem -Recurse -Name | Sort-Object
```

Expected structure:
```
✓ .env.example
✓ .gitignore
✓ Dockerfile
✓ docker-compose.yml
✓ LICENSE
✓ PROJECT_SUMMARY.md
✓ QUICKSTART.md
✓ README.md
✓ requirements.txt
✓ setup.ps1
✓ data/raw/.gitkeep
✓ data/vector_store/.gitkeep
✓ src/__init__.py
✓ src/app_api.py
✓ src/app_gradio.py
✓ src/config.py
✓ src/ingest.py
✓ src/llm.py
✓ src/rag.py
✓ src/retriever.py
✓ tests/__init__.py
✓ tests/test_rag.py
```

## 🚀 Setup Steps (In Order)

### Step 1: Environment Setup ✓
```powershell
# Navigate to project
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot

# Option A: Automated setup (recommended)
.\setup.ps1

# Option B: Manual setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

**Verify**: Run `pip list` - should see ~25 packages

### Step 2: API Key Configuration ✓
```powershell
# Edit .env file
notepad .env

# Add your OpenAI key:
# OPENAI_API_KEY=sk-your-actual-key-here
```

**Verify**: Check `.env` contains valid API key starting with `sk-`

### Step 3: Dataset Preparation ✓
```powershell
# Option A: Use sample data (automatic, no action needed)

# Option B: Add your dataset
Copy-Item "C:\Users\hp\Downloads\HackACure-Dataset(1)\Dataset\*" data\raw\
```

**Verify**: Run `Get-ChildItem data\raw` - should show files or be empty (sample data auto-created)

### Step 4: Document Ingestion ✓
```powershell
python src\ingest.py
```

**Expected output**:
```
📂 Loading documents from: data/raw
✂️  Chunking documents...
🔢 Generating embeddings and creating vector store...
💾 Saving vector store to: data/vector_store
✅ Ingestion complete!
```

**Verify**: Check `data\vector_store\` contains `index.faiss` and `index.pkl`

### Step 5: Launch Application ✓

**Option A: Gradio Web UI** (Recommended)
```powershell
python src\app_gradio.py
```
Open http://localhost:7860

**Option B: FastAPI Server**
```powershell
python src\app_api.py
```
Open http://localhost:8000/docs

**Option C: Command Line**
```powershell
python src\rag.py
```

**Verify**: 
- Gradio: See chat interface in browser
- API: See Swagger UI docs
- CLI: Prompt appears for questions

## 🧪 Testing Checklist

### Test 1: Basic Query ✓
**Input**: "What are the symptoms of diabetes?"

**Expected**:
- Answer with medical information
- [Source X] citations in text
- Sources section with file names
- Medical disclaimer at bottom

### Test 2: Emergency Detection ✓
**Input**: "I'm having chest pain"

**Expected**:
- 🚨 EMERGENCY warning at top
- Advice to call 911 or go to ER
- Still provides general information
- Medical disclaimer

### Test 3: Personal Advice Warning ✓
**Input**: "Should I take aspirin?"

**Expected**:
- ⚠️ Warning about personal medical advice
- Recommendation to consult healthcare provider
- General information about the topic

### Test 4: Multiple Queries ✓
Try these in sequence:
1. "What is hypertension?"
2. "How is it treated?"
3. "What are risk factors?"

**Expected**: All queries work, context maintained in UI

### Test 5: API Endpoint ✓
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat `
  -H "Content-Type: application/json" `
  -d '{"query": "What is diabetes?"}'
```

**Expected**: JSON responses with status 200

## 🐳 Docker Verification (Optional)

### Build Image ✓
```powershell
docker build -t medical-rag-chatbot .
```

**Expected**: Build completes without errors

### Run Container ✓
```powershell
docker run -p 7860:7860 -p 8000:8000 --env-file .env medical-rag-chatbot
```

**Expected**: Container starts, ports accessible

### Docker Compose ✓
```powershell
docker-compose up
```

**Expected**: Service starts on both ports

## 📊 Performance Checks

### Ingestion Performance ✓
- Small dataset (<10 files): ~30-60 seconds
- Medium dataset (10-100 files): ~2-5 minutes
- Large dataset (100+ files): ~5-15 minutes

### Query Performance ✓
- Retrieval: <500ms
- LLM generation: 1-3 seconds
- Total response: <5 seconds

If slower, check:
- Network connection to OpenAI
- FAISS index size
- Increase `TOP_K` cautiously

## 🔍 Debugging Checklist

### Issue: "No OpenAI API key found"
- [ ] Check `.env` file exists
- [ ] Verify `OPENAI_API_KEY=sk-...` is present
- [ ] Key starts with `sk-`
- [ ] No extra spaces or quotes
- [ ] Restart application after adding key

### Issue: "No vector store found"
- [ ] Run `python src\ingest.py`
- [ ] Check `data\vector_store\` has files
- [ ] Verify no errors during ingestion
- [ ] Ensure virtual environment active

### Issue: "Module not found"
- [ ] Activate venv: `.\venv\Scripts\Activate.ps1`
- [ ] Reinstall: `pip install -r requirements.txt`
- [ ] Check Python version: `python --version` (3.11+)

### Issue: Poor Answer Quality
- [ ] Increase `TOP_K` in `src\config.py`
- [ ] Use better model: `LLM_MODEL=gpt-4o` in `.env`
- [ ] Check dataset relevance
- [ ] Review chunking strategy

### Issue: Port Already in Use
```powershell
# Check what's using port 7860 or 8000
netstat -ano | findstr :7860
netstat -ano | findstr :8000

# Kill process if needed (replace PID)
taskkill /PID <process_id> /F
```

## 📈 System Requirements Met

- [x] Python 3.11+ installed
- [x] 4GB+ RAM available
- [x] Internet connection (for OpenAI API)
- [x] ~500MB disk space (dependencies)
- [x] ~1GB+ disk space (vector store, varies by dataset)
- [x] Windows PowerShell 5.1+

## 🎉 Final Verification Commands

Run these to confirm everything works:

```powershell
# 1. Check Python version
python --version

# 2. Verify virtual environment
Get-Command python | Select-Object Source

# 3. Check installed packages
pip list | Select-String -Pattern "openai|langchain|faiss|gradio|fastapi"

# 4. Verify environment file
Get-Content .env | Select-String -Pattern "OPENAI_API_KEY"

# 5. Check vector store
Test-Path data\vector_store\index.faiss

# 6. Run quick test
python -c "from src.config import settings; print(f'Config loaded: {settings.llm_model}')"

# 7. Test import
python -c "from src.rag import RAGSystem; print('RAG system import OK')"
```

**All checks pass?** ✅ Your system is ready!

## 🚀 You're All Set!

### Quick Start Command:
```powershell
# Launch Gradio UI
python src\app_gradio.py
```

Then open http://localhost:7860 and ask:
> "What are the symptoms of diabetes?"

### Next Steps:
1. ✅ Test with your own medical questions
2. ✅ Add your dataset to `data/raw/` and re-ingest
3. ✅ Customize settings in `src/config.py`
4. ✅ Explore API at http://localhost:8000/docs
5. ✅ Read full docs in `README.md`

## 📞 Need Help?

Review these files in order:
1. **QUICKSTART.md** - 5-minute setup
2. **README.md** - Full documentation
3. **PROJECT_SUMMARY.md** - Architecture overview
4. Code comments - Inline explanations

---

**Congratulations!** 🎉 Your Medical RAG Chatbot is fully operational!

Remember: This is for educational purposes. Always consult healthcare professionals for medical advice.
