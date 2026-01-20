@echo off
echo Stopping all Nifty 50 P/E Tracker services...
echo.

REM Kill Node.js processes (NSE Service and Frontend)
taskkill /FI "WINDOWTITLE eq NSE Service*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Frontend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Backend API*" /T /F >nul 2>&1

REM Kill by process name as backup
taskkill /IM node.exe /F >nul 2>&1
taskkill /IM python.exe /F >nul 2>&1

REM Kill processes on specific ports
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3001" ^| findstr "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000" ^| findstr "LISTENING"') do taskkill /F /PID %%a >nul 2>&1

echo All services stopped.
pause
