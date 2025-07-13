# Mouse Coordinate Tracker - PowerShell Installer
# Enhanced Windows installation script with better error handling

param(
    [switch]$BuildExecutable,
    [switch]$InstallOnly,
    [string]$InstallPath = "$env:PROGRAMFILES\Mouse Coordinate Tracker"
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

# Main banner
Write-Host ""
Write-Host "=================================================================" -ForegroundColor $Blue
Write-Host "    🖱️  Mouse Coordinate Tracker - PowerShell Installer" -ForegroundColor $Blue
Write-Host "=================================================================" -ForegroundColor $Blue
Write-Host ""

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script requires administrator privileges for system-wide installation."
    Write-Host "Please right-click and 'Run as Administrator' for full installation." -ForegroundColor $Yellow
    Write-Host ""
    
    $choice = Read-Host "Continue with user-level installation? (y/n)"
    if ($choice -ne "y") {
        exit 1
    }
    $InstallPath = "$env:LOCALAPPDATA\Mouse Coordinate Tracker"
}

# Check Python installation
Write-Status "Checking Python installation..."
try {
    $pythonVersion = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python found: $pythonVersion"
        
        # Check if Python 3.6+
        $version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>&1
        if ([version]$version -lt [version]"3.6") {
            Write-Error "Python 3.6+ is required. Current version: $version"
            exit 1
        }
    } else {
        Write-Error "Python is not installed or not in PATH"
        Write-Host "Please install Python 3.6+ from: https://www.python.org/downloads/" -ForegroundColor $Yellow
        exit 1
    }
} catch {
    Write-Error "Failed to check Python installation"
    exit 1
}

# Build executable if requested
if ($BuildExecutable) {
    Write-Status "Building Windows executable..."
    
    # Install PyInstaller
    Write-Status "Installing PyInstaller..."
    & python -m pip install pyinstaller pillow --quiet
    
    if (Test-Path "scripts\build_windows_installer.py") {
        & python scripts\build_windows_installer.py
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Executable built successfully"
        } else {
            Write-Error "Failed to build executable"
            exit 1
        }
    } else {
        Write-Error "Build script not found"
        exit 1
    }
}

# Install application
if (-not $BuildExecutable -or $InstallOnly) {
    Write-Status "Installing Mouse Coordinate Tracker..."
    
    # Create installation directory
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Success "Created installation directory: $InstallPath"
    }
    
    # Copy files
    Write-Status "Copying application files..."
    
    if (Test-Path "MouseCoordinateTracker_Windows_Installer\MouseCoordinateTracker.exe") {
        Copy-Item "MouseCoordinateTracker_Windows_Installer\MouseCoordinateTracker.exe" "$InstallPath\" -Force
        Copy-Item "README.md" "$InstallPath\" -Force -ErrorAction SilentlyContinue
        
        if (Test-Path "assets") {
            Copy-Item "assets" "$InstallPath\" -Recurse -Force -ErrorAction SilentlyContinue
        }
        
        Write-Success "Files copied successfully"
        
        # Create shortcuts
        Write-Status "Creating shortcuts..."
        
        # Desktop shortcut
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Mouse Coordinate Tracker.lnk")
        $Shortcut.TargetPath = "$InstallPath\MouseCoordinateTracker.exe"
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = "Track and save mouse coordinates"
        $Shortcut.Save()
        
        # Start menu shortcut
        $StartMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
        $Shortcut = $WshShell.CreateShortcut("$StartMenuPath\Mouse Coordinate Tracker.lnk")
        $Shortcut.TargetPath = "$InstallPath\MouseCoordinateTracker.exe"
        $Shortcut.WorkingDirectory = $InstallPath
        $Shortcut.Description = "Track and save mouse coordinates"
        $Shortcut.Save()
        
        Write-Success "Shortcuts created"
        
        Write-Host ""
        Write-Host "=================================================================" -ForegroundColor $Green
        Write-Host "   Installation Complete!" -ForegroundColor $Green
        Write-Host "=================================================================" -ForegroundColor $Green
        Write-Host ""
        Write-Host "Application installed to: $InstallPath" -ForegroundColor $Green
        Write-Host "Desktop shortcut created" -ForegroundColor $Green
        Write-Host "Start menu shortcut created" -ForegroundColor $Green
        Write-Host ""
        
        $launch = Read-Host "Launch Mouse Coordinate Tracker now? (y/n)"
        if ($launch -eq "y") {
            Start-Process "$InstallPath\MouseCoordinateTracker.exe"
        }
        
    } else {
        Write-Warning "Executable not found. Running Python version setup..."
        
        # Setup Python environment
        Write-Status "Setting up Python environment..."
        
        if (-not (Test-Path "venv")) {
            & python -m venv venv
            Write-Success "Virtual environment created"
        }
        
        # Activate virtual environment and install dependencies
        & .\venv\Scripts\activate.ps1
        & pip install -r requirements.txt --quiet
        
        Write-Success "Python environment ready"
        
        # Create batch file for easy launching
        $launcherContent = @"
@echo off
cd /d "$PWD"
call venv\Scripts\activate.bat
python src\mouse_tracker_gui.py
pause
"@
        
        $launcherContent | Out-File -FilePath "Launch Mouse Tracker.bat" -Encoding ASCII
        
        Write-Success "Launcher script created: Launch Mouse Tracker.bat"
        
        $launch = Read-Host "Launch Mouse Coordinate Tracker now? (y/n)"
        if ($launch -eq "y") {
            & ".\Launch Mouse Tracker.bat"
        }
    }
}

Write-Host ""
Write-Success "Thanks for using Mouse Coordinate Tracker!"
