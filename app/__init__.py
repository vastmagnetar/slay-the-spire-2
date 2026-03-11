"""Flask application setup and initialization."""

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
from app.websocket import register_handlers
import os


def create_app():
    """Create and configure Flask app."""
    
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config['SECRET_KEY'] = 'slay-the-spire-secret'
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Register WebSocket handlers
    register_handlers(socketio)
    
    # Routes
    @app.route('/')
    def index():
        """Main game page."""
        return send_from_directory('static', 'index.html')
    
    @app.route('/health')
    def health():
        """Health check."""
        return {'status': 'ok'}, 200
    
    return app, socketio


if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
