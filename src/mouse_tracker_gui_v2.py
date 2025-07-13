#!/usr/bin/env python3
"""
Mouse Coordinate Tracker with PyQt GUI - Enhanced Version
A GUI application to track and display mouse coordinates with visual highlighting.
Includes better error handling for display and permission issues.
"""

import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QCheckBox, QSpinBox,
                             QGroupBox, QGridLayout, QMessageBox, QTextEdit)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPen
from PyQt5.QtWidgets import QDesktopWidget

# Try different mouse libraries for better compatibility
MOUSE_LIB = None
try:
    import pyautogui
    MOUSE_LIB = 'pyautogui'
    # Disable fail-safe for better user experience
    pyautogui.FAILSAFE = False
except Exception as e:
    try:
        from pynput import mouse
        MOUSE_LIB = 'pynput'
    except Exception as e2:
        print(f"Error importing mouse libraries:")
        print(f"  pyautogui: {e}")
        print(f"  pynput: {e2}")
        print("Please install required packages: pip install pyautogui pynput")
        sys.exit(1)


def get_mouse_position():
    """Get mouse position using available library"""
    if MOUSE_LIB == 'pyautogui':
        try:
            return pyautogui.position()
        except Exception:
            # Fallback to pynput if pyautogui fails
            try:
                from pynput import mouse
                controller = mouse.Controller()
                return controller.position
            except Exception:
                return (0, 0)
    elif MOUSE_LIB == 'pynput':
        try:
            controller = mouse.Controller()
            return controller.position
        except Exception:
            return (0, 0)
    return (0, 0)


