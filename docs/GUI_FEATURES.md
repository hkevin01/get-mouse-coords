# GUI Features Documentation

## Main Window

The PyQt5 GUI application provides a comprehensive interface for mouse coordinate tracking with the following sections:

### 1. Current Coordinates Display
- **X Coordinate**: Large, bold display of current mouse X position
- **Y Coordinate**: Large, bold display of current mouse Y position
- Color-coded with blue text and light gray background for easy reading

### 2. Control Panel

#### Tracking Controls
- **Start Tracking Button**: 
  - Green when stopped, click to start tracking
  - Red when active, click to stop tracking
- **Copy Coordinates Button**: Copies current X,Y coordinates to clipboard

#### Highlight Options
- **Enable Highlight Checkbox**: Toggle visual mouse position highlighting
- **Size Spinner**: Adjust highlight circle size (20-200 pixels)
- **Update Frequency**: Control how often coordinates update (10-1000 milliseconds)

### 3. Visual Highlight Overlay

When enabled, a semi-transparent red circle with crosshairs follows your mouse cursor:
- **Always on top**: Visible over all other applications
- **Mouse transparent**: Won't interfere with clicking
- **Customizable size**: Adjustable from 20 to 200 pixels
- **Crosshair center**: Precise positioning indicator

### 4. Status Bar
Shows current application status and copied coordinate information.

## Keyboard Shortcuts
- **Ctrl+C**: In CLI mode, quit the application
- **Copy button**: In GUI mode, copy coordinates to clipboard

## Use Cases

### For Designers
- **UI Element Positioning**: Get exact pixel coordinates for design layouts
- **Screenshot Annotation**: Mark specific points in images
- **Grid Alignment**: Ensure precise element positioning

### For Developers
- **Testing UI Elements**: Verify exact positioning of interface components
- **Game Development**: Get coordinates for sprite positioning
- **Automation Scripts**: Record mouse positions for automation

### For General Users
- **Screen Measurements**: Measure distances between screen elements
- **Reference Points**: Mark specific locations for later reference
- **Troubleshooting**: Report exact mouse positions for support
