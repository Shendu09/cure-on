"""Retriever module for semantic search over vector store."""

from pathlib import Path
from typing import List, Dict, Any

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from config import settings


class Retriever:
    """Handles semantic search and document retrieval."""
    
    def __init__(self, vector_store_path: Path = None):
        """Initialize retriever with vector store."""
        if vector_store_path is None:
            vector_store_path = settings.vector_store_dir
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True, 'batch_size': 8}
        )
        
        # Load vector store
        try:
            self.vector_store = FAISS.load_local(
                str(vector_store_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"✓ Loaded vector store from {vector_store_path}")
        except Exception as e:
            raise RuntimeError(
                f"Failed to load vector store from {vector_store_path}. "
                f"Please run 'python src/ingest.py' first. Error: {e}"
            )
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """Retrieve top-k most relevant document chunks."""
        if k is None:
            k = settings.top_k
        
        # Perform similarity search
        docs = self.vector_store.similarity_search(query, k=k)
        return docs
    
    def retrieve_with_scores(self, query: str, k: int = None) -> List[tuple[Document, float]]:
        """Retrieve top-k most relevant chunks with similarity scores."""
        if k is None:
            k = settings.top_k
        
        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=k)
        return docs_with_scores
    
    def format_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Format retrieved documents as source citations."""
        sources = []
        
        for idx, doc in enumerate(documents, start=1):
            source_info = {
                'id': idx,
                'source': doc.metadata.get('source', 'Unknown'),
                'content': doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                'full_content': doc.page_content
            }
            
            # Add page number if available
            if 'page' in doc.metadata:
                source_info['page'] = doc.metadata['page']
            
            # Add row/index if from CSV/JSON
            if 'row' in doc.metadata:
                source_info['row'] = doc.metadata['row']
            elif 'index' in doc.metadata:
                source_info['index'] = doc.metadata['index']
            
            # Add category if available
            if 'category' in doc.metadata:
                source_info['category'] = doc.metadata['category']
            
            sources.append(source_info)
        
        return sources


def test_retriever():
    """Test the retriever with sample queries."""
    print("\n" + "="*60)
    print("🔍 Testing Retriever")
    print("="*60)
    
    retriever = Retriever()
    
    test_queries = [
        "What are the symptoms of diabetes?",
        "How is hypertension treated?",
        "What is the difference between cold and flu?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 60)
        
        docs = retriever.retrieve(query, k=2)
        sources = retriever.format_sources(docs)
        
        for source in sources:
            print(f"\n[Source {source['id']}] {source['source']}")
            if 'page' in source:
                print(f"Page: {source['page']}")
            print(f"Content: {source['content']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    test_retriever()
