"""LLM module using Hugging Face Inference API (FREE)."""

from typing import List, Dict, Any
import os
from langchain.schema import Document
from config import settings

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    InferenceClient = None


class LLM:
    """Wrapper for Hugging Face Inference API with medical-specific prompting."""
    
    def __init__(self):
        """Initialize Hugging Face LLM."""
        if not HF_AVAILABLE:
            raise ImportError(
                "Hugging Face Hub not installed. Install with: pip install huggingface-hub"
            )
        
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")
        self.model = settings.hf_model
        
        # Initialize InferenceClient
        self.client = InferenceClient(
            model=self.model,
            token=self.api_key if self.api_key else None
        )
        
        print(f"✓ Using Hugging Face API with model: {self.model}")
        if not self.api_key:
            print("⚠️  No HUGGINGFACE_API_KEY found - using free tier (may have rate limits)")
            print("   Get a free API key at: https://huggingface.co/settings/tokens")
        
        self.system_prompt = """You are a helpful medical information assistant. Your role is to provide accurate, evidence-based medical information based on the provided context.

IMPORTANT GUIDELINES:
1. Answer ONLY based on the provided context documents
2. If the context doesn't contain enough information, say so clearly
3. Always cite your sources using [Source X] notation
4. Use clear, accessible language while maintaining medical accuracy
5. When discussing symptoms, treatments, or diagnoses, remind users to consult healthcare professionals
6. Never provide specific medical advice, diagnoses, or treatment recommendations
7. If asked about emergencies, advise immediate medical attention

For every factual statement, reference the source document using [Source 1], [Source 2], etc."""
    
    def _call_api(self, prompt: str, max_retries: int = 3) -> str:
        """Call Hugging Face Inference API."""
        for attempt in range(max_retries):
            try:
                # Use text_generation with InferenceClient
                response = self.client.text_generation(
                    prompt,
                    max_new_tokens=settings.max_tokens,
                    temperature=settings.temperature,
                    return_full_text=False
                )
                
                return response
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # Model loading
                if "loading" in error_msg or "503" in error_msg:
                    import time
                    print(f"Model loading, waiting 10s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(10)
                    continue
                
                # Rate limit
                elif "rate limit" in error_msg or "429" in error_msg:
                    print(f"Rate limited (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(5)
                        continue
                
                print(f"API Error: {e}")
                if attempt == max_retries - 1:
                    return self._fallback_response()
                    
        return self._fallback_response()
    
    def _fallback_response(self) -> str:
        """Fallback response when API fails."""
        return """I apologize, but I'm experiencing technical difficulties accessing the language model. 
        
Please try again in a moment. If the issue persists:
- Check your internet connection
- Verify the Hugging Face API is accessible
- Try a different question

For urgent medical concerns, please contact a healthcare provider immediately."""
    
    def generate_answer(
        self, 
        query: str, 
        retrieved_docs: List[Document]
    ) -> Dict[str, Any]:
        """Generate answer with citations."""
        
        # Safety check
        safety_warning = self.check_query_safety(query)
        if safety_warning:
            return {
                "answer": safety_warning,
                "sources": [],
                "warning": True
            }
        
        # Format context
        context_parts = []
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            context_parts.append(f"[Source {i}] (from {source}):\n{doc.page_content}")
        
        context = "\n\n".join(context_parts)
        
        # Build prompt
        prompt = f"""{self.system_prompt}

CONTEXT DOCUMENTS:
{context}

USER QUESTION: {query}

ASSISTANT: Based on the provided context, """
        
        # Generate answer
        answer = self._call_api(prompt)
        
        # Add medical disclaimer
        disclaimer = "\n\n⚕️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Please consult a qualified healthcare provider for medical concerns."
        
        return {
            "answer": answer + disclaimer,
            "sources": [
                {
                    "source_id": i,
                    "content": doc.page_content[:200] + "...",
                    "metadata": doc.metadata
                }
                for i, doc in enumerate(retrieved_docs, 1)
            ],
            "warning": False
        }
    
    def check_query_safety(self, query: str) -> str:
        """Check for emergency or inappropriate queries."""
        query_lower = query.lower()
        
        # Emergency keywords
        emergency_keywords = [
            "emergency", "urgent", "heart attack", "stroke", "bleeding heavily",
            "can't breathe", "unconscious", "severe pain", "suicide", "overdose",
            "choking", "seizure"
        ]
        
        if any(keyword in query_lower for keyword in emergency_keywords):
            return """🚨 **EMERGENCY ALERT** 🚨

If you or someone else is experiencing a medical emergency:
- Call emergency services immediately (911 in US, 112 in EU, or your local emergency number)
- Do not wait for online medical information
- Get immediate professional medical help

This chatbot is NOT designed for emergency situations and cannot replace emergency medical services."""
        
        # Personal medical advice
        personal_keywords = [
            "should i take", "what should i do", "am i", "do i have",
            "diagnose me", "treat my", "my symptoms"
        ]
        
        if any(keyword in query_lower for keyword in personal_keywords):
            return """⚠️ **Personal Medical Advice Warning** ⚠️

I can provide general medical information from my knowledge base, but I cannot:
- Diagnose your specific condition
- Prescribe treatments
- Give personalized medical advice

Please consult with a qualified healthcare provider who can:
- Examine you properly
- Review your medical history
- Provide appropriate diagnosis and treatment

Would you like general information about a medical topic instead?"""
        
        return ""


# Test if run directly
if __name__ == "__main__":
    llm = LLM()
    print("✓ Hugging Face LLM initialized successfully")
