# dash_integrated_monitor_debug.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
from ipc.queue_manager import get_queue_manager, MessageType

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Global state
queue_manager = get_queue_manager()
active_jobs = {}  # job_id -> queue

# Add debug div
app.layout = dbc.Container([
    html.H1("Data Science Analysis Monitor"),
    
    # Job ID input (for testing)
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(id="job-id-input", placeholder="Enter job ID to monitor"),
                dbc.Button("Monitor", id="monitor-btn", color="primary")
            ])
        ], width=6),
        dbc.Col([
            html.Div(id="monitoring-status")
        ], width=6)
    ], className="mb-3"),
    
    # Progress section
    dbc.Card([
        dbc.CardHeader("Current Operation"),
        dbc.CardBody([
            html.Div(id="operation-message", className="mb-2"),
            dbc.Progress(id="progress-bar", value=0, style={"height": "25px"})
        ])
    ], className="mb-3"),
    
    # Plots section
    dbc.Card([
        dbc.CardHeader("Visualizations"),
        dbc.CardBody([
            dcc.Graph(id="main-plot", style={"height": "400px"})
        ])
    ], className="mb-3"),
    
    # Debug section
    dbc.Card([
        dbc.CardHeader("Debug Info"),
        dbc.CardBody([
            html.Pre(id="debug-output", style={"fontSize": "12px"})
        ])
    ]),
    
    # Hidden interval for polling
    dcc.Interval(id="update-interval", interval=100),
    
    # Store for current job
    dcc.Store(id="current-job-store")
])

@app.callback(
    [Output("monitoring-status", "children"),
     Output("current-job-store", "data")],
    Input("monitor-btn", "n_clicks"),
    State("job-id-input", "value"),
    prevent_initial_call=True
)
def start_monitoring(n_clicks, job_id):
    if not job_id:
        return "Please enter a job ID", None
    
    # Subscribe to job
    if job_id not in active_jobs:
        active_jobs[job_id] = queue_manager.subscribe_to_job(job_id)
        print(f"Subscribed to job: {job_id}")  # Debug
    
    return f"Monitoring job: {job_id}", job_id

@app.callback(
    [Output("operation-message", "children"),
     Output("progress-bar", "value"),
     Output("progress-bar", "label"),
     Output("main-plot", "figure"),
     Output("debug-output", "children")],
    Input("update-interval", "n_intervals"),
    State("current-job-store", "data"),
    prevent_initial_call=True
)
def update_display(n_intervals, job_id):
    debug_info = []
    
    if not job_id:
        return "Not monitoring any job", 0, "0%", go.Figure(), "No job selected"
    
    debug_info.append(f"Monitoring job: {job_id}")
    
    if job_id not in active_jobs:
        return "Job not subscribed", 0, "0%", go.Figure(), "Job not in active_jobs"
    
    # Get messages
    messages = queue_manager.get_messages(active_jobs[job_id], timeout=0.05)
    debug_info.append(f"Messages received: {len(messages)}")
    
    # Also check stored messages
    stored_messages = queue_manager.messages.get(job_id, [])
    debug_info.append(f"Stored messages: {len(stored_messages)}")
    
    # Process messages
    current_progress = 0
    current_message = "Waiting..."
    plot_figure = go.Figure()  # Default empty figure
    
    for msg in messages:
        debug_info.append(f"Message type: {msg.type.value}")
        
        if msg.type == MessageType.PROGRESS:
            current_progress = msg.data["progress"]
            current_message = msg.data["message"]
            debug_info.append(f"Progress: {current_progress}% - {current_message}")
            
        elif msg.type == MessageType.PLOT:
            debug_info.append("Plot message received!")
            plot_data = msg.data["plot_data"]
            
            # Create plot based on type
            if plot_data["type"] == "scatter":
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=plot_data["x"],
                    y=plot_data["y"],
                    mode='markers',
                    marker=dict(size=6, opacity=0.6)
                ))
                fig.update_layout(
                    title=plot_data["title"],
                    xaxis_title=plot_data["xlabel"],
                    yaxis_title=plot_data["ylabel"]
                )
                plot_figure = fig
                
            elif plot_data["type"] == "histogram":
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=plot_data["values"],
                    nbinsx=30
                ))
                fig.update_layout(
                    title=plot_data["title"],
                    xaxis_title=plot_data["xlabel"],
                    yaxis_title=plot_data["ylabel"]
                )
                plot_figure = fig
    
    # If no new messages, check current progress
    if not messages:
        progress_data = queue_manager.get_current_progress(job_id)
        if progress_data:
            current_progress = progress_data["progress"]
            current_message = progress_data["message"]
            debug_info.append(f"Current progress from storage: {current_progress}%")
        else:
            debug_info.append("No progress data found")
    
    debug_text = "\n".join(debug_info)
    
    return (
        current_message,
        current_progress,
        f"{int(current_progress)}%",
        plot_figure,
        debug_text
    )

if __name__ == "__main__":
    print("Queue Manager instance:", id(queue_manager))  # Debug
    print("Starting Dash app...")
    app.run(debug=True)