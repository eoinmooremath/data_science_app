# test_integrated_fixed.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import threading
import queue
import time
import numpy as np
from datetime import datetime
import uuid

# Import from your models file
from models import Message, Job, MessageType

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Simple message queue
message_queue = queue.Queue()
jobs = {}

# Store latest state per job to avoid the jumping progress
job_states = {}

# Minimal layout
app.layout = dbc.Container([
    html.H1("Data Science UI Test"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Actions"),
                dbc.CardBody([
                    dbc.Button("Run Correlation Analysis", id="run-correlation", color="primary", className="mb-2", style={"width": "100%"}),
                    dbc.Button("Run Bootstrap Analysis", id="run-bootstrap", color="secondary", style={"width": "100%"}),
                    html.Hr(),
                    html.Div(id="job-info")
                ])
            ])
        ], width=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Progress"),
                dbc.CardBody([
                    html.Div(id="progress-text"),
                    dbc.Progress(id="progress-bar", value=0, style={"height": "30px"})
                ])
            ], className="mb-3"),
            
            dbc.Card([
                dbc.CardHeader("Visualization"),
                dbc.CardBody([
                    dcc.Graph(id="plot", style={"height": "400px"})
                ])
            ])
        ], width=8)
    ]),
    
    # Update interval
    dcc.Interval(id="interval", interval=100),
    
    # Store current job
    dcc.Store(id="current-job")
])

def run_correlation_analysis(job_id: str):
    """Simulated correlation analysis"""
    # Send progress
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 0, "message": "Starting correlation analysis..."}
    ))
    time.sleep(1)
    
    # Generate data
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 30, "message": "Generating data..."}
    ))
    time.sleep(1)
    
    n_points = 1000
    x = np.random.randn(n_points)
    y = 2 * x + np.random.randn(n_points) * 0.5
    
    # Compute correlation
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 60, "message": "Computing correlation..."}
    ))
    time.sleep(1)
    
    correlation = np.corrcoef(x, y)[0, 1]
    
    # Create plot
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 90, "message": "Creating visualization..."}
    ))
    
    plot_data = {
        "x": x[:100].tolist(),  # Limit for performance
        "y": y[:100].tolist(),
        "title": f"Correlation Analysis (r={correlation:.3f})",
        "type": "scatter"
    }
    
    message_queue.put(Message(
        type=MessageType.PLOT,
        job_id=job_id,
        data=plot_data
    ))
    
    time.sleep(0.5)
    
    # Complete
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 100, "message": "Analysis complete!"}
    ))
    
    # Final result
    message_queue.put(Message(
        type=MessageType.RESULT,
        job_id=job_id,
        data={
            "correlation": correlation,
            "n_points": n_points,
            "interpretation": "Strong positive correlation" if correlation > 0.7 else "Moderate correlation"
        }
    ))
    
    # Update job status
    jobs[job_id].status = "complete"

def run_bootstrap_analysis(job_id: str):
    """Simulated bootstrap analysis"""
    # Send progress
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 0, "message": "Starting bootstrap analysis..."}
    ))
    time.sleep(0.5)
    
    # Generate base data
    base_data = np.random.randn(100)
    bootstrap_means = []
    n_iterations = 1000
    
    # Run bootstrap
    for i in range(n_iterations):
        if i % 100 == 0:
            progress = (i / n_iterations) * 80  # Leave 20% for final steps
            message_queue.put(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                data={"progress": progress, "message": f"Bootstrap iteration {i}/{n_iterations}"}
            ))
            time.sleep(0.1)  # Small delay to see progress
        
        # Bootstrap sample
        sample = np.random.choice(base_data, size=len(base_data), replace=True)
        bootstrap_means.append(np.mean(sample))
    
    # Create histogram
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 90, "message": "Creating visualization..."}
    ))
    
    plot_data = {
        "values": bootstrap_means,
        "title": "Bootstrap Distribution of Means",
        "type": "histogram"
    }
    
    message_queue.put(Message(
        type=MessageType.PLOT,
        job_id=job_id,
        data=plot_data
    ))
    
    time.sleep(0.5)
    
    # Complete
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 100, "message": "Bootstrap analysis complete!"}
    ))
    
    # Final result
    message_queue.put(Message(
        type=MessageType.RESULT,
        job_id=job_id,
        data={
            "mean_of_means": float(np.mean(bootstrap_means)),
            "std_of_means": float(np.std(bootstrap_means)),
            "ci_lower": float(np.percentile(bootstrap_means, 2.5)),
            "ci_upper": float(np.percentile(bootstrap_means, 97.5)),
            "n_iterations": n_iterations
        }
    ))
    
    jobs[job_id].status = "complete"

