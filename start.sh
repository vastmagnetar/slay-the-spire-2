#!/bin/bash
# Slay the Spire 2 - Startup Script

echo "🎮 Slay the Spire 2 - Starting Server..."
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
pip list | grep -q Flask
if [ $? -ne 0 ]; then
    echo "⚠️  Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ All systems ready!"
echo ""
echo "🚀 Starting Flask server on http://localhost:5000"
echo "   Press Ctrl+C to stop"
echo ""

python main.py
