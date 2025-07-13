#!/usr/bin/env python3
"""
Mouse Coordinate Tracker with PyQt GUI
A GUI application to track and display mouse coordinates with visual highlighting.
Following UX Design Principles for optimal usability.
"""

import sys
import os
import subprocess
import pyautogui
from pynput import mouse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QWidget, QLabel, QPushButton,
                             QCheckBox, QGroupBox, QGridLayout,
                             QDesktopWidget, QListWidget, QListWidgetItem)
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
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
    'button': ('Segoe UI', 13, QFont.Bold),
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

# Button Styles (Fitts's Law - let size be natural)
BUTTON_STYLES = {
    'base': """
        QPushButton {{
            border-radius: 6px;
            padding: 6px 12px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
            font-weight: 600;
        }}
    """,
    'primary': """
        QPushButton {{
            background-color: {primary};
            color: white;
            border: none;
        }}
        QPushButton:hover {{ background-color: {primary_hover}; }}
        QPushButton:pressed {{ background-color: {primary_pressed}; }}
    """,
    'secondary': """
        QPushButton {{
            background-color: {surface};
            color: {primary};
            border: 2px solid {primary};
            padding: 4px 10px;
        }}
        QPushButton:hover {{ background-color: #E3F2FD; }}
        QPushButton:pressed {{ background-color: #BBDEFB; }}
    """,
    'success': """
        QPushButton {{
            background-color: {secondary};
            color: white;
            border: none;
        }}
        QPushButton:hover {{ background-color: {secondary_hover}; }}
    """,
    'danger': """
        QPushButton {{
            background-color: {danger};
            color: white;
            border: none;
        }}
        QPushButton:hover {{ background-color: {danger_hover}; }}
    """
}


def get_stylesheet(style_name):
    """Generate stylesheet by combining base and specific styles."""
    return (BUTTON_STYLES['base'] +
            BUTTON_STYLES[style_name].format(**COLORS))


def check_display_environment():
    """Check and fix common display issues."""
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'
    try:
        os.system('xhost +local: 2>/dev/null')
    except Exception:
        pass


