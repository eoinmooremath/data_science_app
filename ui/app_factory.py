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
    "MORPH": dbc.themes.MORPH,
    "PULSE": dbc.themes.PULSE,
    "QUARTZ": dbc.themes.QUARTZ,
    "SANDSTONE": dbc.themes.SANDSTONE,
    "SIMPLEX": dbc.themes.SIMPLEX,
    "SKETCHY": dbc.themes.SKETCHY,
    "SLATE": dbc.themes.SLATE,
    "SOLAR": dbc.themes.SOLAR,
    "SPACELAB": dbc.themes.SPACELAB,
    "SUPERHERO": dbc.themes.SUPERHERO,
    "UNITED": dbc.themes.UNITED,
    "VAPOR": dbc.themes.VAPOR,
    "YETI": dbc.themes.YETI,
    "ZEPHYR": dbc.themes.ZEPHYR
}

def create_app(server: Optional[Flask] = None) -> Dash:
    """Factory function to create the Dash application"""
    
    # Create Dash app
    app = Dash(
        __name__,
        server=server,
        external_stylesheets=[THEMES.get(AppConfig.theme, dbc.themes.BOOTSTRAP)],
        title=AppConfig.app_title,
        update_title="Loading...",
        suppress_callback_exceptions=True
    )
    
    # Initialize core components
    message_bus = MessageBus()
    message_bus.start()
    
    job_manager = JobManager(message_bus)
    
    # Initialize tools
    tools = create_all_tools(job_manager, message_bus)
    
    # Initialize LLM client if API key is available
    llm_client = None
    if AppConfig.anthropic_api_key:
        llm_client = LLMClient(job_manager, tools)
        print("✓ LLM client initialized")
    else:
        print("⚠️  No ANTHROPIC_API_KEY found. Running without LLM support.")
    
    # Initialize UI state
    ui_state = UIStateManager()
    
    # Create layout
    app.layout = create_main_layout()
    
    # Register all callbacks
    register_all_callbacks(
        app=app,
        message_bus=message_bus,
        job_manager=job_manager,
        llm_client=llm_client,
        ui_state=ui_state,
        tools=tools
    )
    
    # Store components in app for access
    app.message_bus = message_bus
    app.job_manager = job_manager
    app.llm_client = llm_client
    app.ui_state = ui_state
    
    return app