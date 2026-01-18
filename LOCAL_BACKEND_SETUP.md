# Running Backend Locally for GitHub Pages

## ⚠️ Important Considerations

Running the backend locally for production has several limitations:

1. **Your computer must be running 24/7** - If you turn off your computer, the site breaks
2. **Internet connection required** - Your local network must be accessible from the internet
3. **Security concerns** - Exposing your local machine to the internet
4. **Not scalable** - Can't handle high traffic
5. **Dynamic IP issues** - Your IP address may change

**Recommended**: Use a cloud service (Railway, Render, Heroku) for production instead.

## Option 1: Using ngrok (Easiest)

ngrok creates a secure tunnel to your local backend.

### Setup Steps:

1. **Install ngrok:**
   - Download from https://ngrok.com/download
   - Or use: `choco install ngrok` (Windows) or `brew install ngrok` (Mac)

2. **Start your backend locally:**
   ```bash
   cd backend
   python run.py
   ```
   Backend runs on `http://localhost:8000`

3. **Create ngrok tunnel:**
   ```bash
   ngrok http 8000
   ```

4. **Copy the ngrok URL** (e.g., `https://abc123.ngrok.io`)

5. **Update GitHub Secret:**
   - Go to GitHub repo → Settings → Secrets → Actions
   - Update `REACT_APP_API_URL` with your ngrok URL
   - Example: `https://abc123.ngrok.io`

6. **Update CORS in backend:**
   ```python
   # In backend/app/main.py, add ngrok domain to CORS
   cors_origins = ["https://*.ngrok.io", "https://*.ngrok-free.app"]
   ```

### Limitations:
- **Free ngrok URLs expire** after 2 hours (paid plans have permanent URLs)
- Need to restart ngrok and update GitHub secret each time
- Not suitable for production

## Option 2: Port Forwarding (Advanced)

If you have a static IP and can configure your router:

1. **Configure router port forwarding:**
   - Forward external port (e.g., 8000) to your local machine:8000
   - Get your public IP address

2. **Update GitHub Secret:**
   - Set `REACT_APP_API_URL` to `http://YOUR_PUBLIC_IP:8000`

3. **Security concerns:**
   - Exposes your local machine directly
   - Need firewall configuration
   - Not recommended without proper security setup

## Option 3: Cloudflare Tunnel (Better Alternative)

Cloudflare Tunnel is more stable than ngrok:

1. **Install cloudflared:**
   ```bash
   # Windows: Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
   # Or use: choco install cloudflared
   ```

2. **Create tunnel:**
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

3. **Use the provided URL** in GitHub secrets

## Recommended: Use Cloud Hosting Instead

### Quick Setup with Railway (5 minutes):

1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub repo
4. Select your repository
5. Add Service → Select `backend` folder
6. Add environment variables:
   - `ENVIRONMENT=production`
   - `FRONTEND_BUILD_PATH=./frontend_build`
7. Railway gives you a permanent URL (e.g., `https://your-app.railway.app`)
8. Use this URL in GitHub secret `REACT_APP_API_URL`

**Benefits:**
- ✅ Free tier available
- ✅ Permanent URL
- ✅ Auto-deploys on git push
- ✅ Runs 24/7
- ✅ Better security
- ✅ Handles traffic spikes

## Testing Locally

If you just want to test locally (not for production):

1. **Run backend:**
   ```bash
   cd backend
   python run.py
   ```

2. **Run frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Access at:** `http://localhost:3000`

The frontend will automatically use `http://localhost:8000` in development mode.

## Summary

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **ngrok** | Quick setup | Temporary URLs, expires | Testing |
| **Port Forwarding** | Direct access | Security risks, setup complexity | Advanced users |
| **Cloudflare Tunnel** | More stable | Still requires local machine | Testing |
| **Cloud Hosting** | Permanent, secure, scalable | None | **Production** ✅ |

**For production, use cloud hosting (Railway/Render/Heroku).**
