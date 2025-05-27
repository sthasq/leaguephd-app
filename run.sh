#!/bin/bash

echo "Starting League PhD Web Application..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if required packages are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip3 install -r requirements_web.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install packages"
        exit 1
    fi
fi

echo
echo "========================================"
echo "  League PhD Web Application"
echo "========================================"
echo
echo "Starting application..."
echo "Your browser will open automatically."
echo
echo "To stop the application, press Ctrl+C"
echo

# Run the application
python3 app.py
