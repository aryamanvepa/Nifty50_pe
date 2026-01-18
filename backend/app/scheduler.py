from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import logging
from datetime import datetime
from .scraper import scrape_all_nifty50_pe
from .database import SessionLocal, Company, PEData
from sqlalchemy import and_

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IST timezone
IST = pytz.timezone('Asia/Kolkata')

scheduler = BackgroundScheduler(timezone=IST)


def save_pe_data_to_db(pe_data_list):
    """Save scraped P/E data to database"""
    db = SessionLocal()
    try:
        saved_count = 0
        for data in pe_data_list:
            # Get or create company
            company = db.query(Company).filter(Company.symbol == data['symbol']).first()
            if not company:
                company = Company(symbol=data['symbol'], name=data['symbol'])
                db.add(company)
                db.commit()
                db.refresh(company)
            
            # Check if data for this date already exists
            existing = db.query(PEData).filter(
                and_(
                    PEData.company_id == company.id,
                    PEData.date == data['date']
                )
            ).first()
            
            if not existing:
                pe_entry = PEData(
                    company_id=company.id,
                    date=data['date'],
                    pe_ratio=data['pe_ratio'],
                    timestamp=datetime.now()
                )
                db.add(pe_entry)
                saved_count += 1
        
        db.commit()
        logger.info(f"Saved {saved_count} new P/E data entries to database")
        
    except Exception as e:
        logger.error(f"Error saving P/E data to database: {str(e)}")
        db.rollback()
    finally:
        db.close()


def scheduled_scrape_job():
    """Job to run at market close (3:30 PM IST)"""
    logger.info("Starting scheduled P/E scraping job...")
    try:
        pe_data = scrape_all_nifty50_pe()
        if pe_data:
            save_pe_data_to_db(pe_data)
            logger.info("Scheduled scraping job completed successfully")
        else:
            logger.warning("No P/E data scraped in scheduled job")
    except Exception as e:
        logger.error(f"Scheduled scraping job failed: {str(e)}")


def start_scheduler():
    """Start the scheduler to run scraping at market close"""
    # Schedule job to run at 3:30 PM IST every weekday (Monday-Friday)
    scheduler.add_job(
        scheduled_scrape_job,
        trigger=CronTrigger(hour=15, minute=30, day_of_week='mon-fri', timezone=IST),
        id='daily_pe_scrape',
        name='Daily Nifty 50 P/E Scraping at Market Close',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("Scheduler started. Will run daily at 3:30 PM IST (market close)")


def stop_scheduler():
    """Stop the scheduler"""
    scheduler.shutdown()
    logger.info("Scheduler stopped")
