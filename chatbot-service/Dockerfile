# ──────────────────────────────────────────────────────────────
# TravelHUB Chatbot Service — Python 3.11 FastAPI
# ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install system deps for sentence-transformers / chromadb
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY data_sync.py .

# Persistent ChromaDB volume mount point
VOLUME ["/app/chroma_data"]

# Expose chatbot port
EXPOSE 8001

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
