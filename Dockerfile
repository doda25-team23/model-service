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

# Download required NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy application code
COPY src ./src

# ===== F6: Flexible port configuration =====
ENV MODEL_PORT=8081

# ===== F10: External model location =====
# A mounted volume will supply the model OR the app downloads it at runtime.
ENV MODEL_DIR=/app/model

# Create directory for mounted or downloaded models
RUN mkdir -p ${MODEL_DIR}

# Expose dynamic port
EXPOSE ${MODEL_PORT}

# Run Flask app with dynamic port + external model directory
CMD ["sh", "-c", "python src/serve_model.py --port=${MODEL_PORT} --model_dir=${MODEL_DIR}"]
