import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
import os
import tempfile

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOT_DATA_FILE = os.path.join(tempfile.gettempdir(), 'mcp_plot_data.json')

app.layout = dbc.Container([
    html.H1("Plot Display Monitor"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Visualization"),
            dcc.Graph(id="plot-display", style={"height": "500px"})
        ], width=8),
        
        dbc.Col([
            html.H3("What LLM Sees"),
            html.Pre(id="llm-view", style={
                "backgroundColor": "#f0f0f0", 
                "padding": "10px",
                "height": "500px",
                "overflow": "auto"
            })
        ], width=4)
    ], className="mt-3"),
    
    # Check for new plots every 500ms
    dcc.Interval(id="plot-interval", interval=500),
])

@app.callback(
    [Output("plot-display", "figure"),
     Output("llm-view", "children")],
    Input("plot-interval", "n_intervals")
)
def update_plot(n):
    try:
        if os.path.exists(PLOT_DATA_FILE):
            with open(PLOT_DATA_FILE, 'r') as f:
                plot_data = json.load(f)
            
            # Create appropriate plot based on type
            if plot_data["type"] == "scatter":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_data["x"],
                    y=plot_data["y"],
                    mode='markers',
                    marker=dict(size=8, opacity=0.6)
                ))
                fig.update_layout(
                    title=plot_data["title"],
                    xaxis_title=plot_data["xlabel"],
                    yaxis_title=plot_data["ylabel"]
                )
            
            elif plot_data["type"] == "histogram":
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=plot_data["values"],
                    nbinsx=50
                ))
                fig.update_layout(
                    title=plot_data["title"],
                    xaxis_title=plot_data["xlabel"],
                    yaxis_title=plot_data["ylabel"]
                )
            
            else:
                fig = go.Figure()
            
            # Show what LLM would see (without the actual data)
            llm_view = f"Plot Type: {plot_data['type']}\nTitle: {plot_data['title']}\n\n[LLM receives statistical summary, not raw plot data]"
            
            return fig, llm_view
        else:
            # Empty plot
            fig = go.Figure()
            fig.update_layout(title="Waiting for analysis...")
            return fig, "No analysis yet"
            
    except Exception as e:
        fig = go.Figure()
        fig.update_layout(title=f"Error: {str(e)}")
        return fig, f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, port=8051)  # Different port to run alongside progress monitor