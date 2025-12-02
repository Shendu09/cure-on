#!/bin/bash

# Render start script - runs when service starts

echo "🚀 Starting Medical RAG Chatbot..."

# Check if vector store exists, if not create it
if [ ! -f "data/vector_store/index.faiss" ]; then
    echo "📊 No vector store found. Creating from sample data..."
    python src/ingest.py
else
    echo "✓ Vector store found, using existing index"
fi

# Start the Gradio app
echo "🏥 Launching Gradio UI..."
python src/app_gradio.py