class HighlightOverlay(QWidget):
    """Transparent overlay window to highlight mouse position"""
    
    def __init__(self):
        super().__init__()
        try:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.setGeometry(0, 0, 100, 100)
            self.highlight_size = 50
            self.highlight_color = QColor(255, 0, 0, 150)  # Red with transparency
            self.is_working = True
        except Exception as e:
            print(f"Warning: Overlay may not work properly: {e}")
            self.is_working = False
        
    def set_highlight_size(self, size):
        """Set the size of the highlight circle"""
        self.highlight_size = size
        self.setGeometry(0, 0, size * 2, size * 2)
        
    def set_highlight_color(self, color):
        """Set the color of the highlight circle"""
        self.highlight_color = color
        
    def update_position(self, x, y):
        """Update the overlay position to center on mouse coordinates"""
        if not self.is_working:
            return
        try:
            half_size = self.highlight_size
            self.move(int(x - half_size), int(y - half_size))
            self.update()
        except Exception:
            pass
        
    def paintEvent(self, event):
        """Draw the highlight circle"""
        if not self.is_working:
            return
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Draw outer circle
            pen = QPen(self.highlight_color, 3)
            painter.setPen(pen)
            center = self.highlight_size
            painter.drawEllipse(center - self.highlight_size//2, center - self.highlight_size//2, 
                              self.highlight_size, self.highlight_size)
            
            # Draw crosshair
            painter.drawLine(center - self.highlight_size//3, center, 
                            center + self.highlight_size//3, center)
            painter.drawLine(center, center - self.highlight_size//3, 
                            center, center + self.highlight_size//3)
        except Exception:
            pass


class MouseCoordinateTracker(QMainWindow):
    """Main application window for mouse coordinate tracking"""
    
    def __init__(self):
        super().__init__()
        self.current_x = 0
        self.current_y = 0
        self.tracking_enabled = False
        self.highlight_enabled = False
        
        # Create highlight overlay
        self.overlay = HighlightOverlay()
        
        # Setup timer for coordinate updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_coordinates)
        
        self.init_ui()
        self.setup_timer()
        
        # Show library info
        self.show_library_info()
        
    def show_library_info(self):
        """Show which mouse library is being used"""
        lib_msg = f"Using {MOUSE_LIB} for mouse tracking"
        if not self.overlay.is_working:
            lib_msg += " (overlay disabled due to display issues)"
        self.status_label.setText(lib_msg)
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Mouse Coordinate Tracker")
        self.setFixedSize(450, 350)
        
        # Center the window
        self.center_window()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Coordinate display section
        coord_group = QGroupBox("Current Coordinates")
        coord_layout = QGridLayout(coord_group)
        
        # X coordinate
        coord_layout.addWidget(QLabel("X:"), 0, 0)
        self.x_label = QLabel("0")
        self.x_label.setFont(QFont("Courier", 16, QFont.Bold))
        self.x_label.setStyleSheet("color: blue; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        self.x_label.setAlignment(Qt.AlignCenter)
        coord_layout.addWidget(self.x_label, 0, 1)
        
        # Y coordinate
        coord_layout.addWidget(QLabel("Y:"), 1, 0)
        self.y_label = QLabel("0")
        self.y_label.setFont(QFont("Courier", 16, QFont.Bold))
        self.y_label.setStyleSheet("color: blue; background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        self.y_label.setAlignment(Qt.AlignCenter)
        coord_layout.addWidget(self.y_label, 1, 1)
        
        layout.addWidget(coord_group)
        
        # Control section
        control_group = QGroupBox("Controls")
        control_layout = QVBoxLayout(control_group)
        
        # Start/Stop tracking
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Tracking")
        self.start_button.clicked.connect(self.toggle_tracking)
        self.start_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        button_layout.addWidget(self.start_button)
        
        self.copy_button = QPushButton("Copy Coordinates")
        self.copy_button.clicked.connect(self.copy_coordinates)
        self.copy_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 8px; }")
        button_layout.addWidget(self.copy_button)
        
        control_layout.addLayout(button_layout)
        
        # Highlight options
        highlight_layout = QHBoxLayout()
        self.highlight_checkbox = QCheckBox("Enable Highlight")
        self.highlight_checkbox.toggled.connect(self.toggle_highlight)
        # Disable if overlay doesn't work
        if not self.overlay.is_working:
            self.highlight_checkbox.setEnabled(False)
            self.highlight_checkbox.setToolTip("Highlight disabled due to display compatibility issues")
        highlight_layout.addWidget(self.highlight_checkbox)
        
        highlight_layout.addWidget(QLabel("Size:"))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(20, 200)
        self.size_spinbox.setValue(50)
        self.size_spinbox.valueChanged.connect(self.update_highlight_size)
        if not self.overlay.is_working:
            self.size_spinbox.setEnabled(False)
        highlight_layout.addWidget(self.size_spinbox)
        
        control_layout.addLayout(highlight_layout)
        
        # Update frequency
        freq_layout = QHBoxLayout()
        freq_layout.addWidget(QLabel("Update Frequency (ms):"))
        self.freq_spinbox = QSpinBox()
        self.freq_spinbox.setRange(10, 1000)
        self.freq_spinbox.setValue(50)
        self.freq_spinbox.valueChanged.connect(self.update_timer_interval)
        freq_layout.addWidget(self.freq_spinbox)
        
        control_layout.addLayout(freq_layout)
        
        layout.addWidget(control_group)
        
        # Debug info section
        debug_group = QGroupBox("Debug Information")
        debug_layout = QVBoxLayout(debug_group)
        
        self.debug_text = QTextEdit()
        self.debug_text.setMaximumHeight(80)
        self.debug_text.setReadOnly(True)
        self.debug_text.setStyleSheet("font-family: Courier; font-size: 10px;")
        debug_layout.addWidget(self.debug_text)
        
        layout.addWidget(debug_group)
        
        # Status section
        self.status_label = QLabel("Ready to track mouse coordinates")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Update debug info
        self.update_debug_info()
        
    def update_debug_info(self):
        """Update debug information display"""
        debug_info = []
        debug_info.append(f"Mouse Library: {MOUSE_LIB}")
        debug_info.append(f"Overlay Working: {self.overlay.is_working}")
        debug_info.append(f"Display: {os.environ.get('DISPLAY', 'Not set')}")
        debug_info.append(f"Python: {sys.version.split()[0]}")
        
        self.debug_text.setText("\n".join(debug_info))
        
    def center_window(self):
        """Center the window on the screen"""
        try:
            screen = QDesktopWidget().screenGeometry()
            size = self.geometry()
            self.move(
                (screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2
            )
        except Exception:
            pass  # If centering fails, just use default position
    
    def setup_timer(self):
        """Setup the timer with initial interval"""
        self.timer.setInterval(50)  # 50ms = 20 FPS
        
    def toggle_tracking(self):
        """Start or stop coordinate tracking"""
        if self.tracking_enabled:
            self.stop_tracking()
        else:
            self.start_tracking()
            
    def start_tracking(self):
        """Start tracking mouse coordinates"""
        self.tracking_enabled = True
        self.timer.start()
        self.start_button.setText("Stop Tracking")
        self.start_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 8px; }")
        self.status_label.setText("Tracking mouse coordinates...")
        
    def stop_tracking(self):
        """Stop tracking mouse coordinates"""
        self.tracking_enabled = False
        self.timer.stop()
        if self.highlight_enabled and self.overlay.is_working:
            self.overlay.hide()
        self.start_button.setText("Start Tracking")
        self.start_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        self.status_label.setText("Tracking stopped")
        
    def toggle_highlight(self, checked):
        """Enable or disable mouse position highlighting"""
        if not self.overlay.is_working:
            return
        self.highlight_enabled = checked
        if not checked:
            self.overlay.hide()
        elif self.tracking_enabled:
            self.overlay.show()
            
    def update_highlight_size(self, size):
        """Update the size of the highlight overlay"""
        if self.overlay.is_working:
            self.overlay.set_highlight_size(size)
        
    def update_timer_interval(self, interval):
        """Update the timer interval for coordinate updates"""
        if self.timer.isActive():
            self.timer.setInterval(interval)
        else:
            self.timer.setInterval(interval)
            
    def update_coordinates(self):
        """Update the displayed coordinates"""
        try:
            # Get current mouse position
            x, y = get_mouse_position()
            self.current_x = int(x)
            self.current_y = int(y)
            
            # Update display
            self.x_label.setText(str(self.current_x))
            self.y_label.setText(str(self.current_y))
            
            # Update highlight overlay if enabled
            if self.highlight_enabled and self.overlay.is_working:
                if not self.overlay.isVisible():
                    self.overlay.show()
                self.overlay.update_position(x, y)
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            
    def copy_coordinates(self):
        """Copy current coordinates to clipboard"""
        coords_text = f"{self.current_x}, {self.current_y}"
        try:
            QApplication.clipboard().setText(coords_text)
            self.status_label.setText(f"Copied coordinates: {coords_text}")
        except Exception as e:
            self.status_label.setText(f"Error copying: {str(e)}")
        
    def closeEvent(self, event):
        """Handle application close event"""
        if self.timer.isActive():
            self.timer.stop()
        if self.overlay.is_working and self.overlay.isVisible():
            self.overlay.close()
        event.accept()


def check_display():
    """Check if display is available and provide helpful error messages"""
    if os.environ.get('DISPLAY') is None:
        return False, "No DISPLAY environment variable set"
    
    try:
        # Try to create a minimal Qt application to test display
        test_app = QApplication([])
        test_app.quit()
        return True, "Display OK"
    except Exception as e:
        return False, str(e)


def main():
    """Main application entry point"""
    print("🖱️  Mouse Coordinate Tracker GUI")
    print("=" * 40)
    
    # Check display availability
    display_ok, display_msg = check_display()
    if not display_ok:
        print(f"❌ Display Issue: {display_msg}")
        print("")
        print("💡 Possible solutions:")
        print("1. If using SSH: ssh -X username@hostname")
        print("2. If using WSL: Install X11 server (VcXsrv/Xming)")
        print("3. Set DISPLAY variable: export DISPLAY=:0")
        print("4. Use the command-line version instead")
        print("")
        
        # Offer to run CLI version
        try:
            response = input("Run command-line version instead? (y/n): ").lower()
            if response in ['y', 'yes']:
                from . import mouse_tracker_cli
                mouse_tracker_cli.main()
                return
        except (KeyboardInterrupt, ImportError):
            pass
        sys.exit(1)
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Mouse Coordinate Tracker")
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MouseCoordinateTracker()
        window.show()
        
        print(f"✅ GUI launched successfully using {MOUSE_LIB}")
        print("🎯 Click 'Start Tracking' to begin coordinate tracking")
        
        # Run application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("💡 Try running the command-line version instead")
        sys.exit(1)


if __name__ == "__main__":
    main()
