#!/bin/bash
# Build script for creating distribution packages

echo "======================================="
echo "League PhD - Distribution Builder"
echo "======================================="
echo

# Check if required tools are available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not available"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
rm -rf __pycache__/
rm -rf .pytest_cache/

# Create distribution directory
mkdir -p dist/

echo "Installing build dependencies..."
pip3 install build wheel pyinstaller

echo "Building Python package..."
python3 -m build

echo "Building standalone executable..."
pyinstaller LeaguePhD.spec --clean

# Create portable distribution
echo "Creating portable distribution..."
mkdir -p dist/league-phd-portable/
cp -r templates/ dist/league-phd-portable/
cp -r assets/ dist/league-phd-portable/
cp app.py ChampSelect.py config.py lcu_handler_web.py mock_lcu_handler.py dist/league-phd-portable/
cp requirements_web.txt dist/league-phd-portable/
cp install_and_run.* run.* dist/league-phd-portable/
cp README.md LICENSE dist/league-phd-portable/

echo "Creating archive..."
cd dist/
tar -czf league-phd-portable.tar.gz league-phd-portable/
zip -r league-phd-portable.zip league-phd-portable/

echo
echo "======================================="
echo "Build completed successfully!"
echo "======================================="
echo "Distribution files created in dist/:"
echo "- league-phd-portable.tar.gz (Linux/Mac)"
echo "- league-phd-portable.zip (Windows)"
echo "- Python wheel package"
echo "- Standalone executable (if PyInstaller succeeded)"
echo
