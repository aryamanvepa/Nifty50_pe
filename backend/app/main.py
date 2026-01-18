from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import date, datetime, timedelta
from .database import get_db, Company, PEData, init_db
from .scraper import scrape_all_nifty50_pe
from .scheduler import start_scheduler, stop_scheduler
from pydantic import BaseModel
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_BUILD_PATH = os.getenv("FRONTEND_BUILD_PATH", "../frontend/build")

app = FastAPI(title="Nifty 50 P/E Tracker API")

# CORS middleware - more permissive in production
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
if ENVIRONMENT == "production":
    # In production, allow all origins or specify your domain
    # Add GitHub Pages domain if using GitHub Pages for frontend
    default_origins = ["*"] if os.getenv("CORS_ORIGINS") is None else os.getenv("CORS_ORIGINS").split(",")
    # Add common GitHub Pages patterns
    github_pages_patterns = [
        "https://*.github.io",
        "https://aryamanvepa.github.io"
    ]
    cors_origins = default_origins + github_pages_patterns if "*" not in default_origins else default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    start_scheduler()
    logger.info("Application started and scheduler initialized")


@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()
    logger.info("Application shutdown and scheduler stopped")


# Pydantic models for API responses
class CompanyResponse(BaseModel):
    id: int
    symbol: str
    name: Optional[str]
    sector: Optional[str]

    class Config:
        from_attributes = True


class PEDataResponse(BaseModel):
    id: int
    company_id: int
    date: date
    pe_ratio: float
    timestamp: datetime

    class Config:
        from_attributes = True


class CompanyPEDataResponse(BaseModel):
    symbol: str
    name: Optional[str]
    data: List[dict]  # List of {date, pe_ratio}


@app.get("/api/companies", response_model=List[CompanyResponse])
async def get_companies(db: Session = Depends(get_db)):
    """Get all companies"""
    companies = db.query(Company).all()
    return companies


@app.get("/api/pe-data/all")
async def get_all_pe_data(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get P/E data for all companies"""
    query = db.query(
        Company.symbol,
        Company.name,
        PEData.date,
        PEData.pe_ratio
    ).join(
        PEData, Company.id == PEData.company_id
    )
    
    if start_date:
        query = query.filter(PEData.date >= start_date)
    if end_date:
        query = query.filter(PEData.date <= end_date)
    
    results = query.order_by(Company.symbol, PEData.date.asc()).all()
    
    # Group by company
    companies_data = {}
    for symbol, name, date_val, pe_ratio in results:
        if symbol not in companies_data:
            companies_data[symbol] = {
                "symbol": symbol,
                "name": name,
                "data": []
            }
        companies_data[symbol]["data"].append({
            "date": date_val.isoformat(),
            "pe_ratio": pe_ratio
        })
    
    return list(companies_data.values())


@app.get("/api/pe-data/{company_id}")
async def get_pe_data(
    company_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get P/E data for a specific company"""
    query = db.query(PEData).filter(PEData.company_id == company_id)
    
    if start_date:
        query = query.filter(PEData.date >= start_date)
    if end_date:
        query = query.filter(PEData.date <= end_date)
    
    pe_data = query.order_by(PEData.date.asc()).all()
    return pe_data


@app.post("/api/scrape-now")
async def trigger_scrape_now(db: Session = Depends(get_db)):
    """Manually trigger P/E scraping (for testing)"""
    try:
        logger.info("Manual scrape triggered")
        pe_data = scrape_all_nifty50_pe()
        
        if pe_data:
            from .scheduler import save_pe_data_to_db
            save_pe_data_to_db(pe_data)
            return {
                "success": True,
                "message": f"Scraped P/E data for {len(pe_data)} companies",
                "count": len(pe_data)
            }
        else:
            return {
                "success": False,
                "message": "No data scraped"
            }
    except Exception as e:
        logger.error(f"Manual scrape failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get statistics about the data"""
    total_companies = db.query(Company).count()
    total_records = db.query(PEData).count()
    
    # Get date range
    min_date = db.query(func.min(PEData.date)).scalar()
    max_date = db.query(func.max(PEData.date)).scalar()
    
    return {
        "total_companies": total_companies,
        "total_records": total_records,
        "date_range": {
            "min": min_date.isoformat() if min_date else None,
            "max": max_date.isoformat() if max_date else None
        }
    }


# Serve static files in production (must be after all API routes)
if ENVIRONMENT == "production":
    frontend_path = Path(FRONTEND_BUILD_PATH)
    if frontend_path.exists():
        # Mount static files (CSS, JS, images, etc.)
        static_path = frontend_path / "static"
        if static_path.exists():
            app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        
        # Serve React app for all non-API routes (React Router support)
        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            # Don't serve frontend for API routes
            if full_path.startswith("api"):
                raise HTTPException(status_code=404, detail="Not found")
            
            # Serve index.html for all other routes (React Router)
            index_path = frontend_path / "index.html"
            if index_path.exists():
                return FileResponse(str(index_path))
            else:
                raise HTTPException(status_code=404, detail="Frontend build not found")
    else:
        logger.warning(f"Frontend build path not found: {FRONTEND_BUILD_PATH}")
