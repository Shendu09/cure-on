"""Document ingestion and vector store creation."""

import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

# PDF processing
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

import pandas as pd

from config import settings


class DocumentIngester:
    """Handles document loading, chunking, and indexing."""
    
    def __init__(self):
        print("Loading embeddings model (this may take a moment)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True, 'batch_size': 8, 'show_progress_bar': False}
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_documents(self, data_dir: Path = None) -> List[Document]:
        """Load all documents from the data directory."""
        if data_dir is None:
            data_dir = settings.raw_data_dir
        
        documents = []
        
        print(f"\n📂 Loading documents from: {data_dir}")
        
        # Get all files
        supported_extensions = ['.txt', '.pdf', '.csv', '.json']
        files = [f for f in data_dir.iterdir() if f.suffix.lower() in supported_extensions]
        
        if not files:
            print(f"⚠️  No documents found in {data_dir}")
            print(f"   Supported formats: {', '.join(supported_extensions)}")
            print(f"   Creating sample document for demo...")
            return self._create_sample_documents()
        
        for file_path in tqdm(files, desc="Loading files"):
            try:
                docs = self._load_file(file_path)
                documents.extend(docs)
                print(f"   ✓ Loaded {len(docs)} chunks from {file_path.name}")
            except Exception as e:
                print(f"   ✗ Error loading {file_path.name}: {e}")
        
        print(f"\n✓ Total documents loaded: {len(documents)}")
        return documents
    
    def _load_file(self, file_path: Path) -> List[Document]:
        """Load a single file based on its extension."""
        suffix = file_path.suffix.lower()
        
        if suffix == '.txt':
            return self._load_txt(file_path)
        elif suffix == '.pdf':
            return self._load_pdf(file_path)
        elif suffix == '.csv':
            return self._load_csv(file_path)
        elif suffix == '.json':
            return self._load_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
    
    def _load_txt(self, file_path: Path) -> List[Document]:
        """Load a text file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return [Document(
            page_content=text,
            metadata={
                'source': file_path.name,
                'file_type': 'txt'
            }
        )]
    
    def _load_pdf(self, file_path: Path) -> List[Document]:
        """Load a PDF file."""
        if PdfReader is None:
            raise ImportError("pypdf is required for PDF support. Install with: pip install pypdf")
        
        documents = []
        reader = PdfReader(str(file_path))
        
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text.strip():
                documents.append(Document(
                    page_content=text,
                    metadata={
                        'source': file_path.name,
                        'page': page_num,
                        'file_type': 'pdf'
                    }
                ))
        
        return documents
    
    def _load_csv(self, file_path: Path) -> List[Document]:
        """Load a CSV file (expects 'text' or 'content' column)."""
        df = pd.read_csv(file_path)
        
        # Find text column
        text_col = None
        for col in ['text', 'content', 'description', 'body', 'document']:
            if col in df.columns:
                text_col = col
                break
        
        if text_col is None:
            raise ValueError(f"CSV must have a 'text' or 'content' column. Found: {df.columns.tolist()}")
        
        documents = []
        for idx, row in df.iterrows():
            text = str(row[text_col])
            if text.strip():
                metadata = {
                    'source': file_path.name,
                    'row': idx + 1,
                    'file_type': 'csv'
                }
                # Add other columns as metadata
                for col in df.columns:
                    if col != text_col:
                        metadata[col] = str(row[col])
                
                documents.append(Document(
                    page_content=text,
                    metadata=metadata
                ))
        
        return documents
    
    def _load_json(self, file_path: Path) -> List[Document]:
        """Load a JSON file (expects list of dicts with 'text' or 'content' key)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            data = [data]
        
        documents = []
        for idx, item in enumerate(data):
            # Find text field
            text = item.get('text') or item.get('content') or item.get('description')
            if not text:
                continue
            
            metadata = {
                'source': file_path.name,
                'index': idx,
                'file_type': 'json'
            }
            # Add all other fields as metadata
            for key, value in item.items():
                if key not in ['text', 'content', 'description']:
                    metadata[key] = str(value)
            
            documents.append(Document(
                page_content=text,
                metadata=metadata
            ))
        
        return documents
    
    def _create_sample_documents(self) -> List[Document]:
        """Create sample medical documents for demo purposes."""
        samples = [
            {
                'content': """Diabetes Mellitus Overview
                
Diabetes is a chronic condition that affects how your body processes blood sugar (glucose). There are two main types:

Type 1 Diabetes: An autoimmune condition where the body doesn't produce insulin. It typically develops in children and young adults.

Type 2 Diabetes: The body becomes resistant to insulin or doesn't produce enough insulin. It's more common in adults and is often associated with obesity and lack of physical activity.

Common symptoms include increased thirst, frequent urination, extreme fatigue, blurred vision, and slow-healing wounds. Early detection and proper management are crucial for preventing complications such as heart disease, kidney damage, and nerve damage.""",
                'source': 'diabetes_guide.txt',
                'category': 'Endocrinology'
            },
            {
                'content': """Hypertension (High Blood Pressure)

Hypertension is a condition in which the force of blood against artery walls is consistently too high. Blood pressure readings consist of two numbers: systolic (pressure when the heart beats) over diastolic (pressure when the heart rests).

Normal: Below 120/80 mm Hg
Elevated: 120-129/<80 mm Hg
Stage 1 Hypertension: 130-139/80-89 mm Hg
Stage 2 Hypertension: 140/90 mm Hg or higher

Risk factors include age, family history, obesity, high salt intake, lack of physical activity, and stress. Management involves lifestyle changes (diet, exercise, stress reduction) and medications if necessary. Regular monitoring is essential.""",
                'source': 'cardiovascular_health.txt',
                'category': 'Cardiology'
            },
            {
                'content': """Common Cold vs. Flu

While both are respiratory illnesses, they are caused by different viruses and have distinct characteristics:

Common Cold:
- Gradual onset
- Mild symptoms
- Runny or stuffy nose, sore throat, cough
- Rarely causes complications
- Duration: 7-10 days

Influenza (Flu):
- Sudden onset
- Severe symptoms
- High fever, body aches, fatigue, dry cough
- Can lead to pneumonia and hospitalization
- Duration: 1-2 weeks or longer

Prevention: Hand hygiene, avoiding close contact with sick individuals, annual flu vaccination for influenza. Treatment: Rest, fluids, over-the-counter medications for symptom relief. Antiviral medications available for flu if started within 48 hours of symptom onset.""",
                'source': 'infectious_diseases.txt',
                'category': 'Infectious Disease'
            }
        ]
        
        documents = []
        for sample in samples:
            documents.append(Document(
                page_content=sample['content'],
                metadata={
                    'source': sample['source'],
                    'category': sample.get('category', 'General'),
                    'file_type': 'sample'
                }
            ))
        
        print(f"   ℹ️  Created {len(documents)} sample documents for demo")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        print("\n✂️  Chunking documents...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"   ✓ Created {len(chunks)} chunks")
        return chunks
    
    def create_vector_store(self, chunks: List[Document]) -> FAISS:
        """Create FAISS vector store from document chunks."""
        print("\n🔢 Generating embeddings and creating vector store...")
        
        # Process in batches to avoid rate limits
        batch_size = 100
        vector_store = None
        
        for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding batches"):
            batch = chunks[i:i + batch_size]
            
            if vector_store is None:
                vector_store = FAISS.from_documents(batch, self.embeddings)
            else:
                batch_store = FAISS.from_documents(batch, self.embeddings)
                vector_store.merge_from(batch_store)
        
        print(f"   ✓ Vector store created with {len(chunks)} chunks")
        return vector_store
    
    def save_vector_store(self, vector_store: FAISS, path: Path = None):
        """Save vector store to disk."""
        if path is None:
            path = settings.vector_store_dir
        
        print(f"\n💾 Saving vector store to: {path}")
        vector_store.save_local(str(path))
        print("   ✓ Vector store saved successfully")
    
    def ingest(self) -> FAISS:
        """Full ingestion pipeline."""
        print("\n" + "="*60)
        print("🏥 Medical RAG Chatbot - Document Ingestion")
        print("="*60)
        
        # Load documents
        documents = self.load_documents()
        
        if not documents:
            raise ValueError("No documents loaded. Please add files to the data/raw directory.")
        
        # Chunk documents
        chunks = self.chunk_documents(documents)
        
        # Create vector store
        vector_store = self.create_vector_store(chunks)
        
        # Save to disk
        self.save_vector_store(vector_store)
        
        print("\n" + "="*60)
        print("✅ Ingestion complete!")
        print("="*60)
        print(f"   Documents: {len(documents)}")
        print(f"   Chunks: {len(chunks)}")
        print(f"   Vector store: {settings.vector_store_dir}")
        print("\n   Next steps:")
        print("   1. Run the API: python src/app_api.py")
        print("   2. Or run Gradio UI: python src/app_gradio.py")
        print("="*60 + "\n")
        
        return vector_store


def main():
    """CLI entry point."""
    try:
        ingester = DocumentIngester()
        ingester.ingest()
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    main()
