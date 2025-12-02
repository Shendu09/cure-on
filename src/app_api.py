"""FastAPI application for Medical RAG Chatbot."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn

from rag import RAGSystem
from config import settings


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model."""
    query: str = Field(..., description="User's medical question", min_length=1)
    top_k: Optional[int] = Field(None, description="Number of sources to retrieve", ge=1, le=10)
    include_disclaimer: bool = Field(True, description="Include medical disclaimer in response")


class Source(BaseModel):
    """Source citation model."""
    id: int
    source: str
    content: str
    page: Optional[int] = None
    category: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str
    sources: List[Source]
    query: str
    warning: Optional[str] = None
    disclaimer: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="Medical RAG Chatbot API",
    description="A RAG-based medical information chatbot with citation support",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system: Optional[RAGSystem] = None


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup."""
    global rag_system
    try:
        print("\n🚀 Starting Medical RAG Chatbot API...")
        rag_system = RAGSystem()
        print("✓ RAG system initialized successfully\n")
    except Exception as e:
        print(f"\n❌ Failed to initialize RAG system: {e}")
        print("Please run 'python src/ingest.py' first to create the vector store.\n")
        raise


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return {
        "status": "running",
        "message": "Medical RAG Chatbot API is running. Visit /docs for API documentation."
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return {
        "status": "healthy",
        "message": "System is operational"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for medical questions."""
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized. Please run ingestion first."
        )
    
    try:
        # Process query
        result = rag_system.query(
            question=request.query,
            top_k=request.top_k,
            include_disclaimer=request.include_disclaimer
        )
        
        # Format sources
        sources = [Source(**source) for source in result['sources']]
        
        return ChatResponse(
            answer=result['answer'],
            sources=sources,
            query=result['query'],
            warning=result.get('warning'),
            disclaimer=result.get('disclaimer')
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/stats")
async def stats():
    """Get system statistics."""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    return {
        "model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "chunk_size": settings.chunk_size,
        "top_k": settings.top_k,
        "vector_store": str(settings.vector_store_dir)
    }


def main():
    """Run the FastAPI server."""
    print("\n" + "="*60)
    print("🏥 Medical RAG Chatbot - FastAPI Server")
    print("="*60)
    print(f"\nStarting server on http://{settings.api_host}:{settings.api_port}")
    print(f"API docs: http://{settings.api_host}:{settings.api_port}/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
