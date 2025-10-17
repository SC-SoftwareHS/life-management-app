# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Expose port (Railway will override with $PORT)
EXPOSE 8000

# Command to run the application
CMD uvicorn server.app.main:app --host 0.0.0.0 --port ${PORT:-8000}
