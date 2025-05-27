@echo off
REM LeaguePhD Installer and Runner for Windows
echo =======================================
echo League PhD - Automated Installation
echo =======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; print(f'Python {sys.version}')"
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements_web.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo =======================================
echo Starting League PhD...
echo =======================================
echo.
echo The application will open in your web browser.
echo Keep this window open while using the application.
echo Press Ctrl+C to stop the application.
echo.

python app.py

echo.
echo Application stopped.
pause
