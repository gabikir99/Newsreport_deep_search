"""
Web-based main entry point for the AI Newsletter Research Tool.
This provides a user-friendly web interface instead of CLI.
"""

from src.web.web_interface import app
from dotenv import load_dotenv

if __name__ == '__main__':
    # Load environment variables
    load_dotenv(override=True)
    
    print("Starting AI Newsletter Research Tool Web Interface...")
    print("Users can enter their email and research topic")
    print("AI agents will research and send comprehensive reports")
    print("\n" + "="*50)
    print("Web interface available at: http://localhost:5000")
    print("="*50 + "\n")
    
    # Start the Flask web application
    app.run(debug=True, host='0.0.0.0', port=5000)