#!/usr/bin/env python3
"""
Main entry point for the AI Newsletter Research Tool Web Interface.
Run this file to start the web server.
"""

import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.web.web_main import *

if __name__ == '__main__':
    # This will execute the web_main.py content
    pass