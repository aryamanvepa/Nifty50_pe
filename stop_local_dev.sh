#!/bin/bash

echo "Stopping all Nifty 50 P/E Tracker services..."
echo ""

# Kill processes by port
lsof -ti:3001 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Kill by process name
pkill -f "node.*service.js" 2>/dev/null
pkill -f "python.*run.py" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null

echo "All services stopped."
