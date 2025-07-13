#!/usr/bin/env python3
"""
Mouse Coordinate Tracker with PyQt GUI
A GUI application to track and display mouse coordinates with visual highlighting.
Following UX Design Principles for optimal usability.
"""

import sys
import os
import pyautogui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QPushButton, 
                             QCheckBox, QSpinBox, QGroupBox, QGridLayout,
                             QDesktopWidget)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QPainter, QPen

# Design System Constants (Following Laws of UX)
COLORS = {
    'primary': '#1976D2',          # Material Blue 700
    'primary_hover': '#1565C0',    # Material Blue 800
    'primary_pressed': '#0D47A1',  # Material Blue 900
    'secondary': '#388E3C',        # Material Green 700
    'secondary_hover': '#2E7D32',  # Material Green 800
    'danger': '#D32F2F',           # Material Red 700
    'danger_hover': '#C62828',     # Material Red 800
    'surface': '#FFFFFF',          # White
    'background': '#F5F5F5',       # Light Gray
    'text_primary': '#212121',     # Dark Gray
    'text_secondary': '#757575',   # Medium Gray
    'border': '#E0E0E0'            # Light Border
}

FONTS = {
    'heading': ('Segoe UI', 16, QFont.Bold),
    'coordinate': ('Consolas', 14, QFont.Bold),
    'button': ('Segoe UI', 14, QFont.Bold),
    'label': ('Segoe UI', 12, QFont.Normal),
    'status': ('Segoe UI', 11, QFont.Normal)
}

# Spacing System (8px base unit)
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32
}

# Button Styles (Following Fitts's Law - balanced sizing)
BUTTON_STYLES = {
    'primary': f"""
        QPushButton {{
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 5px 12px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 600;
            min-height: 32px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['primary_hover']};
        }}
        QPushButton:pressed {{
            background-color: {COLORS['primary_pressed']};
        }}
    """,
    'secondary': f"""
        QPushButton {{
            background-color: {COLORS['surface']};
            color: {COLORS['primary']};
            border: 2px solid {COLORS['primary']};
            border-radius: 6px;
            padding: 3px 10px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 600;
            min-height: 30px;
        }}
        QPushButton:hover {{
            background-color: #E3F2FD;
        }}
        QPushButton:pressed {{
            background-color: #BBDEFB;
        }}
    """,
    'success': f"""
        QPushButton {{
            background-color: {COLORS['secondary']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 5px 12px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 600;
            min-height: 32px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['secondary_hover']};
        }}
    """,
    'danger': f"""
        QPushButton {{
            background-color: {COLORS['danger']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 5px 12px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 600;
            min-height: 32px;
        }}
        QPushButton:hover {{
            background-color: {COLORS['danger_hover']};
        }}
    """
}

# Handle display environment
try:
    import os
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'
except Exception:
    pass
import os


def check_display_environment():
    """Check and fix common display issues"""
    # Set DISPLAY if not set (common in some environments)
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'
    
    # Try to fix X11 authorization issues
    try:
        # This helps with some authorization issues
        os.system('xhost +local: 2>/dev/null')
    except:
        pass


