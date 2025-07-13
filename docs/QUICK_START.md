# Quick Start Guide

## Installation & Setup

1. **Navigate to project directory**:
   ```bash
   cd /home/kevin/Projects/get-mouse-coords
   ```

2. **Run setup script**:
   ```bash
   ./scripts/setup.sh
   ```

3. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

## Running the Applications

### Option 1: Use the Launcher (Recommended)
```bash
python scripts/launcher.py
```
Then choose:
- `1` for GUI application
- `2` for command-line application
- `3` to exit

### Option 2: Direct Execution

#### GUI Application
```bash
python src/mouse_tracker_gui.py
```

#### Command-Line Application
```bash
python src/mouse_tracker_cli.py
```

## Quick GUI Tutorial

1. **Start the GUI**: Use launcher option 1 or run directly
2. **Begin tracking**: Click "Start Tracking" button
3. **Watch coordinates**: Move your mouse to see real-time X,Y updates
4. **Enable highlight**: Check "Enable Highlight" for visual mouse tracking
5. **Adjust settings**: 
   - Change highlight size with the size spinner
   - Modify update frequency for performance tuning
6. **Copy coordinates**: Click "Copy Coordinates" to copy current position
7. **Stop tracking**: Click "Stop Tracking" when done

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Make sure virtual environment is activated
   - Re-run setup script: `./scripts/setup.sh`

2. **GUI doesn't start**:
   - Ensure you have a display server running
   - Try installing system PyQt5: `sudo apt-get install python3-pyqt5`

3. **Permission errors**:
   - Make scripts executable: `chmod +x scripts/*.sh scripts/*.py`

4. **High CPU usage**:
   - Increase update frequency in GUI (higher ms = lower CPU usage)
   - Default 50ms should be fine for most systems

### System Requirements
- Python 3.6 or higher
- Linux with X11 or Wayland display server
- For GUI: PyQt5 and system display libraries

## Tips for Best Performance

1. **Adjust update frequency**: Higher values (100-200ms) for lower CPU usage
2. **Disable highlight**: When not needed, turn off highlight overlay
3. **Use CLI version**: For minimal resource usage, use command-line version
