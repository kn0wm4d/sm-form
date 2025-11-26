"""
Vercel serverless function for handling form submissions and sending emails via SMTP.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import BaseHTTPRequestHandler
import json


def send_email(to_email, subject, html_content):
    """
    Send an email using SMTP with the configured settings.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML content of the email
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    smtp_from_email = os.environ.get('SMTP_FROM_EMAIL', smtp_username)
    smtp_from_name = os.environ.get('SMTP_FROM_NAME', 'Workshop Registration')
    
    if not smtp_username or not smtp_password:
        print("SMTP credentials not configured")
        return False
    
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f"{smtp_from_name} <{smtp_from_email}>"
        message['To'] = to_email
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)
        
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def format_form_data(form_data):
    """
    Format form data into HTML for email.
    
    Args:
        form_data: Dictionary containing form field data
        
    Returns:
        str: HTML formatted string
    """
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            h2 { color: #4F46E5; }
            .field { margin: 15px 0; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }
            .field-label { font-weight: bold; color: #4F46E5; }
            .field-value { margin-top: 5px; }
            .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #4F46E5; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Workshop Registration - Submission Details</h2>
            <p>New workshop registration received:</p>
    """
    
    # Add form fields
    for field_name, field_data in form_data.items():
        if field_name not in ['access_key', 'subject']:
            label = field_data.get('label', field_name.replace('_', ' ').title())
            value = field_data.get('value', '')
            
            # Format arrays nicely
            if isinstance(value, list):
                if value:  # Only show if list has items
                    value = ', '.join(value)
                else:
                    continue  # Skip empty lists
            
            html += f"""
            <div class="field">
                <div class="field-label">{label}</div>
                <div class="field-value">{value}</div>
            </div>
            """
    
    html += """
            <div class="footer">
                <p>This is an automated notification of a new workshop registration.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def format_confirmation_email(user_name):
    """
    Format confirmation email for the user (without submission details).
    
    Args:
        user_name: Name of the user
        
    Returns:
        str: HTML formatted confirmation email
    """
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            h2 {{ color: #4F46E5; }}
            .message {{ margin: 20px 0; padding: 20px; background-color: #f0f9ff; border-left: 4px solid #4F46E5; border-radius: 5px; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #4F46E5; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Workshop Registration Confirmation</h2>
            <div class="message">
                <p>Dear {user_name},</p>
                <p>Thank you for registering for our workshops! We have received your registration successfully.</p>
                <p>We will review your registration and get back to you shortly with further details about the workshops you selected.</p>
            </div>
            <div class="footer">
                <p>If you have any questions or need to make changes to your registration, please contact us.</p>
                <p>We look forward to seeing you at the workshops!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


class handler(BaseHTTPRequestHandler):
    """
    Vercel serverless function handler.
    """
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            if not data:
                self._send_response(400, {'success': False, 'message': 'No data received'})
                return
            
            # Extract email from form data
            recipient_email = None
            if 'email' in data and 'value' in data['email']:
                recipient_email = data['email']['value']
            
            if not recipient_email:
                self._send_response(400, {'success': False, 'message': 'Email is required'})
                return
            
            # Get user name for personalized emails
            user_name = data.get('name', {}).get('value', 'Participant')
            
            # Send confirmation email to user (without details)
            confirmation_subject = f"Workshop Registration Confirmation - {user_name}"
            confirmation_html = format_confirmation_email(user_name)
            user_email_sent = send_email(recipient_email, confirmation_subject, confirmation_html)
            
            # Send submission details to admin email if configured
            admin_email_sent = True  # Default to true if no admin email configured
            email_submissions = os.environ.get('EMAIL_SUBMISSIONS')
            if email_submissions:
                admin_subject = f"New Workshop Registration - {user_name}"
                admin_html = format_form_data(data)
                admin_email_sent = send_email(email_submissions, admin_subject, admin_html)
            
            if user_email_sent and admin_email_sent:
                self._send_response(200, {
                    'success': True,
                    'message': 'Form submitted successfully and confirmation email sent'
                })
            elif user_email_sent:
                self._send_response(200, {
                    'success': True,
                    'message': 'Form submitted and confirmation email sent, but admin notification failed'
                })
            else:
                self._send_response(500, {
                    'success': False,
                    'message': 'Form received but failed to send confirmation email'
                })
                
        except Exception as e:
            print(f"Error processing form submission: {str(e)}")
            self._send_response(500, {
                'success': False,
                'message': f'Server error: {str(e)}'
            })
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self._send_cors_headers()
        self.end_headers()
    
    def _send_response(self, status_code, data):
        """Send JSON response with CORS headers."""
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _send_cors_headers(self):
        """Send CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Accept')
