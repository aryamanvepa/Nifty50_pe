# Nifty 50 P/E Tracker

A web application that automatically scrapes P/E (Price-to-Earnings) ratios for all Nifty 50 companies daily at market close and displays them in interactive line graphs.

## Features

- **Automated Daily Scraping**: Runs automatically at 3:30 PM IST (market close) every weekday
- **Historical Data Tracking**: Stores all P/E data in a database for historical analysis
- **Interactive Charts**: Beautiful line graphs showing P/E movement over time
- **Flexible Time Ranges**: View data for the past week, month, or all available data
- **Company Selection**: Choose which companies to display on the chart
- **Manual Scraping**: Trigger scraping manually for testing

## Project Structure

```
.
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      # FastAPI application
│   │   ├── database.py  # Database models and setup
│   │   ├── scraper.py   # Web scraping logic (uses NSE service)
│   │   └── scheduler.py # Scheduled job management
│   ├── nse_service/     # Node.js NSE service (using stock-nse-india)
│   │   ├── service.js   # Express service wrapper
│   │   ├── package.json
│   │   └── README.md
│   ├── requirements.txt
│   └── run.py          # Application entry point
├── frontend/          # React frontend
│   ├── public/
│   ├── src/
│   │   ├── App.js      # Main React component
│   │   ├── App.css     # Styles
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- **Python 3.8+** for the backend
- **Node.js 18+** for the NSE service
- **npm** or **yarn** for Node.js packages

### NSE Service Setup (Required)

The application uses the [stock-nse-india](https://github.com/hi-imcodeman/stock-nse-india) package via a Node.js service for reliable NSE data access.

1. Navigate to the NSE service directory:
```bash
cd backend/nse_service
```

2. Install dependencies:
```bash
npm install
```

3. Start the NSE service:
```bash
npm start
# Or on Windows: start_service.bat
# Or on Linux/Mac: ./start_service.sh
```

The NSE service will run on `http://localhost:3001`

**Note**: Keep this service running while using the application. The Python backend will automatically use it for scraping P/E data.

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set NSE service URL if running on a different port:
```bash
# Windows PowerShell
$env:NSE_SERVICE_URL="http://localhost:3001"

# Linux/Mac
export NSE_SERVICE_URL=http://localhost:3001
```

5. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

**Important**: Make sure the NSE service is running before starting the backend, or the scraper will fall back to direct NSE API calls (which may be less reliable).

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **First Run**: The database will be created automatically. You may want to trigger a manual scrape to populate initial data.

2. **Manual Scraping**: Click the "Trigger Scrape Now" button in the web interface to manually scrape P/E data.

3. **Viewing Data**: 
   - Select companies from the checkbox list
   - Choose a time range (Week, Month, or All Time)
   - The chart will update automatically

4. **Automatic Scraping**: The scheduler runs automatically at 3:30 PM IST on weekdays. Make sure the backend server is running.

## API Endpoints

- `GET /api/companies` - Get all companies
- `GET /api/pe-data/all` - Get P/E data for all companies (with optional date filters)
- `GET /api/pe-data/{company_id}` - Get P/E data for a specific company
- `POST /api/scrape-now` - Manually trigger scraping
- `GET /api/stats` - Get statistics about stored data

## Notes

- **NSE Service Integration**: The scraper uses the [stock-nse-india](https://github.com/hi-imcodeman/stock-nse-india) package via a Node.js service for more reliable data access. This provides better error handling and data extraction compared to direct API calls.
- **Fallback Mechanism**: If the NSE service is unavailable, the scraper automatically falls back to direct NSE API calls.
- **Batch Processing**: When using the NSE service, P/E data is fetched in batches for better performance.
- The database is SQLite by default (stored as `nifty50_pe_data.db` in the backend directory).
- For production, consider using PostgreSQL and proper environment variables for configuration.

## Troubleshooting

- **No data showing**: Make sure you've triggered at least one scrape (manual or automatic)
- **Scraping fails**: Check if NSE website structure has changed. You may need to update the scraper logic.
- **CORS errors**: Ensure the frontend URL is in the CORS allowed origins in `backend/app/main.py`

## Production Deployment

### Option 1: Standalone Production Build

1. **Build the frontend:**
   ```bash
   # Windows
   build.bat
   
   # Linux/Mac
   chmod +x build.sh
   ./build.sh
   ```

2. **Run in production mode:**
   ```bash
   cd backend
   set ENVIRONMENT=production  # Windows
   # export ENVIRONMENT=production  # Linux/Mac
   python run_production.py
   ```

   The application will be available at `http://localhost:8000` with both frontend and backend served together.

### Option 2: Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

   This will:
   - Build the frontend
   - Build the backend
   - Build the NSE service
   - Start all services together

2. **Access the application:**
   - Web app: `http://localhost:8000`
   - API: `http://localhost:8000/api/stats`

3. **Stop the services:**
   ```bash
   docker-compose down
   ```

### Option 3: Manual Docker Build

1. **Build the Docker image:**
   ```bash
   docker build -t nifty50-pe-tracker .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 \
     -v $(pwd)/backend/nifty50_pe_data.db:/app/nifty50_pe_data.db \
     -e ENVIRONMENT=production \
     nifty50-pe-tracker
   ```

### Environment Variables

For production deployment, you can set these environment variables:

- `ENVIRONMENT`: Set to `production` to enable static file serving
- `FRONTEND_BUILD_PATH`: Path to frontend build (default: `../frontend/build`)
- `PORT`: Server port (default: `8000`)
- `HOST`: Server host (default: `0.0.0.0`)
- `NSE_SERVICE_URL`: URL of NSE service (default: `http://localhost:3001`)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: `*` in production)
- `WORKERS`: Number of Uvicorn workers (default: `4`)

### Deployment Platforms

#### Heroku

1. Create a `Procfile`:
   ```
   web: cd backend && python run_production.py
   ```

2. Set environment variables in Heroku dashboard:
   - `ENVIRONMENT=production`
   - `FRONTEND_BUILD_PATH=./frontend_build`

3. Deploy:
   ```bash
   git push heroku main
   ```

#### Railway / Render

1. Set build command:
   ```bash
   ./build.sh && cd backend && python run_production.py
   ```

2. Set environment variables in platform dashboard

#### VPS / Cloud Server

1. Build the application:
   ```bash
   ./build.sh
   ```

2. Use a process manager like PM2 or systemd:
   ```bash
   # With PM2
   pm2 start backend/run_production.py --name nifty50-tracker --interpreter python3
   ```

3. Set up Nginx reverse proxy (optional but recommended):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Future Enhancements

- Add more technical indicators
- Email alerts for significant P/E changes
- Export data to CSV/Excel
- User authentication and saved preferences
- Comparison tools between companies
