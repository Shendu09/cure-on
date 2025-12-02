# Medical RAG Chatbot - Ollama Quick Setup
# Run this after installing Ollama desktop app

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "🤖 Medical RAG Chatbot - Ollama Setup" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check if Ollama is installed
Write-Host "Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama is installed: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama not found!" -ForegroundColor Red
    Write-Host "`nPlease install Ollama first:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://ollama.ai/download/windows" -ForegroundColor White
    Write-Host "2. Run the installer" -ForegroundColor White
    Write-Host "3. Restart PowerShell" -ForegroundColor White
    Write-Host "4. Run this script again`n" -ForegroundColor White
    exit 1
}

# Check if model is installed
Write-Host "`nChecking for Llama 3.2 model..." -ForegroundColor Yellow
$models = ollama list 2>&1
if ($models -like "*llama3.2*") {
    Write-Host "✓ Llama 3.2 is already installed" -ForegroundColor Green
} else {
    Write-Host "Llama 3.2 not found. Would you like to download it now? (2GB download)" -ForegroundColor Yellow
    Write-Host "Options:" -ForegroundColor White
    Write-Host "  1) llama3.2 (2GB, fast, recommended)" -ForegroundColor White
    Write-Host "  2) llama3 (4.7GB, better quality)" -ForegroundColor White
    Write-Host "  3) mistral (4.1GB, alternative)" -ForegroundColor White
    Write-Host "  4) Skip for now" -ForegroundColor White
    
    $choice = Read-Host "`nEnter choice (1-4)"
    
    switch ($choice) {
        "1" { 
            Write-Host "`nDownloading llama3.2 (this may take 5-10 minutes)..." -ForegroundColor Yellow
            ollama pull llama3.2
            Write-Host "✓ Llama 3.2 installed successfully!" -ForegroundColor Green
        }
        "2" { 
            Write-Host "`nDownloading llama3 (this may take 10-15 minutes)..." -ForegroundColor Yellow
            ollama pull llama3
            Write-Host "✓ Llama 3 installed successfully!" -ForegroundColor Green
        }
        "3" { 
            Write-Host "`nDownloading mistral (this may take 10-15 minutes)..." -ForegroundColor Yellow
            ollama pull mistral
            Write-Host "✓ Mistral installed successfully!" -ForegroundColor Green
        }
        "4" { 
            Write-Host "`nSkipped model download. Install manually with:" -ForegroundColor Yellow
            Write-Host "  ollama pull llama3.2" -ForegroundColor White
        }
    }
}

# Show available models
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Available Ollama Models:" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
ollama list

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Ready to launch the Medical RAG Chatbot!`n" -ForegroundColor Yellow

Write-Host "Launch options:" -ForegroundColor White
Write-Host "  1. Gradio Web UI:  python src\app_gradio.py" -ForegroundColor Gray
Write-Host "  2. FastAPI Server: python src\app_api.py" -ForegroundColor Gray
Write-Host "  3. Command Line:   python src\rag.py`n" -ForegroundColor Gray

$launch = Read-Host "Would you like to launch the Gradio UI now? (y/n)"
if ($launch -eq "y" -or $launch -eq "Y") {
    Write-Host "`nStarting Gradio UI..." -ForegroundColor Green
    Write-Host "Open http://localhost:7860 in your browser`n" -ForegroundColor Cyan
    python src\app_gradio.py
}
