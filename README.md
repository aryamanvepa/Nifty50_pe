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
│   │   ├── scraper.py   # Web scraping logic
│   │   └── scheduler.py # Scheduled job management
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

4. Run the backend server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

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

- The scraper uses the NSE (National Stock Exchange) API. Rate limiting and delays are implemented to be respectful.
- If scraping fails, you may need to adjust the scraping logic based on NSE website changes.
- The database is SQLite by default (stored as `nifty50_pe_data.db` in the backend directory).
- For production, consider using PostgreSQL and proper environment variables for configuration.

## Troubleshooting

- **No data showing**: Make sure you've triggered at least one scrape (manual or automatic)
- **Scraping fails**: Check if NSE website structure has changed. You may need to update the scraper logic.
- **CORS errors**: Ensure the frontend URL is in the CORS allowed origins in `backend/app/main.py`

## Future Enhancements

- Add more technical indicators
- Email alerts for significant P/E changes
- Export data to CSV/Excel
- User authentication and saved preferences
- Comparison tools between companies
