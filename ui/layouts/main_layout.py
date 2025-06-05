import dash_bootstrap_components as dbc
from dash import dcc, html
from config.settings import AppConfig
from ui.components.chat import create_chat_component
from ui.components.progress import create_progress_component
from ui.components.results_ledger import create_results_ledger_component
from ui.components.file_upload import create_file_upload_component
from ui.components.plot_tabs import create_plot_tabs_component
def create_main_layout():
    """Create the main application layout"""
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1(AppConfig.app_title, className="mb-4"),
                html.Hr()
            ])
        ]),
        
        # Main content
        dbc.Row([
            # Left column - Chat and File Upload
            dbc.Col([
                create_chat_component("main-chat"),
                html.Div(className="mb-3"),
                create_file_upload_component("main-file")
            ], width=12, lg=4),
            
            # Middle column - Progress and Results
            dbc.Col([
                create_progress_component("main-progress"),
                html.Div(className="mb-3"),
                create_results_ledger_component("main-results")
            ], width=12, lg=4),
            
            # Right column - Visualizations
            dbc.Col([
                create_plot_tabs_component("main-plots")
            ], width=12, lg=4)
        ], className="g-3"),  # Add gutters between columns
        
        # Hidden components and stores
        dcc.Interval(
            id="update-interval",
            interval=AppConfig.update_interval_ms
        ),
        dcc.Store(id="current-job-store"),
        dcc.Store(id="message-trigger", data=0),
        dcc.Store(id="active-tab-store", data="tab-0"),
        dcc.Download(id="download-results"),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P(
                    "Data Science Assistant - Powered by Claude",
                    className="text-center text-muted"
                )
            ])
        ], className="mt-5")
    ], fluid=True, className="py-3")