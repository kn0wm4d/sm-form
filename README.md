# Multistep Typeform Like Form Template

This is a simple implementation of Working Multi-Step form using Vue, Tailwind CSS with SMTP email notifications.

## Features

- Multi-step form with validation
- SMTP email notifications
- User confirmation emails
- Admin submission notifications
- Configurable via environment variables
- **Vercel-ready deployment**

## How to use

First clone the code to your local system from github.

```bash
git clone https://github.com/kn0wm4d/sm-form.git MyProjectName
# or (same folder)
git clone https://github.com/kn0wm4d/sm-form.git .
```

### Frontend Setup

Install Node dependencies:

```bash
npm install
# or
yarn
```

Run the development server & watch CSS:

```bash
npm run dev
# or
yarn dev
```

To start a development server, go to `src/index.html` and right click on the page and choose "Open with Live Server". or use the shortcut (`Cmd + L` then `Cmd + O`). Alternatively, you can open the live server from the right top icon on the `index.html` page.

Now you will get a URL like: `http://127.0.0.1:3000/src/index.html`

### Backend Setup (For Local Development)

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Configure environment variables:

Copy `.env.example` to `.env` and configure your SMTP settings:

```bash
cp .env.example .env
```

Edit `.env` with your SMTP credentials:

```
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Workshop Registration

# Admin email to receive submission details
EMAIL_SUBMISSIONS=admin@example.com

# Server settings
PORT=5000
DEBUG=False
```

**Note for Gmail users:** You need to use an App Password instead of your regular password. Follow these steps:
1. Enable 2-factor authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Use that app password in the `SMTP_PASSWORD` field

3. Run the backend server:

```bash
python server.py
```

The server will start on `http://localhost:5000`

### How it works

When a form is submitted:
1. User receives a **confirmation email** at the email address they provided (without submission details)
2. Admin receives a **detailed submission email** at the `EMAIL_SUBMISSIONS` address with all form data
3. All SMTP settings are configurable via environment variables

## Deploying to Vercel

This project is ready to be deployed to Vercel with just a few clicks!

### Step 1: Prepare for Deployment

Build the project:

```bash
npm run build
# or
yarn build
```

### Step 2: Deploy to Vercel

1. **Install Vercel CLI** (optional, for command-line deployment):
   ```bash
   npm i -g vercel
   ```

2. **Deploy via Vercel Dashboard** (recommended):
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the configuration from `vercel.json`
   - Click "Deploy"

3. **Or Deploy via CLI**:
   ```bash
   vercel
   ```

### Step 3: Configure Environment Variables on Vercel

After deployment, configure the environment variables in your Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:
   - `SMTP_SERVER` (e.g., `smtp.gmail.com`)
   - `SMTP_PORT` (e.g., `587`)
   - `SMTP_USERNAME` (your email)
   - `SMTP_PASSWORD` (your app password)
   - `SMTP_FROM_EMAIL` (your email)
   - `SMTP_FROM_NAME` (e.g., `Workshop Registration`)
   - `EMAIL_SUBMISSIONS` (admin email to receive submissions)

4. Redeploy your project to apply the environment variables

### Architecture

- **Frontend**: Static Vue.js application served from `/dist`
- **Backend**: Python serverless function in `/api/submit.py`
- **Email**: SMTP via standard Python `smtplib`
- **Deployment**: Vercel with automatic CI/CD

The serverless function will handle form submissions and send emails without needing a dedicated server!

## Local Development vs Production

- **Local**: Uses `http://localhost:5000/submit` endpoint
- **Vercel**: Uses `/api/submit` endpoint (serverless function)

The frontend automatically detects the environment and uses the correct endpoint.

## Manual Deployment (Non-Vercel)

If you prefer to deploy elsewhere:

1. Build the frontend:
   ```bash
   npm run build
   ```

2. Deploy the `/dist` folder to your static hosting
3. Deploy the `server.py` as a Python web server
4. Configure environment variables on your hosting platform
5. Update the frontend's backend URL if needed
