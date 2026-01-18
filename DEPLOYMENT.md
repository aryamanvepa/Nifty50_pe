# Deployment Guide

This guide explains how to deploy the Nifty 50 P/E Tracker application to production.

## Quick Start

### 1. Build for Production

**Windows:**
```bash
build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

This will:
- Build the React frontend
- Copy the build to `backend/frontend_build`

### 2. Run in Production Mode

```bash
cd backend
set ENVIRONMENT=production  # Windows
# export ENVIRONMENT=production  # Linux/Mac
python run_production.py
```

The application will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts:
- Backend API server (port 8000)
- NSE Service (port 3001)
- Frontend served by backend

### Manual Docker Build

```bash
# Build the image
docker build -t nifty50-pe-tracker .

# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/backend/nifty50_pe_data.db:/app/nifty50_pe_data.db \
  -e ENVIRONMENT=production \
  nifty50-pe-tracker
```

## Platform-Specific Deployment

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
   ```bash
   heroku config:set ENVIRONMENT=production
   heroku config:set FRONTEND_BUILD_PATH=./frontend_build
   ```
5. Deploy: `git push heroku main`

### Railway

1. Connect your GitHub repository
2. Set build command: `./build.sh && cd backend && python run_production.py`
3. Set environment variables in Railway dashboard
4. Deploy automatically on push

### Render

1. Create a new Web Service
2. Connect your repository
3. Set:
   - Build Command: `./build.sh`
   - Start Command: `cd backend && ENVIRONMENT=production python run_production.py`
4. Add environment variables

### VPS / Cloud Server

1. **SSH into your server**
2. **Clone the repository:**
   ```bash
   git clone https://github.com/aryamanvepa/Nifty50_pe.git
   cd Nifty50_pe
   ```

3. **Build the application:**
   ```bash
   ./build.sh
   ```

4. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Set up a process manager (PM2):**
   ```bash
   npm install -g pm2
   pm2 start run_production.py --name nifty50-tracker --interpreter python3
   pm2 save
   pm2 startup
   ```

6. **Set up Nginx reverse proxy (optional):**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Set to `production` | `development` |
| `PORT` | Server port | `8000` |
| `HOST` | Server host | `0.0.0.0` |
| `FRONTEND_BUILD_PATH` | Path to frontend build | `../frontend/build` |
| `NSE_SERVICE_URL` | NSE service URL | `http://localhost:3001` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | `*` (production) |
| `WORKERS` | Number of Uvicorn workers | `4` |
| `DATABASE_URL` | Database connection string | `sqlite:///./nifty50_pe_data.db` |

## Production Checklist

- [ ] Build frontend: `npm run build` in frontend directory
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure CORS origins for your domain
- [ ] Set up database (consider PostgreSQL for production)
- [ ] Configure NSE service URL if running separately
- [ ] Set up SSL/HTTPS (recommended)
- [ ] Configure process manager (PM2, systemd, etc.)
- [ ] Set up monitoring and logging
- [ ] Configure backup for database
- [ ] Test all endpoints

## Troubleshooting

### Frontend not loading
- Check that `FRONTEND_BUILD_PATH` is correct
- Verify the build directory exists
- Check file permissions

### API not responding
- Verify backend is running
- Check port conflicts
- Review logs for errors

### Database issues
- Ensure database file has write permissions
- Consider using PostgreSQL for production
- Set up regular backups

## Security Considerations

1. **Use HTTPS**: Always use SSL/TLS in production
2. **Environment Variables**: Never commit secrets to git
3. **CORS**: Restrict CORS origins to your domain
4. **Database**: Use a production database (PostgreSQL recommended)
5. **Rate Limiting**: Consider adding rate limiting for API endpoints
6. **Authentication**: Add authentication if exposing sensitive data

## Support

For issues or questions, please open an issue on GitHub.
