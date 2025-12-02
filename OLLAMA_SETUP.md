# Ollama Setup Guide - Windows

## 📥 Step 1: Install Ollama Desktop App

1. Download Ollama for Windows:
   **https://ollama.ai/download/windows**

2. Run the installer (OllamaSetup.exe)

3. Ollama will start automatically in the background

## 🤖 Step 2: Pull Llama 3 Model

Open PowerShell and run:

```powershell
# Pull Llama 3.2 (smaller, faster - 2GB)
ollama pull llama3.2

# OR pull Llama 3 (larger, better - 4.7GB)
ollama pull llama3

# OR pull Mistral (alternative - 4.1GB)
ollama pull mistral
```

Wait for the download to complete (may take 5-15 minutes depending on model size).

## ✅ Step 3: Verify Ollama is Running

```powershell
ollama list
```

You should see the model you just pulled.

## 🚀 Step 4: Run the Medical RAG Chatbot

```powershell
cd C:\Users\hp\OneDrive\Desktop\vit\medical-rag-chatbot
python src\app_gradio.py
```

Open http://localhost:7860 and start asking medical questions!

## 🔧 Troubleshooting

**"Ollama not found"**
- Make sure you installed Ollama desktop app
- Restart PowerShell after installation

**"Connection refused"**
- Start Ollama: `ollama serve`
- Or restart the Ollama desktop app

**"Model not found"**
- Pull the model: `ollama pull llama3.2`
- Check available models: `ollama list`

**Slow responses**
- Use smaller model: `ollama pull llama3.2` (2GB instead of 4.7GB)
- Reduce max_tokens in config.py

## 📊 Model Comparison

| Model | Size | Speed | Quality | Recommendation |
|-------|------|-------|---------|----------------|
| llama3.2 | 2GB | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | **Recommended for laptops** |
| llama3 | 4.7GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | Best quality |
| mistral | 4.1GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | Good alternative |

## 🎯 Quick Commands

```powershell
# Check if Ollama is running
ollama list

# Pull a model
ollama pull llama3.2

# Test a model
ollama run llama3.2 "What is diabetes?"

# Remove a model
ollama rm llama3

# Update Ollama
# Download latest installer from ollama.ai
```

## 💡 Changing the Model

Edit `.env` file:
```
LLM_MODEL=llama3.2
```

Or set environment variable:
```powershell
$env:LLM_MODEL="mistral"
python src\app_gradio.py
```

## ✨ Benefits of Ollama

✅ **100% Free** - No API costs
✅ **Private** - All data stays on your computer
✅ **Offline** - Works without internet
✅ **Fast** - Optimized for local inference
✅ **Easy** - Simple installation and usage
✅ **Multiple Models** - Try different models easily

---

**Ready?** Download Ollama, pull llama3.2, and run the chatbot! 🚀
