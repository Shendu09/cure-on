"""Configuration settings for the Medical RAG Chatbot."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vector_store"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    """Application settings."""
    
    # Model configuration - Hugging Face for FREE cloud deployment
    use_huggingface: bool = os.getenv("USE_HUGGINGFACE", "true").lower() == "true"
    
    # Hugging Face API (FREE - for production deployment on Render)
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    hf_model: str = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    
    # Embeddings (using sentence-transformers - FREE)
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Legacy local models (for Ollama if needed)
    use_local_models: bool = os.getenv("USE_LOCAL_MODELS", "false").lower() == "true"
    llm_model: str = os.getenv("LLM_MODEL", "llama3")
    
    # LLM settings
    temperature: float = 0.1
    max_tokens: int = 500
    
    # Chunking
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Retrieval
    top_k: int = 5
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    gradio_port: int = 7860
    
    # Paths
    raw_data_dir: Path = RAW_DATA_DIR
    vector_store_dir: Path = VECTOR_STORE_DIR
    
    # Medical safety
    medical_disclaimer: str = (
        "⚕️ **Medical Disclaimer**: This information is for educational purposes only "
        "and is not a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult with a qualified healthcare provider for medical concerns."
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Display model info
if settings.use_huggingface:
    print(f"\n✓ Using HUGGING FACE API (FREE):")
    print(f"  - LLM: {settings.hf_model}")
    print(f"  - Embeddings: {settings.embedding_model}")
    if not settings.huggingface_api_key:
        print("  ⚠️  No API key set - using free tier (rate limited)")
        print("  Get free key at: https://huggingface.co/settings/tokens")
    print("  Perfect for Render deployment!\n")
elif settings.use_local_models:
    print(f"\n✓ Using LOCAL models (Ollama):")
    print(f"  - Embeddings: {settings.embedding_model}")
    print(f"  - LLM: {settings.llm_model}")
    print("  Models will be downloaded on first run (may take a few minutes)\n")
else:
    print("\n✓ Using API-based models\n")
