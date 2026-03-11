#!/usr/bin/env python3
"""Main entry point for the application."""

from app import create_app

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
