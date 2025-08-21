# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app
COPY vectorizer.py .

# Expose FastAPI port
EXPOSE 8000

# Start with Uvicorn
CMD ["uvicorn", "vectorizer:app", "--host", "0.0.0.0", "--port", "8000"]
