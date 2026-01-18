import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date
import time
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nifty 50 companies list
NIFTY_50_SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", "BHARTIARTL",
    "SBIN", "BAJFINANCE", "LICI", "ITC", "SUNPHARMA", "AXISBANK", "KOTAKBANK",
    "LT", "HCLTECH", "ASIANPAINT", "MARUTI", "ULTRACEMCO", "TITAN", "NTPC",
    "NESTLEIND", "WIPRO", "ONGC", "POWERGRID", "M&M", "TATAMOTORS", "ADANIENT",
    "JSWSTEEL", "ADANIPORTS", "TATASTEEL", "HDFCLIFE", "BAJAJFINSV", "COALINDIA",
    "DIVISLAB", "TECHM", "GRASIM", "HINDALCO", "CIPLA", "SBILIFE", "BRITANNIA",
    "EICHERMOT", "APOLLOHOSP", "DRREDDY", "BPCL", "HEROMOTOCO", "INDUSINDBK",
    "VEDL", "GODREJCP", "DABUR"
]


def scrape_pe_ratio(symbol: str) -> float:
    """
    Scrape P/E ratio for a given stock symbol from NSE website
    """
    try:
        # NSE URL for stock quote
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        # First request to get cookies
        session.get("https://www.nseindia.com/", timeout=10)
        time.sleep(1)  # Be respectful with requests
        
        # Get quote data
        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Extract P/E ratio from the response
            if 'priceInfo' in data and 'pe' in data['priceInfo']:
                pe_ratio = data['priceInfo']['pe']
                if pe_ratio and pe_ratio > 0:
                    return float(pe_ratio)
            
            # Alternative: try to get from market data
            if 'marketStatus' in data and 'priceInfo' in data:
                price_info = data.get('priceInfo', {})
                if 'pe' in price_info:
                    pe_ratio = price_info['pe']
                    if pe_ratio and pe_ratio > 0:
                        return float(pe_ratio)
        
        logger.warning(f"Could not find P/E ratio for {symbol} from API")
        
        # Fallback: Try scraping from HTML page
        html_url = f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}"
        html_response = session.get(html_url, timeout=10)
        
        if html_response.status_code == 200:
            soup = BeautifulSoup(html_response.content, 'html.parser')
            # Look for P/E in the page
            pe_elements = soup.find_all(text=lambda text: text and 'P/E' in text)
            # This is a simplified approach - may need adjustment based on actual HTML structure
            
        return None
        
    except Exception as e:
        logger.error(f"Error scraping P/E for {symbol}: {str(e)}")
        return None


def scrape_all_nifty50_pe() -> List[Dict]:
    """
    Scrape P/E ratios for all Nifty 50 companies
    Returns list of dicts with symbol and pe_ratio
    """
    results = []
    current_date = date.today()
    
    logger.info(f"Starting P/E scraping for Nifty 50 companies on {current_date}")
    
    for symbol in NIFTY_50_SYMBOLS:
        logger.info(f"Scraping P/E for {symbol}...")
        pe_ratio = scrape_pe_ratio(symbol)
        
        if pe_ratio:
            results.append({
                "symbol": symbol,
                "pe_ratio": pe_ratio,
                "date": current_date
            })
            logger.info(f"✓ {symbol}: P/E = {pe_ratio}")
        else:
            logger.warning(f"✗ {symbol}: Failed to get P/E ratio")
        
        # Be respectful - add delay between requests
        time.sleep(2)
    
    logger.info(f"Completed scraping. Got P/E data for {len(results)}/{len(NIFTY_50_SYMBOLS)} companies")
    return results


def scrape_pe_alternative_method(symbol: str) -> float:
    """
    Alternative method using yfinance or other data sources
    This is a placeholder - you may need to use paid APIs or other sources
    """
    try:
        # Alternative: Use yfinance if available
        # import yfinance as yf
        # stock = yf.Ticker(f"{symbol}.NS")
        # info = stock.info
        # return info.get('trailingPE') or info.get('forwardPE')
        pass
    except Exception as e:
        logger.error(f"Alternative scraping method failed for {symbol}: {str(e)}")
    
    return None
