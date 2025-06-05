import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import os
from datetime import datetime

# Core imports
from core.message_bus import MessageBus
from core.job_manager import JobManager
from core.models import Message, MessageType

# Tool imports
from tools.statistics import CorrelationTool, BootstrapTool

# LLM imports
from llm.client import LLMClient

# UI imports
from ui.state import UIStateManager
from ui.components.chat import create_chat_component, render_chat_messages
from ui.components.progress import create_progress_component, render_progress
from ui.components.plots import create_plot_component, render_plot

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize core components
message_bus = MessageBus()
message_bus.start()
job_manager = JobManager(message_bus)

# Initialize tools
tools = [
    CorrelationTool(job_manager, message_bus),
    BootstrapTool(job_manager, message_bus)
]

# Initialize LLM client
llm_client = LLMClient(job_manager, tools) if os.getenv("ANTHROPIC_API_KEY") else None

# Initialize UI state
ui_state = UIStateManager()

# Subscribe to messages to update UI state
def handle_progress_message(msg: Message):
    print(f"Progress update: Job {msg.job_id} - {msg.data['progress']}%")
    ui_state.update_job_progress(msg.job_id, msg.data["progress"], msg.data["message"])

def handle_plot_message(msg: Message):
    print(f"Plot received: Job {msg.job_id} - Type: {msg.data.get('type')}")
    ui_state.update_job_plot(msg.job_id, msg.data)

def handle_result_message(msg: Message):
    print(f"Result received: Job {msg.job_id}")
    ui_state.update_job_result(msg.job_id, msg.data)

message_bus.subscribe(MessageType.PROGRESS, handle_progress_message)
message_bus.subscribe(MessageType.PLOT, handle_plot_message)
message_bus.subscribe(MessageType.RESULT, handle_result_message)

# Create layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Science Assistant", className="mb-4")
        ])
    ]),
    
    dbc.Row([
        # Left side - Chat
        dbc.Col([
            create_chat_component("main-chat")
        ], width=5),
        
        # Right side - Results
        dbc.Col([
            create_progress_component("main-progress"),
            html.Div(className="mb-3"),  # Spacer
            create_plot_component("main-plot")
        ], width=7)
    ]),
    
    # Hidden components
    dcc.Interval(id="update-interval", interval=100),
    dcc.Store(id="current-job-store"),
    dcc.Store(id="message-trigger", data=0)
])

# Chat callback
@app.callback(
    [Output("main-chat-history", "children"),
     Output("main-chat-input", "value"),
     Output("current-job-store", "data"),
     Output("message-trigger", "data")],
    [Input("main-chat-send", "n_submit"),
     Input("main-chat-input", "n_submit")],
    [State("main-chat-input", "value"),
     State("message-trigger", "data")],
    prevent_initial_call=True
)
def handle_chat(n_clicks, key_event, user_input, trigger):

    if not user_input:
        return dash.no_update
    
    # Add user message
    ui_state.add_chat_message("user", user_input)
    
    # Process with LLM
    if llm_client:
        # Convert chat messages to LLM format
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in ui_state.chat_messages
        ]
        
        response = llm_client.process_message(messages)
        
        if response["type"] == "tool_use":
            # Tool execution started
            ui_state.add_chat_message(
                "assistant",
                response["message"],
                response["job_id"]
            )
            ui_state.create_job_state(response["job_id"])
            current_job = response["job_id"]
        else:
            # Regular message
            ui_state.add_chat_message("assistant", response["message"])
            current_job = ui_state.current_job_id
    else:
        ui_state.add_chat_message(
            "assistant",
            "No LLM client available. Please set ANTHROPIC_API_KEY."
        )
        current_job = None
    
    # Render chat
    chat_elements = render_chat_messages(ui_state.chat_messages)
    
    return chat_elements, "", current_job, trigger + 1

# Progress and plot update callback
@app.callback(
    [Output("main-progress-job-info", "children"),
     Output("main-progress-text", "children"),
     Output("main-progress-bar", "value"),
     Output("main-progress-bar", "label"),
     Output("main-plot-display", "figure")],
    [Input("update-interval", "n_intervals")],
    [State("current-job-store", "data")],
    prevent_initial_call=True
)
def update_display(n_intervals, current_job_id):
    if not current_job_id or current_job_id not in ui_state.job_states:
        # Return all 5 outputs when no job
        job_info, message, progress, label = render_progress(None, 0, "No active job")
        fig = render_plot(None)
        return job_info, message, progress, label, fig
    
    # Get current job state
    job_state = ui_state.job_states[current_job_id]
    
    # Render progress (returns 4 items)
    job_info, message, progress, label = render_progress(
        current_job_id,
        job_state.progress,
        job_state.message
    )
    
    # Render plot (returns 1 item)
    fig = render_plot(job_state.plot_data)
    
    # Return all 5 outputs
    return job_info, message, progress, label, fig
if __name__ == "__main__":
    if not llm_client:
        print("⚠️  No ANTHROPIC_API_KEY found. Running in demo mode.")
        print("   Set the environment variable to enable Claude integration.")
    else:
        print("✓ LLM client initialized")
    
    print("✓ Starting Data Science Assistant UI...")
    print("\nTry asking:")
    print("  - 'Can you analyze the correlation between two variables?'")
    print("  - 'Run a bootstrap analysis with 2000 iterations'")
    
    app.run(debug=True)