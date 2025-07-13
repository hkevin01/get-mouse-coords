#!/usr/bin/env python3
"""
Icon Generator for Mouse Coordinate Tracker
Converts SVG icon to PNG formats for GUI use
"""

import os
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QSize

def create_png_icon(svg_path, png_path, size=(64, 64)):
    """Convert SVG to PNG with specified size."""
    try:
        # Create SVG renderer
        renderer = QSvgRenderer(svg_path)
        
        # Create pixmap
        pixmap = QPixmap(QSize(*size))
        pixmap.fill()  # Fill with transparent background
        
        # Render SVG to pixmap
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Save as PNG
        pixmap.save(png_path, "PNG")
        print(f"✅ Created {png_path} ({size[0]}x{size[1]})")
        return True
        
    except Exception as e:
        print(f"❌ Error creating {png_path}: {e}")
        return False

def main():
    """Generate PNG icons from SVG."""
    # Ensure assets directory exists
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    svg_file = os.path.join(assets_dir, "mouse_icon.svg")
    
    if not os.path.exists(svg_file):
        print(f"❌ SVG file not found: {svg_file}")
        return
    
    # Generate different sizes
    sizes = [
        (16, 16),   # Small icon
        (32, 32),   # Medium icon
        (64, 64),   # Large icon
        (128, 128), # High DPI
    ]
    
    for width, height in sizes:
        png_file = os.path.join(assets_dir, f"mouse_icon_{width}x{height}.png")
        create_png_icon(svg_file, png_file, (width, height))

if __name__ == "__main__":
    main()
