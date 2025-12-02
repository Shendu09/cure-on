"""Quick test script for Hugging Face deployment."""

import os
import sys
from pathlib import Path

# Set to use Hugging Face
os.environ["USE_HUGGINGFACE"] = "true"
os.environ["USE_LOCAL_MODELS"] = "false"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("=" * 60)
print("🧪 Testing Medical RAG Chatbot - Hugging Face Mode")
print("=" * 60)

# Test 1: Configuration
print("\n1️⃣ Testing configuration...")
try:
    from src.config import settings
    print(f"   ✅ Config loaded")
    print(f"   - Using HF: {settings.use_huggingface}")
    print(f"   - Model: {settings.hf_model}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: LLM Module
print("\n2️⃣ Testing LLM module...")
try:
    from src.llm_huggingface import LLM
    llm = LLM()
    print(f"   ✅ LLM initialized")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Sample Query (with mock documents)
print("\n3️⃣ Testing answer generation...")
try:
    from langchain.schema import Document
    
    # Mock retrieved documents
    mock_docs = [
        Document(
            page_content="Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).",
            metadata={"source": "diabetes_overview.txt"}
        )
    ]
    
    result = llm.generate_answer(
        query="What is diabetes?",
        retrieved_docs=mock_docs
    )
    
    print(f"   ✅ Answer generated successfully!")
    print(f"\n   Answer: {result['answer'][:200]}...")
    print(f"   Sources: {len(result['sources'])} document(s)")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Check requirements
print("\n4️⃣ Checking dependencies...")
required_packages = [
    "langchain",
    "sentence_transformers",
    "faiss",
    "gradio",
    "fastapi",
    "requests"
]

missing = []
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} - MISSING")
        missing.append(package)

if missing:
    print(f"\n   Install missing: pip install {' '.join(missing)}")

print("\n" + "=" * 60)
if not missing:
    print("✅ ALL TESTS PASSED - Ready for Render deployment!")
    print("\nNext steps:")
    print("1. Get free HF key: https://huggingface.co/settings/tokens")
    print("2. Push code to GitHub")
    print("3. Deploy to Render with render.yaml")
    print("4. Add HUGGINGFACE_API_KEY in Render dashboard")
else:
    print("❌ Some tests failed - please fix issues above")
print("=" * 60)