class HighlightOverlay(QWidget):
    """Transparent overlay window to highlight mouse position."""

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.highlight_size = 50
        self.highlight_color = QColor(255, 0, 0, 150)

    def set_highlight_size(self, size):
        """Set the size of the highlight circle."""
        self.highlight_size = size

    def update_position(self, x, y):
        """Update the overlay position to center on mouse coordinates."""
        half_size = self.highlight_size // 2
        self.setGeometry(x - half_size, y - half_size,
                         self.highlight_size, self.highlight_size)
        self.update()

    def paintEvent(self, event):
        """Draw the highlight circle."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.highlight_color, 3)
        painter.setPen(pen)
        # Draw circle in the center of the widget
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawEllipse(rect)
        # Draw crosshair
        center = rect.center()
        painter.drawLine(center.x() - 5, center.y(),
                         center.x() + 5, center.y())
        painter.drawLine(center.x(), center.y() - 5,
                         center.x(), center.y() + 5)


class MouseListener(QThread):
    """A QThread that listens for global mouse clicks using pynput."""
    right_clicked = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.listener = None

    def run(self):
        """Start the mouse listener."""
        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()
        self.listener.join()  # Block until listener stops

    def on_click(self, x, y, button, pressed):
        """Callback for mouse click events."""
        if button == mouse.Button.right and pressed:
            self.right_clicked.emit(x, y)

    def stop(self):
        """Stop the mouse listener."""
        if self.listener:
            self.listener.stop()


class MouseCoordinateTracker(QMainWindow):
    """Main application window for mouse coordinate tracking."""

    def __init__(self):
        super().__init__()
        self.current_x = 0
        self.current_y = 0
        self.tracking_enabled = False
        self.highlight_enabled = False
        self.overlay = HighlightOverlay()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_coordinates)

        # Setup mouse listener thread
        self.mouse_listener = MouseListener()
        self.mouse_listener.right_clicked.connect(self.add_saved_coordinate)
        self.mouse_listener.start()

        self.init_ui()
        self.setup_timer()

    def init_ui(self):
        """Initialize the user interface following UX design principles."""
        self.setWindowTitle("Mouse Coordinate Tracker")
        self.setStyleSheet(f"background-color: {COLORS['background']};")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(SPACING['md'])
        layout.setContentsMargins(SPACING['md'], SPACING['md'],
                                  SPACING['md'], SPACING['md'])

        # Title
        title_label = QLabel("Mouse Coordinate Tracker")
        title_label.setFont(QFont(*FONTS['heading']))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Coordinate Display
        coord_group = self.create_coord_group()
        layout.addWidget(coord_group)

        # Controls
        control_group = self.create_control_group()
        layout.addWidget(control_group)

        # Status Bar
        self.status_label = self.create_status_label()
        layout.addWidget(self.status_label)

        # Saved Coordinates List
        saved_group = self.create_saved_coords_group()
        layout.addWidget(saved_group)

        layout.addStretch(1)
        self.center_window()

    def create_coord_group(self):
        """Create the coordinate display group box."""
        coord_group = QGroupBox("Current Coordinates")
        coord_layout = QGridLayout(coord_group)
        coord_layout.setSpacing(SPACING['sm'])

        self.x_label = self.create_coord_label()
        self.y_label = self.create_coord_label()

        coord_layout.addWidget(QLabel("X:"), 0, 0, Qt.AlignRight)
        coord_layout.addWidget(self.x_label, 0, 1)
        coord_layout.addWidget(QLabel("Y:"), 1, 0, Qt.AlignRight)
        coord_layout.addWidget(self.y_label, 1, 1)
        return coord_group

    def create_control_group(self):
        """Create the controls group box."""
        control_group = QGroupBox("Controls")
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(SPACING['sm'])

        self.start_button = QPushButton("Start Tracking")
        self.start_button.setStyleSheet(get_stylesheet('success'))
        self.start_button.clicked.connect(self.toggle_tracking)

        self.copy_button = QPushButton("Copy Coordinates")
        self.copy_button.setStyleSheet(get_stylesheet('secondary'))
        self.copy_button.clicked.connect(self.copy_coordinates)

        self.highlight_checkbox = QCheckBox("Enable Highlight")
        self.highlight_checkbox.toggled.connect(self.toggle_highlight)

        control_layout.addWidget(self.start_button, 0, 0)
        control_layout.addWidget(self.copy_button, 0, 1)
        control_layout.addWidget(self.highlight_checkbox, 1, 0, 1, 2,
                                 Qt.AlignCenter)
        return control_group

    def create_saved_coords_group(self):
        """Create the saved coordinates group box."""
        saved_group = QGroupBox("Saved Coordinates (Right-click to save)")
        layout = QGridLayout(saved_group)
        layout.setSpacing(SPACING['sm'])

        self.saved_coords_list = QListWidget()
        self.saved_coords_list.setStyleSheet("border-radius: 4px;")

        copy_selected_button = QPushButton("Copy Selected")
        copy_selected_button.setStyleSheet(get_stylesheet('secondary'))
        copy_selected_button.clicked.connect(self.copy_selected_coordinate)

        copy_all_button = QPushButton("Copy All")
        copy_all_button.setStyleSheet(get_stylesheet('secondary'))
        copy_all_button.clicked.connect(self.copy_all_coordinates)

        clear_button = QPushButton("Clear List")
        clear_button.setStyleSheet(get_stylesheet('danger'))
        clear_button.clicked.connect(self.saved_coords_list.clear)

        layout.addWidget(self.saved_coords_list, 0, 0, 1, 3)
        layout.addWidget(copy_selected_button, 1, 0)
        layout.addWidget(copy_all_button, 1, 1)
        layout.addWidget(clear_button, 1, 2)

        return saved_group

    def create_coord_label(self):
        """Create a styled label for displaying coordinates."""
        label = QLabel("0")
        label.setFont(QFont(*FONTS['coordinate']))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"""
            color: {COLORS['primary']};
            background-color: #FFFFFF;
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: {SPACING['xs']}px {SPACING['sm']}px;
        """)
        return label

    def create_status_label(self):
        """Create the styled status label."""
        status_label = QLabel("Ready to track mouse coordinates")
        status_font = QFont(*FONTS['status'])
        status_font.setItalic(True)
        status_label.setFont(status_font)
        status_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            padding: {SPACING['sm']}px;
            background-color: {COLORS['surface']};
            border-radius: 4px;
            border-left: 3px solid {COLORS['primary']};
        """)
        return status_label

    def center_window(self):
        """Center the window on the screen."""
        self.adjustSize()  # Let PyQt calculate the optimal size
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )

    def setup_timer(self):
        """Setup the timer with initial interval."""
        self.timer.setInterval(50)

    def toggle_tracking(self):
        """Start or stop coordinate tracking."""
        if self.tracking_enabled:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        """Start tracking mouse coordinates with visual feedback."""
        self.tracking_enabled = True
        self.timer.start()
        self.start_button.setText("Stop Tracking")
        self.start_button.setStyleSheet(get_stylesheet('danger'))
        self.update_status("🔴 Tracking mouse coordinates...", 'secondary')

    def stop_tracking(self):
        """Stop tracking mouse coordinates."""
        self.tracking_enabled = False
        self.timer.stop()
        if self.highlight_enabled:
            self.overlay.hide()
        self.start_button.setText("Start Tracking")
        self.start_button.setStyleSheet(get_stylesheet('success'))
        self.update_status("⏹️ Tracking stopped.", 'primary')

    def toggle_highlight(self, checked):
        """Enable or disable mouse position highlighting."""
        self.highlight_enabled = checked
        if not checked:
            self.overlay.hide()
        elif self.tracking_enabled:
            self.overlay.show()

    def update_coordinates(self):
        """Update the displayed coordinates."""
        try:
            x, y = pyautogui.position()
            self.current_x, self.current_y = x, y
            self.x_label.setText(str(x))
            self.y_label.setText(str(y))
            if self.highlight_enabled:
                if not self.overlay.isVisible():
                    self.overlay.show()
                self.overlay.update_position(x, y)
        except Exception as e:
            self.update_status(f"Error: {e}", 'danger')

    def copy_coordinates(self):
        """Copy current coordinates to clipboard with feedback."""
        coords_text = f"{self.current_x}, {self.current_y}"
        QApplication.clipboard().setText(coords_text)
        self.update_status(f"📋 Copied: {coords_text}", 'success')
        QTimer.singleShot(3000, self.reset_status)

    def reset_status(self):
        """Reset status to its default state based on tracking status."""
        if self.tracking_enabled:
            self.update_status("🔴 Tracking mouse coordinates...", 'secondary')
        else:
            self.update_status("Ready to track.", 'primary')

    def update_status(self, text, style_color_name):
        """Update the status label's text and style."""
        color = COLORS.get(style_color_name, COLORS['primary'])
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            padding: {SPACING['sm']}px;
            background-color: {COLORS['surface']};
            border-radius: 4px;
            border-left: 3px solid {color};
        """)

    def add_saved_coordinate(self, x, y):
        """Add the given coordinates to the saved list."""
        if self.tracking_enabled:
            coord_text = f"X: {x}, Y: {y}"
            self.saved_coords_list.addItem(QListWidgetItem(coord_text))
            self.update_status(f"💾 Saved: {coord_text}", 'primary')
            QTimer.singleShot(3000, self.reset_status)

    def copy_selected_coordinate(self):
        """Copy the selected coordinate from the list."""
        selected_items = self.saved_coords_list.selectedItems()
        if not selected_items:
            self.update_status("⚠️ No coordinate selected to copy.", 'danger')
            QTimer.singleShot(3000, self.reset_status)
            return

        coord_text = selected_items[0].text()
        QApplication.clipboard().setText(coord_text)
        self.update_status(f"📋 Copied selected: {coord_text}", 'success')
        QTimer.singleShot(3000, self.reset_status)

    def copy_all_coordinates(self):
        """Copy all saved coordinates to the clipboard."""
        if self.saved_coords_list.count() == 0:
            self.update_status("⚠️ No coordinates to copy.", 'danger')
            QTimer.singleShot(3000, self.reset_status)
            return

        all_coords = [self.saved_coords_list.item(i).text()
                      for i in range(self.saved_coords_list.count())]
        clipboard_text = "\n".join(all_coords)
        QApplication.clipboard().setText(clipboard_text)
        self.update_status("📋 Copied all saved coordinates.", 'success')
        QTimer.singleShot(3000, self.reset_status)

    def closeEvent(self, event):
        """Handle application close event."""
        self.mouse_listener.stop()
        self.timer.stop()
        self.overlay.close()
        event.accept()


def main():
    """Main application entry point."""
    check_display_environment()
    pyautogui.FAILSAFE = False

    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        window = MouseCoordinateTracker()
        window.show()
        print("✅ GUI Application started successfully!")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ Error starting GUI application: {e}")
        print("\n💡 Falling back to command-line version...")
        try:
            subprocess.run([sys.executable, "src/mouse_tracker_cli.py"],
                           check=True)
        except Exception:
            print("❌ Could not start command-line version.")
            sys.exit(1)


if __name__ == "__main__":
    main()
