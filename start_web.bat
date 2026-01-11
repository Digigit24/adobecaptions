@echo off
REM Adobe Premiere AI Captioning Tool - Web Interface Launcher
REM Double-click this file to start the web server

setlocal enabledelayedexpansion

echo ========================================
echo Adobe Premiere AI Captioning Tool
echo Web Interface
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.11.9 and add it to PATH.
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
echo.

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not installed. Installing dependencies...
    pip install flask flask-cors
    echo.
)

echo Starting web server...
echo.
echo ========================================
echo   Open in your browser:
echo   http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python "%~dp0web_server.py"

pause
