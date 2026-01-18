import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompanies, setSelectedCompanies] = useState([]);
  const [peData, setPeData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('month'); // week, month, all
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchCompanies();
    fetchStats();
  }, []);

  useEffect(() => {
    if (selectedCompanies.length > 0) {
      fetchPEData();
    }
  }, [selectedCompanies, timeRange]);

  const fetchCompanies = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/companies`);
      setCompanies(response.data);
      // Select first 5 companies by default
      if (response.data.length > 0) {
        setSelectedCompanies(response.data.slice(0, 5).map(c => c.symbol));
      }
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchPEData = async () => {
    setLoading(true);
    try {
      const endDate = new Date();
      let startDate = new Date();
      
      if (timeRange === 'week') {
        startDate.setDate(endDate.getDate() - 7);
      } else if (timeRange === 'month') {
        startDate.setMonth(endDate.getMonth() - 1);
      } else {
        startDate = null; // All data
      }

      const params = {};
      if (startDate) {
        params.start_date = startDate.toISOString().split('T')[0];
      }
      params.end_date = endDate.toISOString().split('T')[0];

      const response = await axios.get(`${API_BASE_URL}/api/pe-data/all`, { params });
      
      // Filter for selected companies and format for chart
      const formattedData = formatDataForChart(response.data.filter(c => selectedCompanies.includes(c.symbol)));
      setPeData(formattedData);
    } catch (error) {
      console.error('Error fetching P/E data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDataForChart = (companiesData) => {
    // Create a map of dates to data points
    const dateMap = {};
    
    companiesData.forEach(company => {
      company.data.forEach(point => {
        const date = point.date;
        if (!dateMap[date]) {
          dateMap[date] = { date };
        }
        dateMap[date][company.symbol] = point.pe_ratio;
      });
    });

    // Convert to array and sort by date
    return Object.values(dateMap).sort((a, b) => new Date(a.date) - new Date(b.date));
  };

  const handleCompanyToggle = (symbol) => {
    setSelectedCompanies(prev => {
      if (prev.includes(symbol)) {
        return prev.filter(s => s !== symbol);
      } else {
        return [...prev, symbol];
      }
    });
  };

  const handleManualScrape = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/scrape-now`);
      alert(`Scraping completed: ${response.data.message}`);
      fetchPEData();
      fetchStats();
    } catch (error) {
      alert('Error triggering scrape: ' + error.message);
    }
  };

  const colors = [
    '#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#00ff00',
    '#0088fe', '#00c49f', '#ffbb28', '#ff8042', '#8884d8'
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nifty 50 P/E Ratio Tracker</h1>
        {stats && (
          <div className="stats">
            <span>Companies: {stats.total_companies}</span>
            <span>Records: {stats.total_records}</span>
            {stats.date_range.min && (
              <span>Date Range: {stats.date_range.min} to {stats.date_range.max}</span>
            )}
          </div>
        )}
      </header>

      <div className="controls">
        <div className="time-range-selector">
          <button 
            className={timeRange === 'week' ? 'active' : ''}
            onClick={() => setTimeRange('week')}
          >
            Week
          </button>
          <button 
            className={timeRange === 'month' ? 'active' : ''}
            onClick={() => setTimeRange('month')}
          >
            Month
          </button>
          <button 
            className={timeRange === 'all' ? 'active' : ''}
            onClick={() => setTimeRange('all')}
          >
            All Time
          </button>
        </div>

        <button className="scrape-button" onClick={handleManualScrape}>
          Trigger Scrape Now
        </button>
      </div>

      <div className="company-selector">
        <h3>Select Companies to Display:</h3>
        <div className="company-checkboxes">
          {companies.map((company, index) => (
            <label key={company.id} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedCompanies.includes(company.symbol)}
                onChange={() => handleCompanyToggle(company.symbol)}
              />
              <span>{company.symbol}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="chart-container">
        {loading ? (
          <div className="loading">Loading chart data...</div>
        ) : peData.length === 0 ? (
          <div className="no-data">No data available. Try triggering a scrape.</div>
        ) : (
          <ResponsiveContainer width="100%" height={600}>
            <LineChart data={peData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={100}
              />
              <YAxis 
                label={{ value: 'P/E Ratio', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip />
              <Legend />
              {selectedCompanies.map((symbol, index) => (
                <Line
                  key={symbol}
                  type="monotone"
                  dataKey={symbol}
                  stroke={colors[index % colors.length]}
                  strokeWidth={2}
                  dot={false}
                  name={symbol}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

export default App;
