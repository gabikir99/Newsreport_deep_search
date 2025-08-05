import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Dict
from agents import function_tool


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """Send out an email with the given subject and HTML body"""
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("gabikir1999@gmail.com") 
    to_email = To("gabikir1999@gmail.com") 
    content = Content("text/html", html_body)
    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=html_body)
    response = sg.client.mail.send.post(request_body=mail.get())
    return {"status": "success", "code": response.status_code}