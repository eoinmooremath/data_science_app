# test_claude_integrated.py
import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import threading
import queue
import time
import numpy as np
from datetime import datetime
import uuid
import json
import os
from anthropic import Anthropic

# Import from your models file
from models import Message, Job, MessageType

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize Anthropic client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Simple message queue
message_queue = queue.Queue()
jobs = {}
job_states = {}

# Layout with chat interface
app.layout = dbc.Container([
    html.H1("Data Science Assistant"),
    
    dbc.Row([
        # Left side - Chat
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Chat with Claude"),
                dbc.CardBody([
                    html.Div(
                        id="chat-history",
                        style={
                            "height": "400px",
                            "overflowY": "scroll",
                            "border": "1px solid #ddd",
                            "padding": "10px",
                            "borderRadius": "5px",
                            "marginBottom": "10px"
                        }
                    ),
                    dbc.InputGroup([
                        dbc.Input(
                            id="user-input",
                            placeholder="Ask me to analyze data...",
                            type="text"
                        ),
                        dbc.Button("Send", id="send-btn", color="primary")
                    ])
                ])
            ])
        ], width=5),
        
        # Right side - Results
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Analysis Progress"),
                dbc.CardBody([
                    html.Div(id="current-job-info", className="mb-2"),
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
        ], width=7)
    ]),
    
    # Hidden components
    dcc.Interval(id="interval", interval=100),
    dcc.Store(id="current-job"),
    dcc.Store(id="chat-messages", data=[])
])

# Tool execution functions (same as before)
def run_correlation_analysis(job_id: str, n_points: int = 1000):
    """Simulated correlation analysis"""
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 0, "message": "Starting correlation analysis..."}
    ))
    time.sleep(1)
    
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 30, "message": "Generating data..."}
    ))
    time.sleep(1)
    
    x = np.random.randn(n_points)
    y = 2 * x + np.random.randn(n_points) * 0.5
    
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 60, "message": "Computing correlation..."}
    ))
    time.sleep(1)
    
    correlation = np.corrcoef(x, y)[0, 1]
    
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 90, "message": "Creating visualization..."}
    ))
    
    plot_data = {
        "x": x[:100].tolist(),
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
    
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 100, "message": "Analysis complete!"}
    ))
    
    # Store result for Claude
    result = {
        "correlation": float(correlation),
        "n_points": n_points,
        "interpretation": "Strong positive correlation" if correlation > 0.7 else "Moderate correlation"
    }
    
    message_queue.put(Message(
        type=MessageType.RESULT,
        job_id=job_id,
        data=result
    ))
    
    jobs[job_id].status = "complete"
    jobs[job_id].result = result

def run_bootstrap_analysis(job_id: str, n_iterations: int = 1000):
    """Simulated bootstrap analysis"""
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 0, "message": "Starting bootstrap analysis..."}
    ))
    time.sleep(0.5)
    
    base_data = np.random.randn(100)
    bootstrap_means = []
    
    for i in range(n_iterations):
        if i % 100 == 0:
            progress = (i / n_iterations) * 80
            message_queue.put(Message(
                type=MessageType.PROGRESS,
                job_id=job_id,
                data={"progress": progress, "message": f"Bootstrap iteration {i}/{n_iterations}"}
            ))
            time.sleep(0.1)
        
        sample = np.random.choice(base_data, size=len(base_data), replace=True)
        bootstrap_means.append(np.mean(sample))
    
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
    
    message_queue.put(Message(
        type=MessageType.PROGRESS,
        job_id=job_id,
        data={"progress": 100, "message": "Bootstrap analysis complete!"}
    ))
    
    result = {
        "mean_of_means": float(np.mean(bootstrap_means)),
        "std_of_means": float(np.std(bootstrap_means)),
        "ci_lower": float(np.percentile(bootstrap_means, 2.5)),
        "ci_upper": float(np.percentile(bootstrap_means, 97.5)),
        "n_iterations": n_iterations
    }
    
    message_queue.put(Message(
        type=MessageType.RESULT,
        job_id=job_id,
        data=result
    ))
    
    jobs[job_id].status = "complete"
    jobs[job_id].result = result

