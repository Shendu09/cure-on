"""Main RAG system orchestration."""

from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from retriever import Retriever
from config import settings

# Import appropriate LLM based on configuration
if settings.use_huggingface:
    from llm_huggingface import LLM  # Hugging Face API (free, cloud-ready)
elif settings.use_local_models:
    from llm_ollama import LLM  # Using Ollama for local LLMs
else:
    from llm import LLM  # Fallback to OpenAI


class RAGSystem:
    """Complete RAG pipeline for medical Q&A."""
    
    def __init__(self, vector_store_path: Optional[Path] = None):
        """Initialize RAG system."""
        print("🏥 Initializing Medical RAG System...")
        
        # Initialize components
        self.retriever = Retriever(vector_store_path)
        self.llm = LLM()
        
        print("✓ RAG system ready!\n")
    
    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        include_disclaimer: bool = True
    ) -> Dict[str, Any]:
        """Process a user query through the RAG pipeline."""
        
        # Check query safety
        safety_check = self.llm.check_query_safety(question)
        
        # Retrieve relevant documents
        if top_k is None:
            top_k = settings.top_k
        
        docs = self.retriever.retrieve(question, k=top_k)
        
        if not docs:
            return {
                'answer': "I couldn't find relevant information in the knowledge base to answer your question. Please rephrase or ask about a different topic.",
                'sources': [],
                'query': question,
                'warning': safety_check.get('message'),
                'disclaimer': settings.medical_disclaimer if include_disclaimer else None
            }
        
        # Generate answer
        result = self.llm.generate_answer(question, docs)
        
        # Add safety warning if present
        if safety_check.get('message'):
            result['warning'] = safety_check['message']
        
        # Add medical disclaimer
        if include_disclaimer:
            result['disclaimer'] = settings.medical_disclaimer
        
        return result
    
    def format_response(self, result: Dict[str, Any]) -> str:
        """Format the response for display."""
        output = []
        
        # Add warning if present
        if result.get('warning'):
            output.append(result['warning'])
            output.append("")
        
        # Add answer
        output.append(result['answer'])
        output.append("")
        
        # Add sources
        if result.get('sources'):
            output.append("**Sources:**")
            for source in result['sources']:
                source_line = f"[{source['id']}] {source['source']}"
                if 'page' in source:
                    source_line += f" (Page {source['page']})"
                if 'category' in source:
                    source_line += f" - {source['category']}"
                output.append(source_line)
            output.append("")
        
        # Add disclaimer
        if result.get('disclaimer'):
            output.append(result['disclaimer'])
        
        return "\n".join(output)


def main():
    """CLI interface for testing."""
    print("\n" + "="*60)
    print("🏥 Medical RAG Chatbot - Interactive Mode")
    print("="*60)
    print("\nInitializing system...")
    
    try:
        rag = RAGSystem()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease run 'python src/ingest.py' first to create the vector store.")
        return
    
    print("Type your medical questions (or 'quit' to exit)\n")
    
    while True:
        try:
            query = input("\n💬 You: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            print("\n🤔 Thinking...")
            result = rag.query(query)
            
            print("\n" + "="*60)
            print(rag.format_response(result))
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