class HighlightOverlay(QWidget):
    """Transparent overlay window to highlight mouse position"""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setGeometry(0, 0, 100, 100)
        self.highlight_size = 50
        self.highlight_color = QColor(255, 0, 0, 150)  # Red with transparency
        
    def set_highlight_size(self, size):
        """Set the size of the highlight circle"""
        self.highlight_size = size
        self.setGeometry(0, 0, size * 2, size * 2)
        
    def set_highlight_color(self, color):
        """Set the color of the highlight circle"""
        self.highlight_color = color
        
    def update_position(self, x, y):
        """Update the overlay position to center on mouse coordinates"""
        half_size = self.highlight_size
        self.move(x - half_size, y - half_size)
        self.update()
        
    def paintEvent(self, event):
        """Draw the highlight circle"""
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
        
    def init_ui(self):
        """Initialize the user interface following UX design principles"""
        self.setWindowTitle("Mouse Coordinate Tracker")
        self.setStyleSheet(f"background-color: {COLORS['background']};")
        
        # Set a sensible default size, but allow resizing
        self.resize(480, 430)
        
        # Center the window
        self.center_window()
        
        # Create main widget and layout with balanced spacing
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(SPACING['md'])  # Consistent vertical spacing
        layout.setContentsMargins(SPACING['md'], SPACING['md'],
                                  SPACING['md'], SPACING['md'])
        
        # Title section
        title_label = QLabel("Mouse Coordinate Tracker")
        title_font = QFont(*FONTS['heading'])
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            padding: {SPACING['sm']}px;
            background-color: {COLORS['surface']};
            border-radius: 8px;
        """)
        layout.addWidget(title_label)
        
        # Coordinate display section (Law of Proximity)
        coord_group = QGroupBox("Current Coordinates")
        coord_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                color: {COLORS['text_primary']};
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px;
            }}
        """)
        coord_layout = QGridLayout(coord_group)
        coord_layout.setSpacing(SPACING['md'])
        coord_layout.setContentsMargins(SPACING['md'], SPACING['md'] + 5,
                                        SPACING['md'], SPACING['md'])
        
        # X coordinate row
        x_label_text = QLabel("X:")
        x_label_text.setFont(QFont(*FONTS['label']))
        x_label_text.setStyleSheet(f"color: {COLORS['text_secondary']};")
        coord_layout.addWidget(
            x_label_text, 0, 0, Qt.AlignRight | Qt.AlignVCenter
        )
        
        self.x_label = QLabel("0")
        coord_font = QFont(*FONTS['coordinate'])
        self.x_label.setFont(coord_font)
        self.x_label.setStyleSheet(f"""
            color: {COLORS['primary']};
            background-color: #F8F9FA;
            padding: {SPACING['xs']}px;
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            min-width: 120px;
            min-height: 32px;
        """)
        self.x_label.setAlignment(Qt.AlignCenter)
        coord_layout.addWidget(self.x_label, 0, 1)
        
        # Y coordinate row
        y_label_text = QLabel("Y:")
        y_label_text.setFont(QFont(*FONTS['label']))
        y_label_text.setStyleSheet(f"color: {COLORS['text_secondary']};")
        coord_layout.addWidget(
            y_label_text, 1, 0, Qt.AlignRight | Qt.AlignVCenter
        )
        
        self.y_label = QLabel("0")
        self.y_label.setFont(coord_font)
        self.y_label.setStyleSheet(f"""
            color: {COLORS['primary']};
            background-color: #F8F9FA;
            padding: {SPACING['xs']}px;
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
            min-width: 120px;
            min-height: 32px;
        """)
        self.y_label.setAlignment(Qt.AlignCenter)
        coord_layout.addWidget(self.y_label, 1, 1)
        
        layout.addWidget(coord_group)
        
        # Control section (Law of Proximity + Fitts's Law)
        control_group = QGroupBox("Controls")
        control_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                color: {COLORS['text_primary']};
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 2px 8px;
            }}
        """)
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(SPACING['md'])
        control_layout.setContentsMargins(SPACING['md'], SPACING['md'] + 5,
                                          SPACING['md'], SPACING['md'])
        
        # Main action buttons (Fitts's Law)
        self.start_button = QPushButton("Start Tracking")
        self.start_button.setStyleSheet(BUTTON_STYLES['success'])
        self.start_button.clicked.connect(self.toggle_tracking)
        control_layout.addWidget(self.start_button, 0, 0)
        
        self.copy_button = QPushButton("Copy Coordinates")
        self.copy_button.setStyleSheet(BUTTON_STYLES['secondary'])
        self.copy_button.clicked.connect(self.copy_coordinates)
        control_layout.addWidget(self.copy_button, 0, 1)
        
        # Settings row (Law of Proximity)
        self.highlight_checkbox = QCheckBox("Enable Highlight")
        self.highlight_checkbox.toggled.connect(self.toggle_highlight)
        # Span 2 columns and align center
        control_layout.addWidget(
            self.highlight_checkbox, 1, 0, 1, 2, Qt.AlignCenter
        )
        
        # Size and Rate controls
        size_rate_layout = QHBoxLayout()
        size_rate_layout.setSpacing(SPACING['md'])
        
        size_label = QLabel("Size:")
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(20, 200)
        self.size_spinbox.setValue(50)
        
        freq_label = QLabel("Rate (ms):")
        self.freq_spinbox = QSpinBox()
        self.freq_spinbox.setRange(10, 1000)
        self.freq_spinbox.setValue(50)

        size_rate_layout.addWidget(size_label)
        size_rate_layout.addWidget(self.size_spinbox)
        size_rate_layout.addWidget(freq_label)
        size_rate_layout.addWidget(self.freq_spinbox)
        size_rate_layout.addStretch()
        
        # Span 2 columns
        control_layout.addLayout(size_rate_layout, 2, 0, 1, 2)
        
        layout.addWidget(control_group)
        
        # Status section (Zeigarnik Effect - feedback)
        self.status_label = QLabel("Ready to track mouse coordinates")
        status_font = QFont('Segoe UI', 11, QFont.Normal)
        status_font.setItalic(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            padding: {SPACING['sm']}px;
            background-color: {COLORS['surface']};
            border-radius: 4px;
            border-left: 3px solid {COLORS['primary']};
            min-height: 20px;
        """)
        layout.addWidget(self.status_label)
        
        # Add a stretch to push content to the top and prevent loose spacing
        layout.addStretch(1)
        
    def center_window(self):
        """Center the window on the screen"""
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
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
        """Start tracking mouse coordinates with visual feedback"""
        self.tracking_enabled = True
        self.timer.start()
        
        # Update button appearance (Goal-Gradient Effect)
        self.start_button.setText("Stop Tracking")
        self.start_button.setStyleSheet(BUTTON_STYLES['danger'])
        
        # Update status (Zeigarnik Effect)
        self.status_label.setText("🔴 Tracking mouse coordinates...")
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            padding: {SPACING['sm']}px;
            background-color: #FFF3E0;
            border-radius: 4px;
            border-left: 3px solid {COLORS['secondary']};
            font-weight: 500;
        """)
        
    def stop_tracking(self):
        """Stop tracking mouse coordinates"""
        self.tracking_enabled = False
        self.timer.stop()
        
        # Hide overlay
        if self.highlight_enabled:
            self.overlay.hide()
            
        # Reset button appearance
        self.start_button.setText("Start Tracking")
        self.start_button.setStyleSheet(BUTTON_STYLES['success'])
        
        # Update status
        self.status_label.setText("⏹️ Tracking stopped - Ready to start again")
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            padding: {SPACING['sm']}px;
            background-color: {COLORS['surface']};
            border-radius: 4px;
            border-left: 3px solid {COLORS['primary']};
        """)
        
    def toggle_highlight(self, checked):
        """Enable or disable mouse position highlighting"""
        self.highlight_enabled = checked
        if not checked:
            self.overlay.hide()
        elif self.tracking_enabled:
            self.overlay.show()
            
    def update_highlight_size(self, size):
        """Update the size of the highlight overlay"""
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
            x, y = pyautogui.position()
            self.current_x = x
            self.current_y = y
            
            # Update display
            self.x_label.setText(str(x))
            self.y_label.setText(str(y))
            
            # Update highlight overlay if enabled
            if self.highlight_enabled:
                if not self.overlay.isVisible():
                    self.overlay.show()
                self.overlay.update_position(x, y)
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            
    def copy_coordinates(self):
        """Copy current coordinates to clipboard with feedback"""
        coords_text = f"{self.current_x}, {self.current_y}"
        QApplication.clipboard().setText(coords_text)
        
        # Provide immediate feedback (Doherty Threshold)
        self.status_label.setText(f"📋 Copied coordinates: {coords_text}")
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            padding: {SPACING['sm']}px;
            background-color: #E8F5E8;
            border-radius: 4px;
            border-left: 3px solid {COLORS['secondary']};
            font-weight: 500;
        """)
        
        # Reset status after 3 seconds
        QTimer.singleShot(3000, self.reset_status)
        
    def reset_status(self):
        """Reset status to default state"""
        if self.tracking_enabled:
            self.status_label.setText("🔴 Tracking mouse coordinates...")
            self.status_label.setStyleSheet(f"""
                color: {COLORS['text_primary']};
                padding: {SPACING['sm']}px;
                background-color: #FFF3E0;
                border-radius: 4px;
                border-left: 3px solid {COLORS['secondary']};
                font-weight: 500;
            """)
        else:
            self.status_label.setText("Ready to track mouse coordinates")
            self.status_label.setStyleSheet(f"""
                color: {COLORS['text_secondary']};
                padding: {SPACING['sm']}px;
                background-color: {COLORS['surface']};
                border-radius: 4px;
                border-left: 3px solid {COLORS['primary']};
            """)
        
    def closeEvent(self, event):
        """Handle application close event"""
        if self.timer.isActive():
            self.timer.stop()
        if self.overlay.isVisible():
            self.overlay.close()
        event.accept()


def main():
    """Main application entry point"""
    # Check and fix display environment
    check_display_environment()
    
    # Disable pyautogui fail-safe for better user experience
    pyautogui.FAILSAFE = False
    
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Mouse Coordinate Tracker")
        
        # Set application style
        app.setStyle('Fusion')
        
        # Create and show main window
        window = MouseCoordinateTracker()
        window.show()
        
        print("✅ GUI Application started successfully!")
        print("🎯 Use the interface to start tracking mouse coordinates")
        
        # Run application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Error starting GUI application: {e}")
        print("")
        print("💡 Possible solutions:")
        print("1. Try: export DISPLAY=:0")
        print("2. Use SSH with X11 forwarding: ssh -X")
        print("3. Install X11 server if using WSL")
        print("4. Run the command-line version instead")
        print("")
        print("🔄 Attempting to start command-line version...")
        
        # Fallback to CLI version
        try:
            import subprocess
            subprocess.run([sys.executable, "src/mouse_tracker_cli.py"])
        except Exception:
            print("❌ Could not start command-line version either")
            sys.exit(1)


if __name__ == "__main__":
    main()
