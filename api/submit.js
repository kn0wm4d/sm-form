/**
 * Vercel serverless function for handling form submissions and sending emails via SMTP.
 * Node.js version (compatible with Vercel free tier)
 */
const nodemailer = require('nodemailer');

/**
 * Format form data into HTML for email.
 */
function formatFormData(formData) {
  let html = `
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
  `;

  // Add form fields
  for (const [fieldName, fieldData] of Object.entries(formData)) {
    if (fieldName !== 'access_key' && fieldName !== 'subject') {
      const label = fieldData.label || fieldName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      let value = fieldData.value || '';

      // Format arrays nicely
      if (Array.isArray(value)) {
        if (value.length > 0) {
          value = value.join(', ');
        } else {
          continue; // Skip empty arrays
        }
      }

      html += `
            <div class="field">
                <div class="field-label">${label}</div>
                <div class="field-value">${value}</div>
            </div>
      `;
    }
  }

  html += `
            <div class="footer">
                <p>This is an automated notification of a new workshop registration.</p>
            </div>
        </div>
    </body>
    </html>
  `;

  return html;
}

/**
 * Format confirmation email for the user (without submission details).
 */
function formatConfirmationEmail(userName) {
  return `
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            h2 { color: #4F46E5; }
            .message { margin: 20px 0; padding: 20px; background-color: #f0f9ff; border-left: 4px solid #4F46E5; border-radius: 5px; }
            .footer { margin-top: 30px; padding-top: 20px; border-top: 2px solid #4F46E5; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Workshop Registration Confirmation</h2>
            <div class="message">
                <p>Dear ${userName},</p>
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
  `;
}

/**
 * Send an email using SMTP with the configured settings.
 */
async function sendEmail(toEmail, subject, htmlContent) {
  const smtpServer = process.env.SMTP_SERVER || 'smtp.gmail.com';
  const smtpPort = parseInt(process.env.SMTP_PORT || '587', 10);
  const smtpUsername = process.env.SMTP_USERNAME;
  const smtpPassword = process.env.SMTP_PASSWORD;
  const smtpFromEmail = process.env.SMTP_FROM_EMAIL || smtpUsername;
  const smtpFromName = process.env.SMTP_FROM_NAME || 'Workshop Registration';

  if (!smtpUsername || !smtpPassword) {
    console.error('SMTP credentials not configured');
    return false;
  }

  try {
    // Create transporter
    const transporter = nodemailer.createTransport({
      host: smtpServer,
      port: smtpPort,
      secure: false, // true for 465, false for other ports
      auth: {
        user: smtpUsername,
        pass: smtpPassword,
      },
    });

    // Send email
    await transporter.sendMail({
      from: `"${smtpFromName}" <${smtpFromEmail}>`,
      to: toEmail,
      subject: subject,
      html: htmlContent,
    });

    console.log(`Email sent successfully to ${toEmail}`);
    return true;
  } catch (error) {
    console.error(`Failed to send email: ${error.message}`);
    return false;
  }
}

/**
 * Vercel serverless function handler
 */
module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept');

  // Handle OPTIONS request
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    res.status(405).json({ success: false, message: 'Method not allowed' });
    return;
  }

  try {
    const data = req.body;

    if (!data) {
      res.status(400).json({ success: false, message: 'No data received' });
      return;
    }

    // Extract email from form data
    const recipientEmail = data.email?.value;

    if (!recipientEmail) {
      res.status(400).json({ success: false, message: 'Email is required' });
      return;
    }

    // Get user name for personalized emails
    const userName = data.name?.value || 'Participant';

    // Send confirmation email to user (without details)
    const confirmationSubject = `Workshop Registration Confirmation - ${userName}`;
    const confirmationHtml = formatConfirmationEmail(userName);
    const userEmailSent = await sendEmail(recipientEmail, confirmationSubject, confirmationHtml);

    // Send submission details to admin email if configured
    let adminEmailSent = true; // Default to true if no admin email configured
    const emailSubmissions = process.env.EMAIL_SUBMISSIONS;
    if (emailSubmissions) {
      const adminSubject = `New Workshop Registration - ${userName}`;
      const adminHtml = formatFormData(data);
      adminEmailSent = await sendEmail(emailSubmissions, adminSubject, adminHtml);
    }

    if (userEmailSent && adminEmailSent) {
      res.status(200).json({
        success: true,
        message: 'Form submitted successfully and confirmation email sent',
      });
    } else if (userEmailSent) {
      res.status(200).json({
        success: true,
        message: 'Form submitted and confirmation email sent, but admin notification failed',
      });
    } else {
      res.status(500).json({
        success: false,
        message: 'Form received but failed to send confirmation email',
      });
    }
  } catch (error) {
    console.error(`Error processing form submission: ${error.message}`);
    res.status(500).json({
      success: false,
      message: `Server error: ${error.message}`,
    });
  }
};
