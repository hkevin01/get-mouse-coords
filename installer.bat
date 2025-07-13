@echo off
title Mouse Coordinate Tracker - Installer

echo.
echo ================================================
echo   Mouse Coordinate Tracker - Windows Installer
echo ================================================
echo.

set "INSTALL_DIR=%PROGRAMFILES%\Mouse Coordinate Tracker"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\Mouse Coordinate Tracker.lnk"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"

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
copy "MouseCoordinateTracker.exe" "%INSTALL_DIR%\" >nul
if exist "assets" xcopy "assets" "%INSTALL_DIR%\assets\" /E /I /Q >nul
copy "README.md" "%INSTALL_DIR%\" >nul 2>nul

echo [4/4] Creating shortcuts...

REM Create desktop shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\MouseCoordinateTracker.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Track and save mouse coordinates'; $Shortcut.Save()}"

REM Create start menu shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU%\Mouse Coordinate Tracker.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\MouseCoordinateTracker.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Track and save mouse coordinates'; $Shortcut.Save()}"

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
echo   • Run from: %INSTALL_DIR%\MouseCoordinateTracker.exe
echo.

set /p launch="Launch Mouse Coordinate Tracker now? (y/n): "
if /i "%launch%"=="y" (
    start "" "%INSTALL_DIR%\MouseCoordinateTracker.exe"
)

echo.
echo Thank you for installing Mouse Coordinate Tracker!
pause