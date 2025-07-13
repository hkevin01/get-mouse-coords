#!/usr/bin/env python3
"""
Launcher script for Mouse Coordinate Tracker
Provides menu to choose between GUI and CLI versions
"""

import os
import sys
import subprocess


def check_virtual_env():
    """Check if virtual environment exists and packages are installed"""
    venv_path = os.path.join(os.path.dirname(__file__), '..', 'venv')
    if not os.path.exists(venv_path):
        print("Virtual environment not found.")
        print("Please run the setup script first:")
        print("  ./scripts/setup.sh")
        return False
    return True


def run_gui():
    """Launch the PyQt5 GUI application"""
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, '..', 'src', 'mouse_tracker_gui.py')
    venv_python = os.path.join(base_dir, '..', 'venv', 'bin', 'python')
    
    if os.path.exists(venv_python):
        subprocess.run([venv_python, script_path], check=False)
    else:
        subprocess.run([sys.executable, script_path], check=False)


def run_cli():
    """Launch the command-line application"""
    base_dir = os.path.dirname(__file__)
    script_path = os.path.join(base_dir, '..', 'src', 'mouse_tracker_cli.py')
    venv_python = os.path.join(base_dir, '..', 'venv', 'bin', 'python')
    
    if os.path.exists(venv_python):
        subprocess.run([venv_python, script_path], check=False)
    else:
        subprocess.run([sys.executable, script_path], check=False)


def main():
    """Main launcher menu"""
    print("=" * 50)
    print("    Mouse Coordinate Tracker Launcher")
    print("=" * 50)
    print()
    
    if not check_virtual_env():
        return
    
    while True:
        print("Choose an option:")
        print("1. Launch GUI Application (PyQt5)")
        print("2. Launch Command-Line Application")
        print("3. Exit")
        print()
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            print("Launching GUI application...")
            run_gui()
            break
        elif choice == '2':
            print("Launching command-line application...")
            run_cli()
            break
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            print()


if __name__ == "__main__":
    main()
