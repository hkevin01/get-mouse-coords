# Mouse Coordinate Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/doc/versions/)
[![Made with PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-brightgreen.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A Python application to track and display mouse coordinates with both GUI and command-line interfaces.

## Features

### GUI Version (PyQt5)
- Real-time mouse coordinate display
- Visual highlight overlay that follows the mouse cursor
- Configurable highlight size and update frequency
- Start/Stop tracking functionality
- Copy coordinates to clipboard
- Modern, user-friendly interface

### Command-Line Version
- Simple terminal-based coordinate display
- Continuous tracking with live updates
- Lightweight and minimal resource usage

## Installation

1. Clone or download the project
2. Run the setup script:
   ```bash
   cd get-mouse-coords
   ./scripts/setup.sh
   ```

## Usage

### GUI Application
```bash
source venv/bin/activate
python src/mouse_tracker_gui.py
```

The GUI provides:
- Real-time X and Y coordinate display
- Start/Stop tracking button
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

## File Structure

```
get-mouse-coords/
├── src/
│   ├── mouse_tracker_gui.py    # PyQt5 GUI application
│   └── mouse_tracker_cli.py    # Command-line application
├── scripts/
│   └── setup.sh               # Setup script
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## GUI Features Explained

### Coordinate Display
- Shows current X and Y mouse coordinates in large, easy-to-read format
- Updates in real-time when tracking is enabled

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

If you encounter issues:

1. Make sure you have Python 3.6+ installed
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. On Linux, you may need additional packages for PyQt5:
   ```bash
   sudo apt-get install python3-pyqt5
   ```

## License

This project is open source and available under the MIT License.
