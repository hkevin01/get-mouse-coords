# Simple Python script to create a basic mouse icon as PNG
from PIL import Image, ImageDraw
import os

def create_mouse_icon():
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Create a 64x64 image with transparent background
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw mouse body (ellipse)
    draw.ellipse([14, 20, 50, 60], fill=(44, 62, 80), outline=(52, 73, 94))
    
    # Draw mouse buttons area
    draw.ellipse([18, 16, 46, 40], fill=(236, 240, 241), outline=(189, 195, 199))
    
    # Draw left button (blue)
    draw.pieslice([18, 16, 32, 40], 180, 360, fill=(52, 152, 219), outline=(41, 128, 185))
    
    # Draw right button (red)
    draw.pieslice([32, 16, 46, 40], 180, 360, fill=(231, 76, 60), outline=(192, 57, 43))
    
    # Draw scroll wheel
    draw.rectangle([30, 20, 34, 28], fill=(149, 165, 166), outline=(127, 140, 141))
    
    # Draw cable
    draw.arc([28, 50, 36, 64], 0, 180, fill=(52, 73, 94), width=3)
    
    # Save as PNG
    img.save("assets/mouse_icon_64x64.png")
    print("✅ Created basic mouse icon: assets/mouse_icon_64x64.png")

if __name__ == "__main__":
    try:
        create_mouse_icon()
    except ImportError:
        print("⚠️ PIL/Pillow not available, skipping icon creation")
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
