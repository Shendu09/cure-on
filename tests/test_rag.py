"""Unit tests for Medical RAG Chatbot."""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import settings
from langchain.schema import Document


class TestChunking:
    """Test document chunking."""
    
    def test_chunk_size(self):
        """Test that chunks respect size limits."""
        from ingest import DocumentIngester
        
        ingester = DocumentIngester()
        
        # Create a long document
        long_text = "This is a test sentence. " * 100
        doc = Document(page_content=long_text, metadata={'source': 'test.txt'})
        
        chunks = ingester.chunk_documents([doc])
        
        # Check that chunks are created
        assert len(chunks) > 1
        
        # Check that chunks respect size (with some tolerance for overlap)
        for chunk in chunks:
            assert len(chunk.page_content) <= settings.chunk_size + settings.chunk_overlap


class TestRetriever:
    """Test retriever functionality."""
    
    @pytest.fixture
    def mock_documents(self):
        """Create mock documents for testing."""
        return [
            Document(
                page_content="Diabetes symptoms include increased thirst and frequent urination.",
                metadata={'source': 'diabetes.txt', 'category': 'Endocrinology'}
            ),
            Document(
                page_content="Hypertension is high blood pressure that can lead to heart disease.",
                metadata={'source': 'hypertension.txt', 'category': 'Cardiology'}
            ),
            Document(
                page_content="The common cold is a viral infection of the upper respiratory tract.",
                metadata={'source': 'cold.txt', 'category': 'Infectious Disease'}
            )
        ]
    
    def test_source_formatting(self, mock_documents):
        """Test source formatting."""
        from retriever import Retriever
        
        # This would require a vector store, so we'll test the format_sources method directly
        # In a real test, you'd create a temporary vector store
        
        # For now, just test that the method exists and returns expected structure
        retriever = Retriever.__new__(Retriever)
        sources = retriever.format_sources(mock_documents)
        
        assert len(sources) == 3
        assert all('id' in s for s in sources)
        assert all('source' in s for s in sources)
        assert all('content' in s for s in sources)


class TestLLM:
    """Test LLM functionality."""
    
    def test_safety_check_emergency(self):
        """Test emergency detection."""
        from llm import LLM
        
        llm = LLM()
        
        emergency_queries = [
            "I'm having chest pain",
            "Can't breathe, urgent help needed",
            "Severe bleeding emergency"
        ]
        
        for query in emergency_queries:
            result = llm.check_query_safety(query)
            assert result['safe'] == True
            assert result['warning'] == 'emergency'
    
    def test_safety_check_personal_advice(self):
        """Test personal advice detection."""
        from llm import LLM
        
        llm = LLM()
        
        advice_queries = [
            "Should I take aspirin?",
            "What medication do you recommend?",
            "What's the right drug dosage for me?"
        ]
        
        for query in advice_queries:
            result = llm.check_query_safety(query)
            assert result['safe'] == True
            assert result['warning'] == 'personal_advice'
    
    def test_safety_check_safe_query(self):
        """Test safe query detection."""
        from llm import LLM
        
        llm = LLM()
        
        safe_queries = [
            "What are the symptoms of diabetes?",
            "How is hypertension treated in general?",
            "What causes the common cold?"
        ]
        
        for query in safe_queries:
            result = llm.check_query_safety(query)
            assert result['safe'] == True
            assert result['warning'] is None


class TestRAGSystem:
    """Test full RAG system (requires vector store)."""
    
    @pytest.mark.skipif(
        not (settings.vector_store_dir / "index.faiss").exists(),
        reason="Vector store not found. Run ingestion first."
    )
    def test_query_execution(self):
        """Test end-to-end query."""
        from rag import RAGSystem
        
        rag = RAGSystem()
        result = rag.query("What are common symptoms?")
        
        assert 'answer' in result
        assert 'sources' in result
        assert 'query' in result
        assert isinstance(result['sources'], list)
    
    def test_format_response(self):
        """Test response formatting."""
        from rag import RAGSystem
        
        mock_result = {
            'answer': 'Test answer',
            'sources': [
                {'id': 1, 'source': 'test.txt', 'content': 'Test content'}
            ],
            'query': 'Test query',
            'disclaimer': 'Test disclaimer'
        }
        
        rag = RAGSystem.__new__(RAGSystem)
        formatted = rag.format_response(mock_result)
        
        assert 'Test answer' in formatted
        assert 'test.txt' in formatted
        assert 'Test disclaimer' in formatted


def test_config_loading():
    """Test configuration loading."""
    assert settings.chunk_size > 0
    assert settings.chunk_overlap >= 0
    assert settings.top_k > 0
    assert settings.temperature >= 0 and settings.temperature <= 2


def test_data_directories_exist():
    """Test that data directories are created."""
    assert settings.raw_data_dir.exists()
    assert settings.vector_store_dir.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
