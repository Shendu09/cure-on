# Medical RAG Chatbot - Windows Setup Script
# Run this script to set up the entire project

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "🏥 Medical RAG Chatbot - Setup Wizard" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+ from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create .env file
Write-Host "`nSetting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
} else {
    Copy-Item .env.example .env
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "`n⚠️  IMPORTANT: Please edit .env and add your OpenAI API key!" -ForegroundColor Red
    Write-Host "   Get a key from: https://platform.openai.com/api-keys`n" -ForegroundColor Yellow
}

# Check for dataset
Write-Host "`nChecking for dataset..." -ForegroundColor Yellow
$dataFiles = Get-ChildItem -Path "data\raw" -Exclude ".gitkeep" -ErrorAction SilentlyContinue
if ($dataFiles.Count -eq 0) {
    Write-Host "ℹ️  No dataset found - sample data will be used for demo" -ForegroundColor Yellow
} else {
    Write-Host "✓ Found $($dataFiles.Count) file(s) in data/raw" -ForegroundColor Green
}

# Summary
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Next steps:`n" -ForegroundColor Yellow

Write-Host "1. Add your OpenAI API key to .env file:" -ForegroundColor White
Write-Host "   notepad .env`n" -ForegroundColor Gray

Write-Host "2. (Optional) Add your dataset to data/raw/:" -ForegroundColor White
Write-Host "   Copy-Item 'C:\path\to\your\dataset\*' data\raw\`n" -ForegroundColor Gray

Write-Host "3. Run ingestion to create the vector store:" -ForegroundColor White
Write-Host "   python src\ingest.py`n" -ForegroundColor Gray

Write-Host "4. Launch the chatbot (choose one):" -ForegroundColor White
Write-Host "   python src\app_gradio.py    # Web UI (recommended)" -ForegroundColor Gray
Write-Host "   python src\app_api.py       # API server" -ForegroundColor Gray
Write-Host "   python src\rag.py           # Command line`n" -ForegroundColor Gray

Write-Host "For detailed instructions, see QUICKSTART.md" -ForegroundColor Cyan
Write-Host "`n============================================`n" -ForegroundColor Cyan

# Ask if user wants to open .env file
$response = Read-Host "Would you like to open .env file now to add your API key? (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    notepad .env
}
