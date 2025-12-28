#!/bin/bash

# Code Review Tool - Startup Script

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║          Code Review & Analysis Tool - Startup               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your configuration"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting MCP Server..."
echo ""

# Start the server
python main.py
