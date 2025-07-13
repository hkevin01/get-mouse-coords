#!/bin/bash
"""
Setup script for Mouse Coordinate Tracker
"""

echo "Setting up Mouse Coordinate Tracker..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To run the GUI application:"
echo "  source venv/bin/activate"
echo "  python src/mouse_tracker_gui.py"
echo ""
echo "To run the command-line version:"
echo "  source venv/bin/activate"
echo "  python src/mouse_tracker_cli.py"
