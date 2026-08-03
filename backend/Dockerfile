# Use official Python 3.10 slim image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (build-essential needed for compiling any C-extensions if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend codebase
COPY . .

# Expose port
EXPOSE 5000

# Run Flask server
CMD ["python", "app.py"]
