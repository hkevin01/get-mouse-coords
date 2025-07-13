#!/usr/bin/env python3
"""
Simple command-line mouse coordinate tracker
Based on the original script but with improvements
"""

import pyautogui
import sys
import time


def main():
    """Main function for command-line coordinate tracking"""
    print('Mouse Coordinate Tracker')
    print('Press Ctrl-C to quit.')
    print('=' * 30)
    
    try:
        while True:
            x, y = pyautogui.position()
            position_str = f'X: {str(x).rjust(4)} Y: {str(y).rjust(4)}'
            print(position_str, end='')
            print('\b' * len(position_str), end='', flush=True)
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        print('\nTracking stopped.')


if __name__ == "__main__":
    main()