@app.callback(
    [Output("job-info", "children"),
     Output("current-job", "data")],
    [Input("run-correlation", "n_clicks"),
     Input("run-bootstrap", "n_clicks")],
    prevent_initial_call=True
)
def start_analysis(corr_clicks, boot_clicks):
    # Determine which button was clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Create job
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    tool_name = "correlation" if button_id == "run-correlation" else "bootstrap"
    
    job = Job(id=job_id, tool_name=tool_name, status="running")
    jobs[job_id] = job
    
    # Initialize job state
    job_states[job_id] = {
        "progress": 0,
        "message": "Starting...",
        "plot": None,
        "result": None
    }
    
    # Start analysis in background
    if tool_name == "correlation":
        thread = threading.Thread(target=run_correlation_analysis, args=(job_id,))
    else:
        thread = threading.Thread(target=run_bootstrap_analysis, args=(job_id,))
    
    thread.daemon = True
    thread.start()
    
    return dbc.Alert(f"Started {tool_name} analysis\nJob ID: {job_id}", color="info"), job_id

@app.callback(
    [Output("progress-text", "children"),
     Output("progress-bar", "value"),
     Output("progress-bar", "label"),
     Output("plot", "figure")],
    [Input("interval", "n_intervals")],
    [State("current-job", "data")],
    prevent_initial_call=True
)
def update_display(n, current_job):
    if not current_job or current_job not in job_states:
        return "No active job", 0, "0%", go.Figure()
    
    # Process new messages
    messages = []
    try:
        while True:
            msg = message_queue.get_nowait()
            messages.append(msg)
    except queue.Empty:
        pass
    
    # Update state for current job only
    state = job_states[current_job]
    plot_updated = False
    
    for msg in messages:
        if msg.job_id != current_job:
            continue  # Ignore messages from other jobs
            
        if msg.type == MessageType.PROGRESS:
            state["progress"] = msg.data["progress"]
            state["message"] = msg.data["message"]
        
        elif msg.type == MessageType.PLOT:
            state["plot"] = msg.data
            plot_updated = True
        
        elif msg.type == MessageType.RESULT:
            result_text = "Analysis Complete!\n\n"
            for key, value in msg.data.items():
                if isinstance(value, float):
                    result_text += f"{key}: {value:.4f}\n"
                else:
                    result_text += f"{key}: {value}\n"
            state["message"] = result_text
    
    # Create plot if updated
    fig = go.Figure()
    if plot_updated and state["plot"]:
        plot_data = state["plot"]
        
        if plot_data.get("type") == "scatter":
            fig.add_trace(go.Scatter(
                x=plot_data["x"],
                y=plot_data["y"],
                mode='markers',
                marker=dict(size=8, opacity=0.6)
            ))
            fig.update_layout(
                title=plot_data["title"],
                xaxis_title="X",
                yaxis_title="Y"
            )
        
        elif plot_data.get("type") == "histogram":
            fig.add_trace(go.Histogram(
                x=plot_data["values"],
                nbinsx=30
            ))
            fig.update_layout(
                title=plot_data["title"],
                xaxis_title="Value",
                yaxis_title="Frequency"
            )
    elif state["plot"]:
        # Return existing plot
        plot_data = state["plot"]
        
        if plot_data.get("type") == "scatter":
            fig.add_trace(go.Scatter(
                x=plot_data["x"],
                y=plot_data["y"],
                mode='markers',
                marker=dict(size=8, opacity=0.6)
            ))
            fig.update_layout(
                title=plot_data["title"],
                xaxis_title="X",
                yaxis_title="Y"
            )
        
        elif plot_data.get("type") == "histogram":
            fig.add_trace(go.Histogram(
                x=plot_data["values"],
                nbinsx=30
            ))
            fig.update_layout(
                title=plot_data["title"],
                xaxis_title="Value",
                yaxis_title="Frequency"
            )
    
    return (
        state["message"], 
        state["progress"], 
        f"{int(state['progress'])}%",
        fig
    )

if __name__ == "__main__":
    print("Starting test app...")
    print("1. Click 'Run Correlation Analysis' or 'Run Bootstrap Analysis'")
    print("2. Watch the progress bar")
    print("3. See the plot appear")
    app.run(debug=True)