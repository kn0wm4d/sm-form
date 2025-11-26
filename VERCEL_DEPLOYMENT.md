# Vercel Deployment Guide

This guide will help you deploy the Workshop Registration Form to Vercel.

> **Important Update (2024)**: This project now uses **Node.js serverless functions** instead of Python. This ensures compatibility with Vercel's free tier, which no longer supports the deprecated `@vercel/python` runtime. The functionality remains the same, but the backend has been migrated to Node.js with the Nodemailer library.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup) (free tier is sufficient)
2. Your repository pushed to GitHub
3. SMTP credentials (e.g., Gmail with App Password)

## Step-by-Step Deployment

### 1. Connect Repository to Vercel

1. Log in to [Vercel](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. Select **"Import Git Repository"**
4. Choose your GitHub repository: `kn0wm4d/sm-form`
5. Click **"Import"**

### 2. Configure Project Settings

Vercel will automatically detect the configuration from `vercel.json`. You don't need to change any build settings.

Default settings should be:
- **Framework Preset**: Other
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### 3. Add Environment Variables

Before deploying, add your SMTP environment variables:

1. In the project import screen, expand **"Environment Variables"**
2. Add the following variables:

| Variable Name | Example Value | Description |
|--------------|---------------|-------------|
| `SMTP_SERVER` | `smtp.gmail.com` | Your SMTP server address (defaults to smtp.gmail.com if not set) |
| `SMTP_PORT` | `587` | SMTP port - use 587 for STARTTLS or 465 for SSL (defaults to 587) |
| `SMTP_USERNAME` | `your-email@gmail.com` | Your email address (required) |
| `SMTP_PASSWORD` | `xxxx xxxx xxxx xxxx` | Your email password or app password (required) |
| `SMTP_FROM_EMAIL` | `your-email@gmail.com` | Email address to send from (defaults to SMTP_USERNAME) |
| `SMTP_FROM_NAME` | `Workshop Registration` | Display name for emails (defaults to 'Workshop Registration') |
| `EMAIL_SUBMISSIONS` | `admin@example.com` | Admin email to receive submissions (optional) |

**Note about defaults**: Only `SMTP_USERNAME` and `SMTP_PASSWORD` are required. Other variables have sensible defaults suitable for Gmail. For other SMTP providers, you should explicitly set all variables.

**Important for Gmail Users:**
- You must use an [App Password](https://myaccount.google.com/apppasswords), not your regular password
- Enable 2-factor authentication on your Google account first
- Generate an app password specifically for this application

### 4. Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (usually 1-2 minutes)
3. Your site will be live at `https://your-project-name.vercel.app`

### 5. Test Your Deployment

1. Visit your deployed site
2. Fill out the form with a valid email address
3. Submit the form
4. Check both:
   - The user's email inbox for the confirmation email
   - The admin email (`EMAIL_SUBMISSIONS`) for the detailed submission

### 6. Configure Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to **"Domains"**
3. Add your custom domain
4. Follow Vercel's instructions to configure DNS

## Environment Variables Update

To update environment variables after deployment:

1. Go to your project in Vercel dashboard
2. Click **"Settings"**
3. Navigate to **"Environment Variables"**
4. Add, edit, or remove variables
5. **Important**: After changing environment variables, you must **redeploy** your project:
   - Go to **"Deployments"**
   - Click **"..."** on the latest deployment
   - Select **"Redeploy"**

## Troubleshooting

### Email not sending

1. **Check environment variables**: Ensure all SMTP variables are set correctly
2. **Check SMTP credentials**: 
   - For Gmail, verify you're using an App Password
   - Test your credentials with a simple email client
3. **Check server logs**:
   - Go to Vercel dashboard
   - Navigate to your project → **"Deployments"**
   - Click on the latest deployment
   - Check the **"Functions"** tab for error logs

### Build fails

1. **Check build logs**: Look for errors in the Vercel deployment logs
2. **Verify package.json**: Ensure all dependencies are listed (including nodemailer)
3. **Test locally**: Run `npm run build` locally to ensure it works

### Form submission fails

1. **Check browser console**: Look for JavaScript errors
2. **Check network tab**: Verify the request to `/api/submit` is being made
3. **Test API endpoint**: Visit `https://your-site.vercel.app/api/submit` (should show method not allowed for GET)

### API 404 Error

If you're getting a 404 error for `/api/submit`:

1. **Ensure you're using the latest version**: The project has been updated to use Node.js serverless functions (Vercel free tier compatible)
2. **Verify deployment**: Check that `api/submit.js` was deployed correctly in your Vercel dashboard
3. **Check build logs**: Make sure there are no errors during the build process
4. **Redeploy**: Try redeploying your project from the Vercel dashboard

## Monitoring

Vercel provides built-in monitoring:

1. **Analytics**: Track page views and performance
2. **Logs**: View serverless function logs
3. **Speed Insights**: Monitor site performance

Access these from your project dashboard.

## Cost

The free Vercel tier includes:
- Unlimited deployments
- 100 GB bandwidth per month
- Serverless function executions
- Automatic HTTPS

This is more than sufficient for most workshop registration forms.

## Security Notes

1. **Never commit** `.env` files to git
2. **Use App Passwords** for Gmail (never your main password)
3. **Rotate credentials** periodically
4. **Monitor function logs** for suspicious activity

## Support

For issues with:
- **Vercel deployment**: Check [Vercel documentation](https://vercel.com/docs)
- **This project**: Open an issue on GitHub
- **SMTP/Email**: Contact your email provider's support
