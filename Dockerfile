FROM python:3.12.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data (required by the app)
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy application code
COPY src ./src

# ===== F6: Flexible port configuration =====
ENV MODEL_PORT=8081

# ===== F10: External model location =====
# The model will either come from a mounted volume or be downloaded at runtime.
ENV MODEL_DIR=/app/model

# Ensure the directory exists (for volume or download)
RUN mkdir -p ${MODEL_DIR}

# Expose the port
EXPOSE ${MODEL_PORT}

# ===== F10: Download model if missing, then start the service =====
CMD ["sh", "-c", "python src/download_model.py && python src/serve_model.py --port=${MODEL_PORT} --model_dir=${MODEL_DIR}"]
