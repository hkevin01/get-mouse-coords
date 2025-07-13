#!/bin/bash

# Mouse Coordinate Tracker - Enhanced Installation & Launch Script
# This script provides a complete setup and launch experience

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main banner
echo -e "${BLUE}"
echo "=================================================================="
echo "    🖱️  Mouse Coordinate Tracker - Installation & Launcher"
echo "=================================================================="
echo -e "${NC}"

# Check if Python 3 is available
print_status "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed."
    echo ""
    echo "Please install Python 3.6+ using one of these methods:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "  macOS:         brew install python3"
    echo ""
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
print_success "Python $python_version found"

# Check if version is 3.6+
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)" 2>/dev/null; then
    print_error "Python 3.6+ is required. Current version: $python_version"
    exit 1
fi

# Check if virtual environment exists, create if not
print_status "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment found"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip --quiet

# Install/update dependencies
print_status "Installing dependencies..."
if pip install -r requirements.txt --quiet; then
    print_success "Dependencies installed successfully"
else
    print_warning "Some dependencies failed to install, trying individual packages..."
    pip install PyQt5>=5.15.0 --quiet || print_warning "PyQt5 installation failed"
    pip install pyautogui>=0.9.54 --quiet || print_warning "pyautogui installation failed"
    pip install pynput>=1.7.6 --quiet || print_warning "pynput installation failed"
fi

# Generate icons if script exists
if [ -f "scripts/generate_icons.py" ]; then
    print_status "Generating application icons..."
    if python scripts/generate_icons.py 2>/dev/null; then
        print_success "Icons generated successfully"
    else
        print_warning "Icon generation failed, but continuing..."
    fi
fi

# Create desktop launcher (optional)
create_desktop_launcher() {
    local desktop_file="$HOME/Desktop/mouse-coordinate-tracker.desktop"
    local current_dir=$(pwd)
    
    cat > "$desktop_file" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Mouse Coordinate Tracker
Comment=Track and save mouse coordinates
Exec=bash -c "cd '$current_dir' && source venv/bin/activate && python src/mouse_tracker_gui.py"
Icon=$current_dir/assets/mouse_icon_64x64.png
Terminal=false
Categories=Utility;Development;
EOF
    
    chmod +x "$desktop_file"
    print_success "Desktop launcher created: $desktop_file"
}

# Main menu
echo ""
echo "Setup complete! Choose an option:"
echo "  1. Launch GUI Application"
echo "  2. Launch CLI Application"
echo "  3. Create Desktop Launcher"
echo "  4. Install System-wide (requires sudo)"
echo "  5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        print_status "Launching GUI application..."
        python src/mouse_tracker_gui.py
        ;;
    2)
        print_status "Launching CLI application..."
        python src/mouse_tracker_cli.py
        ;;
    3)
        create_desktop_launcher
        ;;
    4)
        print_status "Installing system-wide..."
        sudo cp install.sh /usr/local/bin/mouse-coordinate-tracker
        sudo chmod +x /usr/local/bin/mouse-coordinate-tracker
        print_success "Installed to /usr/local/bin/mouse-coordinate-tracker"
        print_status "You can now run 'mouse-coordinate-tracker' from anywhere"
        ;;
    5)
        print_status "Exiting..."
        ;;
    *)
        print_warning "Invalid choice. To run the application later, use:"
        echo "  GUI: source venv/bin/activate && python src/mouse_tracker_gui.py"
        echo "  CLI: source venv/bin/activate && python src/mouse_tracker_cli.py"
        ;;
esac

echo ""
print_success "Thanks for using Mouse Coordinate Tracker!"
