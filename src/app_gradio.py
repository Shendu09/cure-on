"""Gradio web UI for Medical RAG Chatbot."""

import gradio as gr
from typing import List, Tuple
import traceback
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from rag import RAGSystem
from config import settings


# Initialize RAG system
print("🏥 Initializing Medical RAG System for Gradio...")
try:
    rag_system = RAGSystem()
    print("✓ System ready!\n")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Please run 'python src/ingest.py' first to create the vector store.\n")
    raise


def format_sources_html(sources: List[dict]) -> str:
    """Format sources as HTML for better display."""
    if not sources:
        return ""
    
    html = "<div style='margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 5px;'>"
    html += "<h4 style='margin-top: 0;'>📚 Sources:</h4>"
    
    for source in sources:
        html += f"<div style='margin: 10px 0; padding: 10px; background-color: white; border-left: 3px solid #4CAF50;'>"
        html += f"<strong>[{source['id']}] {source['source']}</strong>"
        
        if 'page' in source:
            html += f" <em>(Page {source['page']})</em>"
        
        if 'category' in source:
            html += f" <span style='color: #666;'>- {source['category']}</span>"
        
        html += f"<br><small style='color: #666;'>{source['content'][:200]}...</small>"
        html += "</div>"
    
    html += "</div>"
    return html


def chat_fn(message: str, history: List[Tuple[str, str]]) -> Tuple[str, str]:
    """Process chat message and return response."""
    try:
        if not message.strip():
            return "", "Please enter a question."
        
        # Query RAG system
        result = rag_system.query(message, include_disclaimer=True)
        
        # Format answer
        answer = result['answer']
        
        # Add warning if present
        if result.get('warning'):
            answer = f"⚠️ {result['warning']}\n\n{answer}"
        
        # Add disclaimer
        if result.get('disclaimer'):
            answer = f"{answer}\n\n---\n\n{result['disclaimer']}"
        
        # Format sources separately
        sources_html = format_sources_html(result.get('sources', []))
        
        return answer, sources_html
    
    except Exception as e:
        error_msg = f"❌ Error: {str(e)}\n\n{traceback.format_exc()}"
        return error_msg, ""


# Custom CSS
custom_css = """
#chatbot {
    height: 500px;
}
#sources {
    max-height: 400px;
    overflow-y: auto;
}
.disclaimer {
    background-color: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}
"""

# Example queries
examples = [
    "What are the symptoms of diabetes?",
    "How is hypertension diagnosed and treated?",
    "What's the difference between a cold and the flu?",
    "What are the risk factors for heart disease?",
    "How can I prevent type 2 diabetes?",
]

# Build Gradio interface
with gr.Blocks(css=custom_css, title="Medical RAG Chatbot", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🏥 Medical RAG Chatbot
        
        Ask medical questions and get accurate, citation-backed answers from our knowledge base.
        
        **Important**: This chatbot provides general medical information for educational purposes only. 
        It is not a substitute for professional medical advice, diagnosis, or treatment.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="Chat",
                elem_id="chatbot",
                height=500,
                show_label=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask a medical question...",
                    lines=2,
                    scale=4
                )
                submit = gr.Button("Send", variant="primary", scale=1)
            
            clear = gr.Button("Clear Chat")
            
            gr.Examples(
                examples=examples,
                inputs=msg,
                label="Example Questions"
            )
        
        with gr.Column(scale=1):
            sources = gr.HTML(
                label="Sources & Citations",
                elem_id="sources"
            )
    
    gr.Markdown(
        """
        ---
        
        ### ⚕️ Medical Disclaimer
        
        This chatbot is for informational and educational purposes only and is not a substitute 
        for professional medical advice, diagnosis, or treatment. Always seek the advice of your 
        physician or other qualified health provider with any questions you may have regarding 
        a medical condition.
        
        ### 🔒 Privacy
        
        Your queries are processed securely. We do not store personal medical information.
        
        ### 📊 System Info
        
        - **Model**: {model}
        - **Embeddings**: {embedding_model}
        - **Knowledge Base**: Medical documents
        """.format(
            model=settings.llm_model,
            embedding_model=settings.embedding_model
        )
    )
    
    def user_msg(user_message, history):
        """Add user message to chat."""
        return "", history + [[user_message, None]]
    
    def bot_msg(history):
        """Generate bot response."""
        user_message = history[-1][0]
        bot_response, sources_html = chat_fn(user_message, history[:-1])
        history[-1][1] = bot_response
        return history, sources_html
    
    # Event handlers
    msg.submit(user_msg, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_msg, chatbot, [chatbot, sources]
    )
    
    submit.click(user_msg, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot_msg, chatbot, [chatbot, sources]
    )
    
    clear.click(lambda: ([], ""), None, [chatbot, sources], queue=False)


def main():
    """Launch Gradio app."""
    import os
    
    print("\n" + "="*60)
    print("🏥 Medical RAG Chatbot - Gradio Web UI")
    print("="*60)
    print(f"\nLaunching Gradio interface on port {settings.gradio_port}...")
    print("="*60 + "\n")
    
    # For Render deployment, use 0.0.0.0 and PORT env variable
    server_name = os.getenv("GRADIO_SERVER_NAME", "127.0.0.1")
    server_port = int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", settings.gradio_port)))
    
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=False,
        show_error=True,
        inbrowser=False  # Don't open browser on server
    )


if __name__ == "__main__":
    main()
