# test_progress.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import time
import threading
import queue

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Queue for progress updates
progress_queue = queue.Queue()

app.layout = dbc.Container([
    html.H1("Progress Test"),
    
    dbc.Button("Start Long Operation", id="start-btn", color="primary"),
    
    html.Div(id="status-text", className="mt-3"),
    
    dbc.Progress(id="progress-bar", value=0, className="mt-3"),
    
    # Hidden interval component for polling progress
    dcc.Interval(id="progress-interval", interval=100, disabled=True),
])

def long_running_operation():
    """Simulates work being done"""
    for i in range(100):
        time.sleep(0.1)  # Simulate work
        progress_queue.put(i + 1)
    progress_queue.put("DONE")

@app.callback(
    [Output("progress-interval", "disabled"),
     Output("status-text", "children")],
    Input("start-btn", "n_clicks"),
    prevent_initial_call=True
)
def start_operation(n_clicks):
    # Start background thread
    thread = threading.Thread(target=long_running_operation)
    thread.start()
    
    return False, "Operation started..."

@app.callback(
    [Output("progress-bar", "value"),
     Output("progress-bar", "label"),
     Output("progress-interval", "disabled", allow_duplicate=True)],
    Input("progress-interval", "n_intervals"),
    prevent_initial_call=True
)
def update_progress(n):
    try:
        progress = progress_queue.get_nowait()
        if progress == "DONE":
            return 100, "100%", True
        else:
            return progress, f"{progress}%", False
    except queue.Empty:
        return dash.no_update, dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run(debug=True)