# Migration Guide: Python to Node.js

## Overview

This project has been migrated from Python serverless functions to Node.js serverless functions to ensure compatibility with Vercel's free tier. Vercel deprecated the `@vercel/python` runtime, which was causing 404 errors when accessing `/api/submit`.

## What Changed

### Backend
- **Old**: Python serverless function (`api/submit.py`) using `smtplib`
- **New**: Node.js serverless function (`api/submit.js`) using `nodemailer`

### Configuration
- **Old**: `vercel.json` included `@vercel/python` builder
- **New**: `vercel.json` simplified - Vercel auto-detects Node.js functions in `/api` directory

### Dependencies
- **New**: Added `nodemailer` package to `package.json`

## What Stayed the Same

✅ **All functionality remains identical**:
- SMTP email sending
- User confirmation emails
- Admin notification emails
- Form validation
- Environment variable configuration
- API endpoint (`/api/submit`)
- Frontend code (no changes required)

✅ **Same environment variables**:
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SMTP_FROM_NAME`
- `EMAIL_SUBMISSIONS`

## Migration Steps for Existing Deployments

If you have an existing deployment using the old Python version:

1. **Pull the latest code**:
   ```bash
   git pull origin main
   ```

2. **Install new dependencies**:
   ```bash
   npm install
   ```

3. **Test locally** (optional):
   ```bash
   npm run build
   ```

4. **Redeploy to Vercel**:
   - Option A: Automatic (if you have auto-deploy enabled, just push to GitHub)
   - Option B: Manual via Vercel dashboard (Deployments → Redeploy)
   - Option C: Via CLI:
     ```bash
     vercel --prod
     ```

5. **Verify the deployment**:
   - Test the form submission
   - Check that emails are being sent
   - Verify in Vercel dashboard under Functions that `submit.js` is listed

## Troubleshooting

### Still getting 404 errors?

1. **Clear Vercel cache**: In your Vercel project settings, try redeploying with cache cleared
2. **Check Functions tab**: Go to Vercel dashboard → Your Project → Functions. You should see `api/submit.js` listed
3. **Verify environment variables**: Make sure all SMTP environment variables are still configured in Vercel

### Email not sending?

1. **Check logs**: Go to Vercel dashboard → Deployments → Latest → Functions → Click on `api-submit`
2. **Verify credentials**: Ensure your SMTP credentials are correct and environment variables are set
3. **Test locally**: You can test the Node.js function locally if needed

## Benefits of the Migration

1. ✅ **Compatible with Vercel free tier** (Python runtime is no longer supported)
2. ✅ **Faster cold starts** (Node.js functions start faster than Python on Vercel)
3. ✅ **Better integration** (Node.js is Vercel's primary runtime)
4. ✅ **Future-proof** (No risk of deprecated runtimes)

## Notes

- The old `api/submit.py` file is kept in the repository for reference but is not used
- `requirements.txt` is also kept for reference
- `server.py` (local development server) still exists for Python-based local testing if preferred
- The Node.js serverless function is production-ready and fully tested

## Support

If you encounter any issues during migration:
1. Check the troubleshooting section above
2. Review the [Vercel Deployment Guide](VERCEL_DEPLOYMENT.md)
3. Open an issue on GitHub with details about the error
