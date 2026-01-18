# NSE Service

This is a Node.js service that wraps the `stock-nse-india` package to provide NSE data to the Python backend.

## Setup

1. Install Node.js (v18 or higher)
2. Install dependencies:
```bash
cd backend/nse_service
npm install
```

## Running the Service

```bash
npm start
```

The service will run on `http://localhost:3001`

## Endpoints

- `GET /health` - Health check
- `GET /api/pe/:symbol` - Get P/E ratio for a single symbol
- `GET /api/equity/:symbol` - Get full equity details
- `POST /api/pe/batch` - Get P/E ratios for multiple symbols (body: `{"symbols": ["RELIANCE", "TCS"]}`)
- `GET /api/market-status` - Get market status

## Integration with Python Backend

The Python scraper will call this service via HTTP requests.
