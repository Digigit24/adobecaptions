@echo off
REM Adobe Premiere AI Captioning Tool - Advanced Options
REM This script provides interactive options for language and model selection

setlocal enabledelayedexpansion

echo ========================================
echo Adobe Premiere AI Captioning Tool
echo Advanced Mode
echo ========================================
echo.

REM Check if video file is provided
if "%~1"=="" (
    echo ERROR: No video file provided!
    echo.
    echo Usage: caption_video_advanced.bat input.mp4
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

set VIDEO_FILE=%~1
set VIDEO_NAME=%~n1

echo Input: %VIDEO_NAME%%~x1
echo.

REM Language selection
echo Select Language:
echo   1. Auto-detect (recommended)
echo   2. English
echo   3. Hindi
echo   4. Marathi
echo.
set /p LANG_CHOICE="Enter choice (1-4) [default: 1]: "

if "%LANG_CHOICE%"=="" set LANG_CHOICE=1

set LANG_PARAM=
if "%LANG_CHOICE%"=="2" set LANG_PARAM=-l en
if "%LANG_CHOICE%"=="3" set LANG_PARAM=-l hi
if "%LANG_CHOICE%"=="4" set LANG_PARAM=-l mr

echo.

REM Model selection
echo Select Whisper Model:
echo   1. tiny   (fastest, least accurate)
echo   2. base   (balanced - recommended)
echo   3. small  (better accuracy, slower)
echo   4. medium (high accuracy, much slower)
echo.
set /p MODEL_CHOICE="Enter choice (1-4) [default: 2]: "

if "%MODEL_CHOICE%"=="" set MODEL_CHOICE=2

set MODEL_PARAM=-m base
if "%MODEL_CHOICE%"=="1" set MODEL_PARAM=-m tiny
if "%MODEL_CHOICE%"=="2" set MODEL_PARAM=-m base
if "%MODEL_CHOICE%"=="3" set MODEL_PARAM=-m small
if "%MODEL_CHOICE%"=="4" set MODEL_PARAM=-m medium

echo.
echo ========================================
echo Processing...
echo ========================================
echo.

REM Run the Python script with parameters
python "%~dp0caption_tool.py" "%VIDEO_FILE%" %LANG_PARAM% %MODEL_PARAM%

set ERRORLVL=%ERRORLEVEL%

echo.
if %ERRORLVL% EQU 0 (
    echo ========================================
    echo SUCCESS!
    echo ========================================
) else (
    echo ========================================
    echo ERROR: Processing failed!
    echo ========================================
)

echo.
pause
exit /b %ERRORLVL%
