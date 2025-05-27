"""League PhD - Web-based desktop application for League of Legends draft analysis."""
import asyncio
import json
import logging
import sys
import threading
import webbrowser
from pathlib import Path
from typing import Optional

from flask import Flask, render_template, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import requests

from ChampSelect import ChampSelect
from config import APP_NAME, VERSION_FILE, GITHUB_API_URL, GITHUB_RELEASES_URL

# Try to import LCU handler, fall back to mock if not available
try:
    from lcu_handler_web import LCUHandlerWeb
    LCU_AVAILABLE = True
except ImportError:
    from mock_lcu_handler import LCUHandlerWeb
    LCU_AVAILABLE = False


class LeaguePhDApp:
    """Main League PhD web application."""
    
    def __init__(self, debug: bool = False):
        """Initialize the Flask application."""
        self.debug = debug
        self.setup_logging()
        
        # Flask app setup
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'leaguephd_secret_key_2024'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", async_mode='threading')
        
        # Components
        self.champ_select = ChampSelect()
        self.lcu_handler: Optional[LCUHandlerWeb] = None
        self.version = self.load_version()
        
        # Setup routes and events
        self.setup_routes()
        self.setup_socket_events()
        
        self.logger.info(f"Initialized {APP_NAME} v{self.version}")
        if not LCU_AVAILABLE:
            self.logger.warning("LCU driver not available - running in demo mode")
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO if self.debug else logging.WARNING,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_version(self) -> str:
        """Load version from version file."""
        try:
            with open(VERSION_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            self.logger.warning(f"Version file {VERSION_FILE} not found")
            return "Unknown"
    
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main page."""
            return render_template('index.html', 
                                 app_name=APP_NAME, 
                                 version=self.version)
        
        @self.app.route('/api/status')
        def status():
            """Get application status."""
            return jsonify({
                'connected': self.lcu_handler.connected if self.lcu_handler else False,
                'version': self.version,
                'champ_select_active': self.champ_select.active
            })
        
        @self.app.route('/api/version/check')
        def check_version():
            """Check for updates."""
            try:
                response = requests.get(GITHUB_API_URL, timeout=5)
                response.raise_for_status()
                latest_version = response.json()['tag_name']
                
                return jsonify({
                    'current': self.version,
                    'latest': latest_version,
                    'update_available': self.version != latest_version,
                    'download_url': GITHUB_RELEASES_URL
                })
            except Exception as e:
                self.logger.error(f"Failed to check version: {e}")
                return jsonify({'error': 'Failed to check for updates'}), 500
        
        @self.app.route('/assets/<path:filename>')
        def assets(filename):
            """Serve static assets."""
            return send_from_directory('assets', filename)
    
    def setup_socket_events(self):
        """Setup SocketIO events."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            self.logger.info('Client connected')
            # Send current state
            emit('status_update', {
                'connected': self.lcu_handler.connected if self.lcu_handler else False,
                'champ_select': self.champ_select.__repr__()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            self.logger.info('Client disconnected')
    
    def emit_champ_select_update(self, champ_select_data: dict, update_data: dict):
        """Emit champion select update to all connected clients."""
        self.socketio.emit('champ_select_update', {
            'champ_select': champ_select_data,
            'update': update_data
        })
    
    def emit_connection_status(self, connected: bool):
        """Emit connection status to all connected clients."""
        self.socketio.emit('connection_status', {'connected': connected})
    
    def start_lcu_handler(self):
        """Start LCU handler in background thread."""
        def run_lcu():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.lcu_handler = LCUHandlerWeb(
                self.champ_select,
                self.emit_champ_select_update,
                self.emit_connection_status,
                self.logger
            )
            
            try:
                loop.run_until_complete(self.lcu_handler.start())
            except Exception as e:
                self.logger.error(f"LCU Handler error: {e}")
            finally:
                loop.close()
        
        lcu_thread = threading.Thread(target=run_lcu, daemon=True)
        lcu_thread.start()
        self.logger.info("LCU handler started in background thread")
    
    def open_browser(self, host: str = '127.0.0.1', port: int = 5000):
        """Open the application in the default browser."""
        url = f"http://{host}:{port}"
        
        def open_url():
            import time
            time.sleep(1)  # Wait for server to start
            webbrowser.open(url)
        
        threading.Thread(target=open_url, daemon=True).start()
    
    def run(self, host: str = '127.0.0.1', port: int = 5000, open_browser: bool = True):
        """Run the Flask application."""
        self.logger.info(f"Starting {APP_NAME} on {host}:{port}")
        
        # Start LCU handler
        self.start_lcu_handler()
        
        # Open browser
        if open_browser:
            self.open_browser(host, port)
            print(f"\n🚀 {APP_NAME} is starting...")
            print(f"📱 Opening browser at: http://{host}:{port}")
            print(f"🔧 Debug mode: {'ON' if self.debug else 'OFF'}")
            print(f"📊 Version: {self.version}")
            print("\n💡 To stop the application, press Ctrl+C")
        
        try:
            # Run Flask app with SocketIO
            self.socketio.run(
                self.app,
                host=host,
                port=port,
                debug=False,  # We handle our own logging
                use_reloader=False  # Avoid issues with threading
            )
        except KeyboardInterrupt:
            self.logger.info("Application stopped by user")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            raise


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="League PhD Web Application")
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    parser.add_argument('--mock', action='store_true', help='Force mock mode (demo without League client)')
    args = parser.parse_args()
    
    # Force mock mode if requested
    if args.mock:
        global LCU_AVAILABLE
        LCU_AVAILABLE = False
    
    # Create and run app
    app = LeaguePhDApp(debug=args.debug)
    app.run(host=args.host, port=args.port, open_browser=not args.no_browser)


if __name__ == '__main__':
    main()
