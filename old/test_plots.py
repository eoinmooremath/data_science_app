# test_plots.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Store for plot metadata (this is what would go to LLM)
plot_metadata = {}

app.layout = dbc.Container([
    html.H1("Plot Display Test"),
    
    dbc.Button("Generate Plot", id="generate-btn", color="primary"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Local Display"),
            dcc.Graph(id="plot-display")
        ], width=8),
        
        dbc.Col([
            html.H3("What LLM Sees"),
            html.Pre(id="llm-data", style={"backgroundColor": "#f0f0f0", "padding": "10px"})
        ], width=4)
    ], className="mt-3")
])

@app.callback(
    [Output("plot-display", "figure"),
     Output("llm-data", "children")],
    Input("generate-btn", "n_clicks"),
    prevent_initial_call=True
)
def generate_plot(n_clicks):
    # Generate some data
    x = np.linspace(0, 10, 100)
    y = np.sin(x) + np.random.normal(0, 0.1, 100)
    
    # Create plot for local display
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_layout(title="Analysis Results")
    
    # Create metadata for LLM
    metadata = {
        "plot_type": "scatter",
        "title": "Analysis Results",
        "data_summary": {
            "x_range": [float(x.min()), float(x.max())],
            "y_range": [float(y.min()), float(y.max())],
            "n_points": len(x),
            "trend": "sinusoidal with noise"
        },
        "key_findings": "Sinusoidal pattern detected with period ≈ 2π"
    }
    
    # Display
    return fig, json.dumps(metadata, indent=2)

if __name__ == "__main__":
    app.run(debug=True)
