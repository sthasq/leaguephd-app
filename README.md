# League PhD

🚀 **Modern Web-Based League of Legends Draft Analysis Tool**

A completely redesigned League PhD application that runs in your web browser, eliminating Windows compatibility issues while providing real-time champion select analysis and recommendations.

## ✨ Key Features

- 🌐 **Web-Based Architecture**: Runs in browser to solve PyQt5/DLL compatibility issues
- 🔄 **Real-Time Updates**: WebSocket communication for instant data synchronization
- 🎯 **Auto-Detection**: Automatically connects to League of Legends client
- 📊 **Modern UI**: Clean, responsive interface with real-time updates
- 🛡️ **Cross-Platform**: Works seamlessly on Windows, Mac, and Linux
- ⚡ **No Installation Hassles**: One-click setup with automatic dependency management

## 🛠️ System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher (auto-checked by installer)
- **Web Browser**: Chrome, Firefox, Edge, or Safari (modern versions)
- **League of Legends**: Client installation (optional - demo mode available)

## 🚀 Quick Start Guide

### ⚡ One-Click Installation (Recommended)

**Windows Users:**
1. Download the project files
2. Double-click `install_and_run.bat`
3. The installer will automatically:
   - Check Python installation
   - Install all dependencies
   - Start the application
   - Open your browser to the interface

**Mac/Linux Users:**
1. Download the project files
2. Open terminal in the project folder
3. Run: `./install_and_run.sh`
4. The installer handles everything automatically

### 🔧 Manual Installation

```bash
# Clone the repository
git clone https://github.com/your-username/leaguephd-app.git
cd leaguephd-app

# Install dependencies
pip install -r requirements_web.txt

# Run the application
python app.py
```

### 🎮 Demo Mode (No League Client Required)

Perfect for testing or showcasing:
```bash
python app.py --mock
```
```

## 💡 How to Use

1. **Start the Application**:
   - **Easy way**: Use `install_and_run.bat` (Windows) or `install_and_run.sh` (Mac/Linux)
   - **Manual way**: Run `python app.py` in terminal

2. **Browser Opens Automatically**: The app opens `http://localhost:5000` in your default browser

3. **League Client Connection**:
   - If League of Legends is running → Automatically connects
   - If not running → Runs in demo mode with sample data

4. **Champion Select Analysis**:
   - Enter champion select in League of Legends
   - View real-time pick/ban tracking and recommendations
   - Get team composition insights and suggestions

## 🏗️ Project Architecture

### Modern Web-Based Design

```
leaguephd-app/
├── app.py                    # Flask application server
├── ChampSelect.py           # Data models and game state
├── config.py                # Configuration constants
├── lcu_handler_web.py       # League Client API integration
├── mock_lcu_handler.py      # Demo mode simulator
├── requirements_web.txt     # Web-specific dependencies
├── templates/
│   └── index.html          # Modern web interface
├── assets/
│   └── icon.ico            # Application icon
└── Deployment Scripts:
    ├── install_and_run.bat  # Windows one-click installer
    ├── install_and_run.sh   # Mac/Linux one-click installer
    ├── run.bat              # Simple Windows runner
    └── run.sh               # Simple Mac/Linux runner
```

### Technical Stack

- **Backend**: Flask + SocketIO for real-time communication
- **Frontend**: Modern HTML5/CSS3/JavaScript with WebSocket support
- **LCU Integration**: Direct REST API communication with League Client
- **Cross-Platform**: Pure Python with web interface (no native dependencies)

## 🔧 Development

### Running in Development Mode

```bash
# Enable debug mode with detailed logging
python app.py --debug

# Run with mock data (no League client needed)
python app.py --mock

# Custom port
python app.py --port 8080
```

### Building for Distribution

**PyInstaller** (Single executable):
```bash
pip install pyinstaller
pyinstaller LeaguePhD.spec
```

**Docker** (Containerized deployment):
```bash
docker build -t leaguephd .
docker run -p 5000:5000 leaguephd
```

**Python Package**:
```bash
pip install build
python -m build
```

## 🔧 Troubleshooting

### ❌ Application Won't Start
- **Check Python**: Ensure Python 3.8+ is installed and in PATH
- **Use Auto-Installer**: The `install_and_run` scripts handle dependency issues
- **Port Conflict**: If port 5000 is busy, try: `python app.py --port 8080`

### ❌ Can't Connect to League Client
- **Start League First**: Launch League of Legends client before League PhD
- **Restart Both**: Close both applications and restart
- **Check API Access**: Ensure League client isn't in restricted mode

### ❌ Browser Issues
- **Manual Access**: Navigate to `http://localhost:5000` manually
- **Try Different Browser**: Test with Chrome, Firefox, or Edge
- **Firewall**: Check if Windows Firewall is blocking local connections

### ❌ Dependency Issues
```bash
# Clear pip cache and reinstall
pip cache purge
pip install --no-cache-dir -r requirements_web.txt

# Alternative: Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements_web.txt
```

## 🆚 Improvements Over Previous Version

| Feature | Old (PyQt5) | New (Web) |
|---------|-------------|-----------|
| **Compatibility** | Windows DLL issues | Universal browser support |
| **Installation** | Complex dependencies | One-click installers |
| **UI Updates** | GUI redraws | Real-time WebSocket |
| **Cross-Platform** | Windows-focused | True cross-platform |
| **Development** | Native GUI complexity | Standard web technologies |
| **Distribution** | Large executables | Lightweight Python |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes following the existing code style
4. **Test** your changes: `python app.py --debug`
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to the branch: `git push origin feature/amazing-feature`
7. **Submit** a pull request

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/your-username/leaguephd-app/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/leaguephd-app/discussions)
- **Wiki**: [Project Wiki](https://github.com/your-username/leaguephd-app/wiki)

---

⭐ **If this project helped you, please give it a star!** ⭐
2. Create a feature branch
3. Make your changes following the existing code style
4. Test your changes
5. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.
