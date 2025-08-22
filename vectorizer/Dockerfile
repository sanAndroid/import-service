# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install protoc compiler if not already
RUN apt-get update && apt-get install -y --no-install-recommends \
      protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Copy your app
COPY vectorizer.py .
COPY vectorize.proto .

# Expose GPRC port
EXPOSE 50051

# Auto Generate Code 
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. vectorize.proto
# Run the vectorizer
CMD ["python", "vectorizer.py"]
