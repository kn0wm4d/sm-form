#!/usr/bin/env python3
"""
Flask server for handling form submissions and sending emails via SMTP.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# SMTP Configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', SMTP_USERNAME)
SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'Workshop Registration')
EMAIL_SUBMISSIONS = os.getenv('EMAIL_SUBMISSIONS')  # Admin email for submission details


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
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print("SMTP credentials not configured")
        return False
    
    try:
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
        message['To'] = to_email
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        message.attach(html_part)
        
        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
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


@app.route('/submit', methods=['POST'])
def submit_form():
    """
    Handle form submission and send confirmation email.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data received'}), 400
        
        # Extract email from form data
        recipient_email = None
        if 'email' in data and 'value' in data['email']:
            recipient_email = data['email']['value']
        
        if not recipient_email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # Get user name for personalized emails
        user_name = data.get('name', {}).get('value', 'Participant')
        
        # Send confirmation email to user (without details)
        confirmation_subject = f"Workshop Registration Confirmation - {user_name}"
        confirmation_html = format_confirmation_email(user_name)
        user_email_sent = send_email(recipient_email, confirmation_subject, confirmation_html)
        
        # Send submission details to admin email if configured
        admin_email_sent = True  # Default to true if no admin email configured
        if EMAIL_SUBMISSIONS:
            admin_subject = f"New Workshop Registration - {user_name}"
            admin_html = format_form_data(data)
            admin_email_sent = send_email(EMAIL_SUBMISSIONS, admin_subject, admin_html)
        
        if user_email_sent and admin_email_sent:
            return jsonify({
                'success': True,
                'message': 'Form submitted successfully and confirmation email sent'
            }), 200
        elif user_email_sent:
            return jsonify({
                'success': True,
                'message': 'Form submitted and confirmation email sent, but admin notification failed'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Form received but failed to send confirmation email'
            }), 500
            
    except Exception as e:
        print(f"Error processing form submission: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
