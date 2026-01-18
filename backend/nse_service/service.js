const express = require('express');
const { NseIndia } = require('stock-nse-india');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Enable CORS for Python backend
app.use(cors());
app.use(express.json());

const nseIndia = new NseIndia();

// Root endpoint
app.get('/', (req, res) => {
  res.json({ 
    service: 'NSE India Service',
    status: 'running',
    endpoints: {
      health: '/health',
      peRatio: '/api/pe/:symbol',
      equityDetails: '/api/equity/:symbol',
      batchPE: 'POST /api/pe/batch',
      marketStatus: '/api/market-status'
    }
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'NSE India Service' });
});

// Get P/E ratio for a symbol
app.get('/api/pe/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const equityDetails = await nseIndia.getEquityDetails(symbol);
    
    // Extract P/E ratio from equity details
    // Based on stock-nse-india package structure, P/E is in metadata.pdSymbolPe
    let peRatio = null;
    
    if (equityDetails) {
      // Primary location: metadata.pdSymbolPe (P/E ratio for the symbol)
      if (equityDetails.metadata && equityDetails.metadata.pdSymbolPe) {
        peRatio = equityDetails.metadata.pdSymbolPe;
      }
      // Fallback: metadata.pdSectorPe (sector P/E)
      else if (equityDetails.metadata && equityDetails.metadata.pdSectorPe) {
        peRatio = equityDetails.metadata.pdSectorPe;
      }
      // Additional fallbacks for other possible locations
      else if (equityDetails.priceInfo && equityDetails.priceInfo.pe) {
        peRatio = equityDetails.priceInfo.pe;
      } else if (equityDetails.info && equityDetails.info.pe) {
        peRatio = equityDetails.info.pe;
      } else if (equityDetails.securityInfo) {
        peRatio = equityDetails.securityInfo.pe || equityDetails.securityInfo.priceToEarning;
      }
    }
    
    if (peRatio && peRatio > 0) {
      res.json({ 
        symbol: symbol.toUpperCase(),
        pe_ratio: parseFloat(peRatio),
        success: true
      });
    } else {
      res.json({ 
        symbol: symbol.toUpperCase(),
        pe_ratio: null,
        success: false,
        message: 'P/E ratio not found in response'
      });
    }
  } catch (error) {
    console.error(`Error fetching P/E for ${req.params.symbol}:`, error.message);
    res.status(500).json({ 
      symbol: req.params.symbol.toUpperCase(),
      error: error.message,
      success: false
    });
  }
});

// Get equity details (full data)
app.get('/api/equity/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const equityDetails = await nseIndia.getEquityDetails(symbol);
    res.json({ symbol: symbol.toUpperCase(), data: equityDetails, success: true });
  } catch (error) {
    console.error(`Error fetching equity details for ${req.params.symbol}:`, error.message);
    res.status(500).json({ 
      symbol: req.params.symbol.toUpperCase(),
      error: error.message,
      success: false
    });
  }
});

// Batch get P/E ratios for multiple symbols
app.post('/api/pe/batch', async (req, res) => {
  try {
    const { symbols } = req.body;
    if (!Array.isArray(symbols)) {
      return res.status(400).json({ error: 'symbols must be an array' });
    }
    
    const results = [];
    
    for (const symbol of symbols) {
      try {
        const equityDetails = await nseIndia.getEquityDetails(symbol);
        let peRatio = null;
        
        if (equityDetails) {
          // Primary location: metadata.pdSymbolPe (P/E ratio for the symbol)
          if (equityDetails.metadata && equityDetails.metadata.pdSymbolPe) {
            peRatio = equityDetails.metadata.pdSymbolPe;
          }
          // Fallback: metadata.pdSectorPe (sector P/E)
          else if (equityDetails.metadata && equityDetails.metadata.pdSectorPe) {
            peRatio = equityDetails.metadata.pdSectorPe;
          }
          // Additional fallbacks
          else if (equityDetails.priceInfo && equityDetails.priceInfo.pe) {
            peRatio = equityDetails.priceInfo.pe;
          } else if (equityDetails.info && equityDetails.info.pe) {
            peRatio = equityDetails.info.pe;
          } else if (equityDetails.securityInfo) {
            peRatio = equityDetails.securityInfo.pe || equityDetails.securityInfo.priceToEarning;
          }
        }
        
        results.push({
          symbol: symbol.toUpperCase(),
          pe_ratio: peRatio && peRatio > 0 ? parseFloat(peRatio) : null,
          success: peRatio && peRatio > 0
        });
        
        // Small delay to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 500));
      } catch (error) {
        console.error(`Error fetching P/E for ${symbol}:`, error.message);
        results.push({
          symbol: symbol.toUpperCase(),
          pe_ratio: null,
          success: false,
          error: error.message
        });
      }
    }
    
    res.json({ results, success: true });
  } catch (error) {
    console.error('Error in batch P/E fetch:', error.message);
    res.status(500).json({ error: error.message, success: false });
  }
});

// Get market status
app.get('/api/market-status', async (req, res) => {
  try {
    const marketStatus = await nseIndia.getData('marketStatus');
    res.json({ data: marketStatus, success: true });
  } catch (error) {
    console.error('Error fetching market status:', error.message);
    res.status(500).json({ error: error.message, success: false });
  }
});

app.listen(PORT, () => {
  console.log(`NSE Service running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
