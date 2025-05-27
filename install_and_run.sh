#!/bin/bash
# LeaguePhD Installer and Runner for Linux/Mac
echo "======================================="
echo "League PhD - Automated Installation"
echo "======================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager or https://python.org"
    exit 1
fi

echo "Python found. Checking version..."
python3 --version
echo

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not available"
    echo "Please install pip3 for your system"
    exit 1
fi

echo "Installing/updating dependencies..."
pip3 install -r requirements_web.txt

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "======================================="
echo "Starting League PhD..."
echo "======================================="
echo
echo "The application will open in your web browser."
echo "Keep this terminal open while using the application."
echo "Press Ctrl+C to stop the application."
echo

python3 app.py
