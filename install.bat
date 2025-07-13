@echo off
REM Mouse Coordinate Tracker - Windows Installation Script
REM This script sets up the environment and launches the application

title Mouse Coordinate Tracker - Installer

echo.
echo ===============================================
echo   Mouse Coordinate Tracker - Windows Setup
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6+ from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/5] Python found! Checking version...
python -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.6+ is required
    echo Current version:
    python --version
    echo.
    pause
    exit /b 1
)

echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists, skipping...
)

echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Trying to install individual packages...
    pip install PyQt5>=5.15.0
    pip install pyautogui>=0.9.54
    pip install pynput>=1.7.6
)

echo [5/5] Generating application icons...
if exist "scripts\generate_icons.py" (
    python scripts\generate_icons.py
)

echo.
echo ===============================================
echo   Installation Complete!
echo ===============================================
echo.
echo Choose an option:
echo   1. Launch GUI Application
echo   2. Launch CLI Application  
echo   3. Create Desktop Shortcut
echo   4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting GUI application...
    python src\mouse_tracker_gui.py
) else if "%choice%"=="2" (
    echo.
    echo Starting CLI application...
    python src\mouse_tracker_cli.py
) else if "%choice%"=="3" (
    call :create_shortcut
) else (
    echo.
    echo To run the application later, use:
    echo   GUI: venv\Scripts\activate.bat ^&^& python src\mouse_tracker_gui.py
    echo   CLI: venv\Scripts\activate.bat ^&^& python src\mouse_tracker_cli.py
)

echo.
pause
exit /b 0

:create_shortcut
echo.
echo Creating desktop shortcut...

set "shortcut_path=%USERPROFILE%\Desktop\Mouse Coordinate Tracker.bat"
set "current_dir=%CD%"

(
echo @echo off
echo title Mouse Coordinate Tracker
echo cd /d "%current_dir%"
echo call venv\Scripts\activate.bat
echo python src\mouse_tracker_gui.py
echo pause
) > "%shortcut_path%"

if exist "%shortcut_path%" (
    echo Desktop shortcut created: %shortcut_path%
) else (
    echo Failed to create desktop shortcut
)
goto :eof
