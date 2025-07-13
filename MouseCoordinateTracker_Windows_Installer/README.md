# Mouse Coordinate Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/doc/versions/)
[![Made with PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-brightgreen.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A Python application to track and display mouse coordinates with both GUI and command-line interfaces.

## Screenshot

![Mouse Coordinate Tracker GUI](assets/screenshot.png)

*The modern, user-friendly interface showing real-time coordinates, tracking controls, and saved coordinates management.*

## Features

### GUI Version (PyQt5)
- Real-time mouse coordinate display
- Visual highlight overlay that follows the mouse cursor
- **Right-click to save coordinates anywhere on screen**
- **List of saved coordinates with copy/clear options**
- Configurable highlight size and update frequency
- Start/Stop tracking functionality
- Copy coordinates to clipboard
- Modern, user-friendly interface with custom icon

### Command-Line Version
- Simple terminal-based coordinate display
- Continuous tracking with live updates
- Lightweight and minimal resource usage

## Installation

### Quick Install (Recommended)

**Windows Executable Installer:**
```cmd
# Download the latest release from GitHub
# Run MouseCoordinateTracker_Windows_Installer/installer.bat as Administrator
```
Or build your own:
```cmd
git clone https://github.com/hkevin01/get-mouse-coords.git
cd get-mouse-coords
python scripts/build_windows_installer.py
```

**Linux/macOS:**
```bash
git clone https://github.com/hkevin01/get-mouse-coords.git
cd get-mouse-coords
chmod +x install.sh
./install.sh
```

**Windows (Script-based):**
```cmd
git clone https://github.com/hkevin01/get-mouse-coords.git
cd get-mouse-coords
install.bat
```

### Manual Installation

1. Clone or download the project
2. Run the setup script:
   ```bash
   cd get-mouse-coords
   ./scripts/setup.sh
   ```

## Usage

### Quick Launch Scripts

**Linux/macOS Enhanced Installer:**
```bash
./install.sh
```
This provides options to:
- Launch GUI or CLI application
- Create desktop launcher
- Install system-wide
- Generate application icons

**Windows Installer:**
```cmd
install.bat
```
Provides similar functionality with Windows-specific options.

### Manual Launch

### GUI Application
```bash
source venv/bin/activate
python src/mouse_tracker_gui.py
```

The GUI provides:
- Real-time X and Y coordinate display
- Start/Stop tracking button
- **Right-click anywhere to save current coordinates**
- **List view of all saved coordinates**
- **Copy individual or all saved coordinates**
- Highlight overlay toggle with size control
- Adjustable update frequency
- Copy coordinates button

### Command-Line Application
```bash
source venv/bin/activate
python src/mouse_tracker_cli.py
```

Press Ctrl+C to quit the command-line version.

## Requirements

- Python 3.6+
- PyQt5 (for GUI version)
- pyautogui
- pynput (for global mouse events)

## File Structure

```
get-mouse-coords/
├── src/
│   ├── mouse_tracker_gui.py         # PyQt5 GUI application
│   └── mouse_tracker_cli.py         # Command-line application
├── scripts/
│   ├── setup.sh                     # Basic setup script
│   ├── generate_icons.py            # Icon generation utility
│   ├── create_simple_icon.py        # Fallback icon creator
│   └── build_windows_installer.py   # Windows EXE builder
├── assets/
│   ├── mouse_icon.svg               # Application icon (SVG)
│   └── screenshot.png               # GUI screenshot
├── docs/                            # Documentation
├── install.sh                       # Enhanced Linux/macOS installer
├── install.bat                      # Windows batch installer
├── run.sh                           # Quick launch script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── MouseCoordinateTracker_Windows_Installer/  # Windows EXE installer package
    ├── MouseCoordinateTracker.exe   # Standalone executable
    ├── installer.bat                # Windows installer script
    └── assets/                      # Application assets
```

## GUI Features Explained

### Coordinate Display
- Shows current X and Y mouse coordinates in large, easy-to-read format
- Updates in real-time when tracking is enabled

### Saved Coordinates (NEW!)
- **Right-click anywhere on screen** while tracking to save current coordinates
- View all saved coordinates in a scrollable list
- **Copy Selected**: Copy individual coordinates from the list
- **Copy All**: Copy all saved coordinates to clipboard (one per line)
- **Clear List**: Remove all saved coordinates

### Highlight Overlay
- Optional visual circle that follows your mouse cursor
- Includes crosshair for precise positioning
- Adjustable size (20-200 pixels)
- Semi-transparent red overlay that stays on top of all windows

### Controls
- **Start/Stop Tracking**: Toggle coordinate tracking on/off
- **Copy Coordinates**: Copy current coordinates to clipboard
- **Enable Highlight**: Toggle the visual highlight overlay
- **Size**: Adjust highlight circle size
- **Update Frequency**: Control how often coordinates update (10-1000ms)

## Troubleshooting

### Building Windows Executable

To create a standalone Windows executable:

1. **Install build dependencies:**
   ```bash
   pip install pyinstaller pillow
   ```

2. **Run the builder script:**
   ```bash
   python scripts/build_windows_installer.py
   ```

3. **The script will create:**
   - `MouseCoordinateTracker.exe` - Standalone executable
   - `installer.bat` - Installation script
   - Complete installer package in `MouseCoordinateTracker_Windows_Installer/`

4. **To install on Windows:**
   - Right-click `installer.bat` and "Run as Administrator"
   - Follow the installation prompts
   - Desktop and Start Menu shortcuts will be created

### General Issues

If you encounter issues:

1. Make sure you have Python 3.6+ installed
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. On Linux, you may need additional packages for PyQt5:
   ```bash
   sudo apt-get install python3-pyqt5
   ```

## License

This project is open source and available under the MIT License.
