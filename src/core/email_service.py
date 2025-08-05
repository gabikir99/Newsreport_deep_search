import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict
from src.agents.custom_agents import function_tool

# Global variable to store the recipient email (set by web interface)
_recipient_email = "gabikir1999@gmail.com"  # Default fallback


def update_recipient_email(email: str):
    """Update the recipient email address for sending reports"""
    global _recipient_email
    _recipient_email = email


def get_recipient_email() -> str:
    """Get the current recipient email address"""
    return _recipient_email


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send out an email with the given subject and HTML body to the configured recipient"""
    try:
        print(f"[EMAIL DEBUG] Attempting to send email to: {_recipient_email}")
        print(f"[EMAIL DEBUG] Subject: {subject}")
        print(f"[EMAIL DEBUG] Body length: {len(html_body)} characters")
        
        # Check API key
        api_key = os.environ.get('SENDGRID_API_KEY')
        if not api_key:
            error_msg = "SendGrid API key not found in environment variables"
            print(f"[EMAIL ERROR] {error_msg}")
            return {"status": "error", "message": error_msg}
        
        print(f"[EMAIL DEBUG] API key found: {api_key[:10]}...")
        
        # Initialize SendGrid client
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        
        # Create email components
        from_email = Email("gabikir1999@gmail.com") 
        to_email = To(_recipient_email)
        
        print(f"[EMAIL DEBUG] From: {from_email.email}")
        print(f"[EMAIL DEBUG] To: {to_email.email}")
        
        # Create mail object
        mail = Mail(
            from_email=from_email, 
            to_emails=to_email, 
            subject=subject, 
            html_content=html_body
        )
        
        print("[EMAIL DEBUG] Mail object created, sending...")
        
        # Send email
        response = sg.client.mail.send.post(request_body=mail.get())
        
        print(f"[EMAIL DEBUG] SendGrid response status: {response.status_code}")
        print(f"[EMAIL DEBUG] SendGrid response body: {response.body}")
        print(f"[EMAIL DEBUG] SendGrid response headers: {response.headers}")
        
        if response.status_code == 202:
            print("[EMAIL SUCCESS] Email sent successfully!")
            return {
                "status": "success", 
                "code": response.status_code, 
                "sent_to": _recipient_email,
                "message": "Email sent successfully"
            }
        else:
            error_msg = f"SendGrid returned status {response.status_code}: {response.body}"
            print(f"[EMAIL ERROR] {error_msg}")
            return {
                "status": "error", 
                "code": response.status_code, 
                "message": error_msg,
                "sent_to": _recipient_email
            }
            
    except Exception as e:
        error_msg = f"Exception while sending email: {str(e)}"
        print(f"[EMAIL ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error", 
            "message": error_msg,
            "sent_to": _recipient_email
        }