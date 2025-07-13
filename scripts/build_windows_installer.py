"""
Windows Installer Builder for Mouse Coordinate Tracker
Creates a standalone executable installer for Windows using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create PyInstaller spec file for the application."""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/mouse_tracker_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/*', 'assets'),
        ('requirements.txt', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=['pynput.keyboard._win32', 'pynput.mouse._win32'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MouseCoordinateTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/mouse_icon.ico',
    version_file='version_info.txt'
)
"""
    
    with open("mouse_tracker.spec", "w") as f:
        f.write(spec_content.strip())
    print("✅ Created PyInstaller spec file")

def create_version_info():
    """Create version info file for Windows executable."""
    version_info = """
# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Mouse Coordinate Tracker'),
        StringStruct(u'FileDescription', u'Track and save mouse coordinates'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'MouseCoordinateTracker'),
        StringStruct(u'LegalCopyright', u'MIT License'),
        StringStruct(u'OriginalFilename', u'MouseCoordinateTracker.exe'),
        StringStruct(u'ProductName', u'Mouse Coordinate Tracker'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    
    with open("version_info.txt", "w") as f:
        f.write(version_info.strip())
    print("✅ Created version info file")

def create_icon():
    """Create or convert icon for Windows executable."""
    icon_paths = [
        "assets/mouse_icon_64x64.png",
        "assets/mouse_icon.svg"
    ]
    
    # Try to convert existing icon to ICO format
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            try:
                from PIL import Image
                if icon_path.endswith('.png'):
                    img = Image.open(icon_path)
                    img.save("assets/mouse_icon.ico", format='ICO')
                    print("✅ Created ICO icon from PNG")
                    return True
            except ImportError:
                print("⚠️ PIL not available for icon conversion")
                break
            except Exception as e:
                print(f"⚠️ Icon conversion failed: {e}")
                break
    
    # Create a simple ICO file if conversion failed
    print("📝 Using default icon")
    return False

def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building executable...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "mouse_tracker.spec"
        ])
        print("✅ Executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_installer_script():
    """Create an installer batch script."""
    installer_script = """@echo off
title Mouse Coordinate Tracker - Installer

echo.
echo ================================================
echo   Mouse Coordinate Tracker - Windows Installer
echo ================================================
echo.

set "INSTALL_DIR=%PROGRAMFILES%\\Mouse Coordinate Tracker"
set "DESKTOP_SHORTCUT=%USERPROFILE%\\Desktop\\Mouse Coordinate Tracker.lnk"
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"

echo [1/4] Checking permissions...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
) else (
    echo ⚠️ This installer requires administrator privileges
    echo Please right-click and "Run as administrator"
    pause
    exit /b 1
)

echo [2/4] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo ✅ Installation directory: %INSTALL_DIR%

echo [3/4] Copying files...
copy "MouseCoordinateTracker.exe" "%INSTALL_DIR%\\" >nul
if exist "assets" xcopy "assets" "%INSTALL_DIR%\\assets\\" /E /I /Q >nul
copy "README.md" "%INSTALL_DIR%\\" >nul 2>nul

echo [4/4] Creating shortcuts...

REM Create desktop shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MouseCoordinateTracker.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Track and save mouse coordinates'; $Shortcut.Save()}"

REM Create start menu shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\\Mouse Coordinate Tracker.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MouseCoordinateTracker.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Track and save mouse coordinates'; $Shortcut.Save()}"

echo.
echo ================================================
echo   Installation Complete!
echo ================================================
echo.
echo Application installed to: %INSTALL_DIR%
echo Desktop shortcut created: %DESKTOP_SHORTCUT%
echo Start menu shortcut created
echo.
echo You can now:
echo   • Double-click the desktop shortcut
echo   • Find it in your Start Menu
echo   • Run from: %INSTALL_DIR%\\MouseCoordinateTracker.exe
echo.

set /p launch="Launch Mouse Coordinate Tracker now? (y/n): "
if /i "%launch%"=="y" (
    start "" "%INSTALL_DIR%\\MouseCoordinateTracker.exe"
)

echo.
echo Thank you for installing Mouse Coordinate Tracker!
pause
"""
    
    with open("installer.bat", "w") as f:
        f.write(installer_script.strip())
    print("✅ Created installer script")

def main():
    """Main build process."""
    print("🔧 Building Windows Installer for Mouse Coordinate Tracker")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("src/mouse_tracker_gui.py"):
        print("❌ Please run this script from the project root directory")
        return False
    
    # Install PyInstaller
    if not install_pyinstaller():
        return False
    
    # Create necessary files
    create_spec_file()
    create_version_info()
    create_icon()
    
    # Build executable
    if not build_executable():
        return False
    
    # Create installer script
    create_installer_script()
    
    # Copy executable and create distribution
    dist_dir = "dist"
    exe_source = f"{dist_dir}/MouseCoordinateTracker"  # Linux builds without .exe
    exe_windows = f"{dist_dir}/MouseCoordinateTracker.exe"  # Windows format
    
    # Check for either format
    if os.path.exists(exe_source):
        # Rename to Windows format if needed
        if not os.path.exists(exe_windows):
            shutil.copy(exe_source, exe_windows)
            print(f"✅ Copied executable to Windows format: {exe_windows}")
        
        # Create installer package
        installer_dir = "MouseCoordinateTracker_Windows_Installer"
        if os.path.exists(installer_dir):
            shutil.rmtree(installer_dir)
        os.makedirs(installer_dir)
        
        # Copy files to installer directory
        shutil.copy(exe_windows, installer_dir)
        shutil.copy("installer.bat", installer_dir)
        shutil.copy("README.md", installer_dir)
        
        if os.path.exists("assets"):
            shutil.copytree("assets", f"{installer_dir}/assets")
        
        print(f"✅ Installer package created: {installer_dir}/")
        exe_size = os.path.getsize(exe_windows) / 1024 / 1024
        print(f"📦 Executable size: {exe_size:.1f} MB")
        print()
        print("🎉 Windows installer ready!")
        print(f"   📁 Package location: {installer_dir}/")
        print(f"   🚀 To install: Run {installer_dir}/installer.bat as Admin")
        print(f"   📱 Standalone: Use {installer_dir}/MouseCoordinateTracker.exe")
        
        return True
    else:
        print("❌ Executable not found in dist directory")
        return False


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Build completed successfully!")
