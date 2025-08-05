#!/usr/bin/env python3
"""
Simple test for the web interface
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting simple web test...")

try:
    from flask import Flask
    print("Flask imported successfully")
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return '<h1>Hello! Web interface is working!</h1><p>Go to <a href="/test">test page</a></p>'
    
    @app.route('/test')
    def test():
        return '<h1>Test page works!</h1><p><a href="/">Back to home</a></p>'
    
    print("Routes configured successfully")
    print("Starting Flask app on http://localhost:5000")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()