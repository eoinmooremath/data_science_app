# dash_progress_monitor.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import json
import os
import tempfile
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

PROGRESS_FILE = os.path.join(tempfile.gettempdir(), 'mcp_progress.json')

app.layout = dbc.Container([
    html.H1("MCP Operation Monitor"),
    
    html.Div(id="operation-status", className="mt-3"),
    
    dbc.Progress(
        id="progress-bar", 
        value=0, 
        className="mt-3",
        style={"height": "30px"}
    ),
    
    html.Div(id="progress-message", className="mt-2 text-muted"),
    
    html.Div(id="last-update", className="mt-2 text-muted small"),
    
    # Poll for updates every 100ms
    dcc.Interval(id="progress-interval", interval=100),
])

@app.callback(
    [Output("progress-bar", "value"),
     Output("progress-bar", "label"),
     Output("progress-message", "children"),
     Output("operation-status", "children"),
     Output("last-update", "children")],
    Input("progress-interval", "n_intervals")
)
def update_progress(n):
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                data = json.load(f)
            
            progress = data["progress"]
            message = data["message"]
            timestamp = data.get("timestamp", 0)
            
            if progress >= 100:
                status = html.Div([
                    html.I(className="bi bi-check-circle-fill text-success me-2"),
                    "Operation Complete"
                ])
            elif progress > 0:
                status = html.Div([
                    html.I(className="bi bi-gear-fill text-primary me-2"),
                    "Operation Running"
                ])
            else:
                status = html.Div([
                    html.I(className="bi bi-pause-circle text-secondary me-2"),
                    "Waiting for operation..."
                ])
            
            last_update = f"Last update: {datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')[:-3]}"
            
            return progress, f"{progress:.0f}%", message, status, last_update
        else:
            return 0, "0%", "No operation running", "Waiting for MCP server...", ""
    except Exception as e:
        return 0, "0%", f"Error: {str(e)}", "Error", ""

if __name__ == "__main__":
    app.run(debug=True)