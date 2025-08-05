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
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("gabikir1999@gmail.com") 
    to_email = To(_recipient_email)  # Use the dynamically set recipient email
    content = Content("text/html", html_body)
    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=html_body)
    response = sg.client.mail.send.post(request_body=mail.get())
    return {"status": "success", "code": response.status_code, "sent_to": _recipient_email}