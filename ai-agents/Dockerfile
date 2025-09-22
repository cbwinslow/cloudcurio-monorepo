# Dockerfile for AI Agents
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package management
RUN pip install uv

# Copy requirements and install Python dependencies with uv
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port for API (if needed)
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]