def call_claude_with_tools(messages):
    """Call Claude with tool definitions"""
    tools = [
        {
            "name": "analyze_correlation",
            "description": "Analyze correlation between two variables with visualization",
            "input_schema": {
                "type": "object",
                "properties": {
                    "n_points": {
                        "type": "integer",
                        "description": "Number of data points to generate",
                        "default": 1000
                    }
                },
                "required": []
            }
        },
        {
            "name": "bootstrap_analysis",
            "description": "Perform bootstrap analysis to estimate sampling distribution",
            "input_schema": {
                "type": "object",
                "properties": {
                    "n_iterations": {
                        "type": "integer",
                        "description": "Number of bootstrap iterations",
                        "default": 1000
                    }
                },
                "required": []
            }
        }
    ]
    
    try:
        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0,
            messages=messages,
            tools=tools
        )
        return response
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return None

@app.callback(
    [Output("chat-history", "children"),
     Output("chat-messages", "data"),
     Output("user-input", "value"),
     Output("current-job", "data"),
     Output("current-job-info", "children")],
    [Input("send-btn", "n_clicks"),
     Input("user-input", "n_keydown")],
    [State("user-input", "value"),
     State("chat-messages", "data")],
    prevent_initial_call=True
)
def handle_chat(n_clicks, key_event, user_input, messages):
    # Check if Enter was pressed
    if ctx.triggered_id == "user-input" and key_event and key_event["key"] != "Enter":
        return dash.no_update
    
    if not user_input:
        return dash.no_update
    
    # Add user message
    messages.append({"role": "user", "content": user_input})
    
    # Call Claude
    response = call_claude_with_tools(messages)
    
    current_job_id = None
    job_info = None
    
    if response:
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            tool_use = next((block for block in response.content if hasattr(block, 'name')), None)
            
            if tool_use:
                # Create job
                job_id = f"job_{uuid.uuid4().hex[:8]}"
                current_job_id = job_id
                
                job = Job(id=job_id, tool_name=tool_use.name, status="running")
                jobs[job_id] = job
                
                # Initialize job state
                job_states[job_id] = {
                    "progress": 0,
                    "message": "Starting...",
                    "plot": None,
                    "result": None
                }
                
                # Execute tool
                if tool_use.name == "analyze_correlation":
                    n_points = tool_use.input.get("n_points", 1000)
                    thread = threading.Thread(
                        target=run_correlation_analysis,
                        args=(job_id, n_points)
                    )
                elif tool_use.name == "bootstrap_analysis":
                    n_iterations = tool_use.input.get("n_iterations", 1000)
                    thread = threading.Thread(
                        target=run_bootstrap_analysis,
                        args=(job_id, n_iterations)
                    )
                
                thread.daemon = True
                thread.start()
                
                # Add assistant message about starting the tool
                assistant_msg = f"I'll {tool_use.name.replace('_', ' ')} for you. Starting the analysis now..."
                messages.append({"role": "assistant", "content": assistant_msg})
                
                job_info = dbc.Alert(
                    f"Running: {tool_use.name}\nJob ID: {job_id}",
                    color="info"
                )
        else:
            # Regular response
            assistant_msg = response.content[0].text
            messages.append({"role": "assistant", "content": assistant_msg})
    else:
        messages.append({"role": "assistant", "content": "Sorry, I encountered an error. Please try again."})
    
    # Build chat display
    chat_display = []
    for msg in messages:
        if msg["role"] == "user":
            chat_display.append(
                html.Div([
                    html.Strong("You: "),
                    html.Span(msg["content"])
                ], style={"marginBottom": "10px", "padding": "10px", "backgroundColor": "#e3f2fd", "borderRadius": "5px"})
            )
        else:
            chat_display.append(
                html.Div([
                    html.Strong("Claude: "),
                    html.Span(msg["content"])
                ], style={"marginBottom": "10px", "padding": "10px", "backgroundColor": "#f5f5f5", "borderRadius": "5px"})
            )
    
    return chat_display, messages, "", current_job_id, job_info

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
            continue
            
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
    
    # Create plot
    fig = go.Figure()
    if state["plot"]:
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
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable")
        print("Example: export ANTHROPIC_API_KEY='your-key-here'")
    else:
        print("Starting Data Science Assistant...")
        print("Try asking: 'Can you analyze the correlation between two variables?'")
        print("Or: 'Please run a bootstrap analysis'")
        app.run(debug=True)