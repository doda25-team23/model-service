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

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Copy source code
COPY src ./src

# Create output directory for model files
RUN mkdir -p output

# Download dataset and prepare model
RUN python src/get_data.py && \
    python src/text_preprocessing.py && \
    python src/text_classification.py

# Expose the API port
EXPOSE 8081

# Run the Flask application
CMD ["python", "src/serve_model.py"]
