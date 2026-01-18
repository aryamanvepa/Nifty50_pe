# GitHub Pages Deployment Guide

## Important Note

**GitHub Pages only serves static files** - it cannot run Python/Node.js backends. This means:

1. **Frontend**: Can be deployed to GitHub Pages ✅
2. **Backend API**: Must be hosted separately (Railway, Render, Heroku, etc.) ⚠️

## Setup Instructions

### Step 1: Deploy Backend Separately

You need to host your backend API on a platform that supports Python:

**Option A: Railway (Recommended - Free tier available)**
1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Select the `backend` folder
4. Set environment variables:
   - `ENVIRONMENT=production`
   - `FRONTEND_BUILD_PATH=./frontend_build`
5. Railway will auto-deploy

**Option B: Render**
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && ENVIRONMENT=production python run_production.py`
5. Add environment variables

**Option C: Heroku**
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `heroku config:set ENVIRONMENT=production`
4. `git push heroku main`

### Step 2: Configure Frontend API URL

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add a new secret:
   - Name: `REACT_APP_API_URL`
   - Value: Your backend URL (e.g., `https://your-app.railway.app` or `https://your-app.herokuapp.com`)

### Step 3: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - **Source**: `GitHub Actions`
3. The workflow will automatically deploy on every push to `main`

### Step 4: Update Frontend for Production

The frontend is already configured to use `REACT_APP_API_URL` environment variable. The GitHub Actions workflow will use this to build the frontend with the correct API URL.

## How It Works

1. **GitHub Actions Workflow** (`deploy-pages.yml`):
   - Triggers on push to `main` branch
   - Builds the React frontend
   - Uses `REACT_APP_API_URL` secret for API endpoint
   - Deploys to GitHub Pages

2. **Frontend** (`frontend/src/App.js`):
   - Uses `process.env.REACT_APP_API_URL` or defaults to localhost in development
   - In production (GitHub Pages), it will use the backend URL you configured

3. **Backend**:
   - Runs on Railway/Render/Heroku
   - Serves API at `/api/*` endpoints
   - CORS is configured to allow GitHub Pages domain

## Testing Locally

Before deploying, test that your frontend can connect to your backend:

1. Deploy backend first
2. Update `frontend/src/App.js` temporarily:
   ```javascript
   const API_BASE_URL = 'https://your-backend-url.railway.app';
   ```
3. Build and test:
   ```bash
   cd frontend
   npm run build
   npm install -g serve
   serve -s build
   ```

## Troubleshooting

### Frontend can't connect to backend
- Check CORS settings in `backend/app/main.py`
- Verify backend URL is correct in GitHub Secrets
- Check browser console for errors

### GitHub Pages shows blank page
- Check browser console for errors
- Verify `REACT_APP_API_URL` secret is set correctly
- Check GitHub Actions workflow logs

### Backend not responding
- Verify backend is deployed and running
- Check backend logs on your hosting platform
- Test backend URL directly: `https://your-backend-url/api/stats`

## Alternative: Full-Stack Deployment

If you want everything in one place, consider:

- **Vercel**: Can deploy both frontend and backend (with serverless functions)
- **Railway**: Can deploy full-stack apps
- **Render**: Supports full-stack deployments
- **Fly.io**: Good for full-stack apps

These platforms can host both frontend and backend together, eliminating the need for GitHub Pages.
