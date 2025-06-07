import os
import sys
import logging
from dash import Dash
import dash_bootstrap_components as dbc
from flask import Flask

# Disable Werkzeug request logging
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import configuration
from config.settings import AppConfig

# Import the main app factory
from ui.app_factory import create_app

# Create Flask server (for production deployment)
server = Flask(__name__)

# Create Dash app
app = create_app(server=server)

# Expose the server for WSGI
application = app.server

if __name__ == "__main__":
    # Start the LLM client's background thread now that the app is configured
    app.llm_client.start()
    
    # Print the URL for easy access
    print(f"🚀 Application starting on http://{AppConfig.host}:{AppConfig.port}")
    
    # Development mode
    app.run(
        debug=AppConfig.debug,
        host=AppConfig.host,
        port=AppConfig.port
    )