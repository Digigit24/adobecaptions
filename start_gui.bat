@echo off
REM Adobe Premiere AI Captioning Tool - GUI Launcher
REM Double-click this file to start the GUI application

setlocal enabledelayedexpansion

echo ========================================
echo Adobe Premiere AI Captioning Tool - GUI
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

echo Starting GUI application...
echo.

REM Run the GUI
pythonw "%~dp0caption_gui.py"

REM If pythonw fails, try python
if errorlevel 1 (
    python "%~dp0caption_gui.py"
)

exit /b %ERRORLEVEL%
