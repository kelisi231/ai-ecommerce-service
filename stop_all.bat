@echo off
chcp 65001 >nul
cd /d "%~dp0"
rem Close windows opened by start_all.bat (also kills their processes)
taskkill /FI "WINDOWTITLE eq AI-CS*" /T /F >nul 2>&1
rem Fallback: kill by port (covers manually started services)
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8000,8001,8002 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"
echo Services on 8000/8001/8002 stopped.
pause
