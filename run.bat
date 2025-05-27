@echo off
echo Starting League PhD Web Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements_web.txt
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  League PhD Web Application
echo ========================================
echo.
echo Starting application...
echo Your browser will open automatically.
echo.
echo To stop the application, press Ctrl+C
echo.

REM Run the application
python app.py

echo.
echo Application stopped.
pause
