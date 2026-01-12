@echo off
REM Adobe Premiere AI Captioning Tool - Quick Launch Script
REM Usage: caption_video.bat input.mp4
REM Or drag-and-drop a video file onto this .bat file

setlocal enabledelayedexpansion

echo ========================================
echo Adobe Premiere AI Captioning Tool
echo ========================================
echo.

REM Check if video file is provided
if "%~1"=="" (
    echo ERROR: No video file provided!
    echo.
    echo Usage:
    echo   caption_video.bat input.mp4
    echo   OR drag and drop a video file onto this script
    echo.
    pause
    exit /b 1
)

REM Check if file exists
if not exist "%~1" (
    echo ERROR: File not found: %~1
    echo.
    pause
    exit /b 1
)

REM Get the full path
set VIDEO_FILE=%~1
set VIDEO_NAME=%~n1
set VIDEO_DIR=%~dp1

echo Input: %VIDEO_NAME%%~x1
echo.

REM Run the Python script
python "%~dp0caption_tool.py" "%VIDEO_FILE%"

set ERRORLVL=%ERRORLEVEL%

echo.
if %ERRORLVL% EQU 0 (
    echo ========================================
    echo DONE! Check the output folder.
    echo ========================================
) else (
    echo ========================================
    echo ERROR: Captioning failed!
    echo ========================================
)

echo.
pause
exit /b %ERRORLVL%
