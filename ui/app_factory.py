from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from flask import Flask
from typing import Optional

from config.settings import AppConfig
from core.message_bus import MessageBus
from core.job_manager import JobManager
from ui.layouts.main_layout import create_main_layout
from ui.callbacks import register_all_callbacks
from ui.state import UIStateManager
from tools import create_all_tools
from llm.client import LLMClient

# Theme mapping
THEMES = {
    "BOOTSTRAP": dbc.themes.BOOTSTRAP,
    "CYBORG": dbc.themes.CYBORG,
    "DARKLY": dbc.themes.DARKLY,
    "FLATLY": dbc.themes.FLATLY,
    "JOURNAL": dbc.themes.JOURNAL,
    "LITERA": dbc.themes.LITERA,
    "LUMEN": dbc.themes.LUMEN,
    "LUX": dbc.themes.LUX,
    "MATERIA": dbc.themes.MATERIA,
    "MINTY": dbc.themes.MINTY,
    "PULSE": dbc.themes.PULSE,
    "SANDSTONE": dbc.themes.SANDSTONE,
    "SIMPLEX": dbc.themes.SIMPLEX,
    "SKETCHY": dbc.themes.SKETCHY,
    "SPACELAB": dbc.themes.SPACELAB,
    "UNITED": dbc.themes.UNITED,
    "YETI": dbc.themes.YETI
}


def create_app(server: Optional[Flask] = None) -> Dash:
    """Create and configure the Dash application"""
    
    # Get theme
    theme_name = AppConfig.theme.upper()
    theme = THEMES.get(theme_name, dbc.themes.BOOTSTRAP)
    
    # Create Dash app
    app = Dash(
        __name__,
        server=server,
        external_stylesheets=[theme],
        suppress_callback_exceptions=True,
        title="Data Science UI"
    )
    
    # Initialize core components
    message_bus = MessageBus()
    job_manager = JobManager(message_bus)
    
    # Create LLM client first, which now instantiates the LLM
    llm_client = LLMClient(job_manager, message_bus)
    
    # Create tools dictionary, passing the now-available LLM to the creator
    tools = create_all_tools(job_manager, message_bus, llm=llm_client.llm)
    
    # Register all tools with the client
    llm_client.register_tools(tools)
    
    # Store references in app config for callbacks
    app.llm_client = llm_client
    app.job_manager = job_manager
    app.message_bus = message_bus
    app.ui_state = UIStateManager()
    
    # Set layout
    app.layout = create_main_layout()
    
    # Register callbacks
    register_all_callbacks(app, message_bus, job_manager, llm_client, app.ui_state, list(tools.values()))
    
    print("✓ Dash app created and configured")
    return app