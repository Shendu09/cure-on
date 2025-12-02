"""LLM module for generating answers with citations."""

from typing import List, Dict, Any
from langchain_community.llms import HuggingFacePipeline
from langchain.schema import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from config import settings


class LLM:
    """Wrapper for local LLM with medical-specific prompting."""
    
    def __init__(self):
        """Initialize local LLM."""
        print(f"Loading local LLM: {settings.llm_model}...")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(settings.llm_model)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(settings.llm_model)
        
        # Create pipeline
        pipe = pipeline(
            "text2text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_length=settings.max_tokens,
            temperature=settings.temperature,
            do_sample=True if settings.temperature > 0 else False
        )
        
        self.llm = HuggingFacePipeline(pipeline=pipe)
        
        print("✓ LLM loaded successfully")
        
        self.system_prompt = """You are a helpful medical information assistant. Your role is to provide accurate, evidence-based medical information based on the provided context.

IMPORTANT GUIDELINES:
1. Answer ONLY based on the provided context documents
2. If the context doesn't contain enough information to answer the question, say so clearly
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
        
        # Build prompt (for text2text models like FLAN-T5)
        prompt = f"""You are a helpful medical information assistant. Answer the question based on the context provided.

Context:
{context}

Question: {query}

Instructions:
- Answer ONLY based on the context above
- Cite sources using [Source X] notation
- Use clear, accessible language
- If context is insufficient, say so
- Remind users to consult healthcare professionals

Answer:"""
        
        # Generate response
        answer = self.llm.invoke(prompt)
        
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
        # Keywords that might indicate emergency or inappropriate queries
        emergency_keywords = [
            'emergency', 'urgent', 'immediately', 'severe pain',
            'chest pain', 'can\'t breathe', 'suicide', 'overdose',
            'severe bleeding', 'stroke', 'heart attack'
        ]
        
        query_lower = query.lower()
        
        # Check for emergency
        if any(keyword in query_lower for keyword in emergency_keywords):
            return {
                'safe': True,
                'warning': 'emergency',
                'message': '🚨 **EMERGENCY**: If this is a medical emergency, please call emergency services (911 in the US) or go to the nearest emergency room immediately. Do not rely on this chatbot for emergency medical situations.'
            }
        
        # Check for overly personal medical advice requests
        personal_keywords = [
            'should i take', 'prescribe', 'recommend treatment',
            'what medication', 'drug dosage', 'am i having'
        ]
        
        if any(keyword in query_lower for keyword in personal_keywords):
            return {
                'safe': True,
                'warning': 'personal_advice',
                'message': '⚠️ **Note**: I can provide general medical information, but I cannot provide personal medical advice, diagnoses, or treatment recommendations. Please consult with a qualified healthcare provider for personalized medical guidance.'
            }
        
        return {'safe': True, 'warning': None, 'message': None}


def test_llm():
    """Test LLM with sample context."""
    print("\n" + "="*60)
    print("🤖 Testing LLM")
    print("="*60)
    
    llm = LLM()
    
    # Create sample context documents
    sample_docs = [
        Document(
            page_content="Diabetes symptoms include increased thirst, frequent urination, extreme fatigue, blurred vision, and slow-healing wounds.",
            metadata={'source': 'diabetes_guide.txt', 'page': 1, 'category': 'Endocrinology'}
        ),
        Document(
            page_content="Type 2 diabetes is more common in adults and is often associated with obesity and lack of physical activity. Management includes diet, exercise, and medications.",
            metadata={'source': 'diabetes_guide.txt', 'page': 2, 'category': 'Endocrinology'}
        )
    ]
    
    query = "What are the symptoms of diabetes?"
    
    print(f"\nQuery: {query}\n")
    
    result = llm.generate_answer(query, sample_docs)
    
    print("Answer:")
    print(result['answer'])
    print("\nSources:")
    for source in result['sources']:
        print(f"  [{source['id']}] {source['source']}", end='')
        if 'page' in source:
            print(f" (Page {source['page']})", end='')
        print()
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_llm()
