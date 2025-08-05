from flask import Flask, render_template, request, jsonify, redirect, url_for
import asyncio
import threading
from src.core.research_pipeline import run_research_pipeline, send_report_email
from dotenv import load_dotenv

app = Flask(__name__)

# Store the current research status
research_status = {
    "is_running": False,
    "progress": "",
    "completed": False,
    "error": None
}

def run_async_research(query, user_email):
    """Run the research pipeline in a separate thread"""
    global research_status
    
    async def research_task():
        try:
            # Ensure environment is loaded in this thread context
            from dotenv import load_dotenv
            load_dotenv(override=True)
            
            research_status["is_running"] = True
            research_status["progress"] = "Planning searches..."
            research_status["completed"] = False
            research_status["error"] = None
            
            # Update email service with user's email
            from src.core.email_service import update_recipient_email
            update_recipient_email(user_email)
            
            research_status["progress"] = "Performing web searches..."
            report = await run_research_pipeline(query)
            
            research_status["progress"] = "Generating and sending report..."
            await send_report_email(report)
            
            research_status["progress"] = "Complete! Report sent to your email."
            research_status["completed"] = True
            research_status["is_running"] = False
            
        except Exception as e:
            research_status["error"] = str(e)
            research_status["is_running"] = False
            research_status["progress"] = f"Error: {str(e)}"
    
    # Run the async function in a new event loop
    def run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(research_task())
        loop.close()
    
    thread = threading.Thread(target=run_in_thread)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    """Main page with input form"""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_research():
    """Handle form submission"""
    email = request.form.get('email')
    topic = request.form.get('topic')
    
    if not email or not topic:
        return jsonify({"error": "Please provide both email and topic"}), 400
    
    # Validate email format (basic validation)
    if '@' not in email or '.' not in email:
        return jsonify({"error": "Please provide a valid email address"}), 400
    
    # Start research process
    run_async_research(topic, email)
    
    return redirect(url_for('progress'))

@app.route('/progress')
def progress():
    """Progress page showing research status"""
    return render_template('progress.html')

@app.route('/status')
def status():
    """API endpoint for progress updates"""
    return jsonify(research_status)

if __name__ == '__main__':
    load_dotenv(override=True)
    app.run(debug=True, host='0.0.0.0', port=5000)