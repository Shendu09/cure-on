FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create directories
RUN mkdir -p data/raw data/vector_store

# Environment
ENV PYTHONUNBUFFERED=1 \
    USE_HUGGINGFACE=true

EXPOSE 7860

# Ingest data then start app
CMD python src/ingest.py && python src/app_gradio.py
