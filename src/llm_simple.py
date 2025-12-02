"""Simple LLM fallback without transformers."""

from typing import List, Dict, Any
from langchain.schema import Document
from config import settings


class LLM:
    """Simple template-based response system (fallback when models unavailable)."""
    
    def __init__(self):
        """Initialize simple responder."""
        print("⚠️  Using template-based responses (LLM loading disabled)")
        print("   This provides simple answers based on retrieved context.")
        
        self.system_prompt = """You are a helpful medical information assistant."""
    
    def generate_answer(
        self,
        query: str,
        context_docs: List[Document],
        include_sources: bool = True
    ) -> Dict[str, Any]:
        """Generate a simple answer based on retrieved context."""
        
        # Format context
        context_parts = []
        for idx, doc in enumerate(context_docs, start=1):
            source_info = f"[Source {idx}: {doc.metadata.get('source', 'Unknown')}"
            if 'page' in doc.metadata:
                source_info += f", Page {doc.metadata['page']}"
            source_info += "]"
            context_parts.append(f"{source_info}\n{doc.page_content}")
        
        # Create simple answer from context
        answer_parts = []
        answer_parts.append(f"Based on the available information about '{query}':\n")
        
        for idx, doc in enumerate(context_docs, start=1):
            content = doc.page_content.strip()
            # Take first 200 chars or first paragraph
            preview = content.split('\n\n')[0] if '\n\n' in content else content[:300]
            answer_parts.append(f"{preview} [Source {idx}]")
        
        answer = "\n\n".join(answer_parts)
        
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
