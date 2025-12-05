#!/bin/bash

# SQL Agent Startup Script

echo "🚀 Starting SQL Agent..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating .env.example..."
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo ""
    echo "Example .env file:"
    echo "OPENAI_API_KEY=your-api-key-here"
    echo "OPENAI_MODEL=gpt-4o-mini"
    echo ""
    read -p "Press enter to continue anyway, or Ctrl+C to exit..."
fi

# Create data directory if it doesn't exist
mkdir -p data

# Start with docker-compose
echo "🐳 Starting Docker containers..."
docker-compose up --build

