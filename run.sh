#!/bin/bash

# Mouse Coordinate Tracker - Quick Run Script
# This script sets up the environment and launches the application

set -e  # Exit on any error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "🖱️  Mouse Coordinate Tracker"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "📦 Setting up the project for the first time..."
    echo ""
    
    # Run setup script
    if [ -f "scripts/setup.sh" ]; then
        chmod +x scripts/setup.sh
        ./scripts/setup.sh
    else
        echo "❌ Setup script not found!"
        exit 1
    fi
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Setup display for GUI applications
echo "🖥️  Setting up display environment..."
export DISPLAY=${DISPLAY:-:0}
xhost +local: 2>/dev/null || echo "X11 access control setup attempted"

# Check if packages are installed
echo "📋 Checking dependencies..."
if ! python -c "import PyQt5, pyautogui, pynput" 2>/dev/null; then
    echo "📦 Installing missing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Environment ready!"
echo ""

# Default behavior: Launch GUI directly
echo "🚀 Launching Mouse Coordinate Tracker GUI..."
echo ""
echo "� Features available:"
echo "   • Real-time coordinate display"
echo "   • Visual mouse highlighting"
echo "   • Copy coordinates to clipboard"
echo "   • Adjustable update frequency"
echo ""

# Launch GUI application
python src/mouse_tracker_gui.py

echo ""
echo "� Mouse Coordinate Tracker closed."
