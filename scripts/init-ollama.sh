#!/bin/bash

# Script to initialize Ollama with models

echo "Initializing Ollama with models..."

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434/api/tags >/dev/null; do
    sleep 5
done

echo "Ollama is ready. Pulling models..."

# Pull some useful models
echo "Pulling llama2 model..."
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello"
}'

echo "Pulling mistral model..."
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Hello"
}'

echo "Pulling orca-mini model..."
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "orca-mini",
  "prompt": "Hello"
}'

echo "Ollama initialization complete!"