FROM python:3.12.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data at build time (optional but okay)
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy application source code
COPY src ./src

# F10: external model dir
ENV MODEL_DIR=/models

# F10: model dir inside container
RUN mkdir -p /models


# Expose the API port
EXPOSE 8081

# F10: we download model if missing then run
CMD ["sh", "-c", "python src/download_model.py && python src/serve_model.py"]
