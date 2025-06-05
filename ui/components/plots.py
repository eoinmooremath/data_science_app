import dash_bootstrap_components as dbc
from dash import dcc, html
from typing import Dict, Any, Optional

def create_plot_component(plot_id: str = "plot"):
    """Create a basic plot component container"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Plot", className="mb-0"),
            html.Small("Interactive visualization", className="text-muted")
        ]),
        dbc.CardBody([
            dcc.Graph(
                id=f"{plot_id}-graph",
                style={"height": "400px"}
            )
        ])
    ], style={"height": "100%"})

def create_empty_plot_message():
    """Create empty state message for plots"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-chart-line fa-3x text-muted mb-3"),
                html.H5("No visualizations yet", className="text-muted"),
                html.P("Upload data and ask for plots to see visualizations here.", 
                      className="text-muted mb-0")
            ], className="text-center py-5")
        ])
    ], className="h-100 d-flex align-items-center")