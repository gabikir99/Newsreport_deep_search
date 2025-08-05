#!/usr/bin/env python3
"""
Main entry point for the AI Newsletter Research Tool Web Interface.
Run this file to start the web server.
"""

import sys
import os
from dotenv import load_dotenv

# Add the project root to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # Load environment variables
    load_dotenv(override=True)
    
    print("Starting AI Newsletter Research Tool Web Interface...")
    print("Users can enter their email and research topic")
    print("AI agents will research and send comprehensive reports")
    print("\n" + "="*50)
    print("Web interface available at: http://localhost:5000")
    print("="*50 + "\n")
    
    try:
        from src.web.web_interface import app
        # Start the Flask web application
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting web interface: {e}")
        import traceback
        traceback.print_exc()