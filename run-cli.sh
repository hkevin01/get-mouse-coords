#!/bin/bash

# Mouse Coordinate Tracker - Command Line Launcher
# Quick access to CLI version

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "🖱️  Mouse Coordinate Tracker - CLI Mode"
echo "======================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🚀 Starting command-line coordinate tracker..."
echo "📍 Move your mouse to see coordinates"
echo "⏹️  Press Ctrl+C to quit"
echo ""

python src/mouse_tracker_cli.py
