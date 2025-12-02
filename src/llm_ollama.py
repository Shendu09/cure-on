"""LLM module using Ollama for local models."""

from typing import List, Dict, Any
from langchain.schema import Document
from config import settings

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


class LLM:
    """Wrapper for Ollama local LLM with medical-specific prompting."""
    
    def __init__(self):
        """Initialize Ollama LLM."""
        if not OLLAMA_AVAILABLE:
            raise ImportError(
                "Ollama not installed. Install with: pip install ollama\n"
                "Also install Ollama desktop app from: https://ollama.ai"
            )
        
        self.model = settings.llm_model
        print(f"✓ Using Ollama with model: {self.model}")
        print("  Make sure Ollama is running and the model is pulled:")
        print(f"  ollama pull {self.model}")
        
        # Test connection
        try:
            ollama.list()
            print("✓ Ollama is running")
        except Exception as e:
            print(f"⚠️  Ollama may not be running. Start it with: ollama serve")
            print(f"   Error: {e}")
        
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
    
    def generate_answer(
        self,
        query: str,
        context_docs: List[Document],
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """Generate an answer with citations based on retrieved context."""
        
        # Format context with source markers
        context_parts = []
        for idx, doc in enumerate(context_docs, start=1):
            source_info = f"[Source {idx}: {doc.metadata.get('source', 'Unknown')}"
            if 'page' in doc.metadata:
                source_info += f", Page {doc.metadata['page']}"
            source_info += "]"
            
            context_parts.append(f"{source_info}\n{doc.page_content}\n")
        
        context = "\n".join(context_parts)
        
        # Build prompt
        user_message = f"""Context documents:
{context}

User question: {query}

Please provide a comprehensive answer based on the context above. Remember to cite sources using [Source X] notation for each factual claim."""
        
        # Generate response using Ollama
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': user_message}
                ],
                options={
                    'temperature': settings.temperature,
                    'num_predict': settings.max_tokens,
                }
            )
            
            answer = response['message']['content']
            
        except Exception as e:
            # Fallback to simple context-based answer
            answer = f"⚠️ Ollama error: {e}\n\n"
            answer += "Based on the available information:\n\n"
            for idx, doc in enumerate(context_docs, start=1):
                content = doc.page_content.strip()
                preview = content.split('\n\n')[0] if '\n\n' in content else content[:300]
                answer += f"{preview} [Source {idx}]\n\n"
        
        # Format sources
        sources = []
        if include_sources:
            for idx, doc in enumerate(context_docs, start=1):
                source = {
                    'id': idx,
                    'source': doc.metadata.get('source', 'Unknown'),
                    'content': doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                }
                if 'page' in doc.metadata:
                    source['page'] = doc.metadata['page']
                if 'category' in doc.metadata:
                    source['category'] = doc.metadata['category']
                
                sources.append(source)
        
        return {
            'answer': answer,
            'sources': sources,
            'query': query
        }
    
    def check_query_safety(self, query: str) -> Dict[str, Any]:
        """Check if query is appropriate and safe."""
        emergency_keywords = [
            'emergency', 'urgent', 'immediately', 'severe pain',
            'chest pain', 'can\'t breathe', 'suicide', 'overdose',
            'severe bleeding', 'stroke', 'heart attack'
        ]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in emergency_keywords):
            return {
                'safe': True,
                'warning': 'emergency',
                'message': '🚨 **EMERGENCY**: If this is a medical emergency, please call emergency services (911 in the US) or go to the nearest emergency room immediately.'
            }
        
        personal_keywords = [
            'should i take', 'prescribe', 'recommend treatment',
            'what medication', 'drug dosage', 'am i having'
        ]
        
        if any(keyword in query_lower for keyword in personal_keywords):
            return {
                'safe': True,
                'warning': 'personal_advice',
                'message': '⚠️ **Note**: I can provide general medical information, but cannot provide personal medical advice. Please consult a healthcare provider.'
            }
        
        return {'safe': True, 'warning': None, 'message': None}
