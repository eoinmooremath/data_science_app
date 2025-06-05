import dash
from dash import dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import os
from datetime import datetime
import base64
import io

# Core imports
from core.message_bus import MessageBus
from core.job_manager import JobManager
from core.models import Message, MessageType

# Tool imports
from tools.statistics import CorrelationTool, BootstrapTool
from tools.data_tools import GetDataInfoTool, AnalyzeUploadedDataTool, uploaded_datasets

# LLM imports
from llm.client import LLMClient

# UI imports
from ui.state import UIStateManager
from ui.components.chat import create_chat_component, render_chat_messages
from ui.components.progress import create_progress_component, render_progress
from ui.components.plots import create_plot_component, render_plot
from ui.components.results_ledger import (
    create_results_ledger_component, 
    render_results_ledger,
    export_results_to_csv,
    export_results_to_latex
)
from ui.components.file_upload import (
    create_file_upload_component,
    parse_uploaded_file,
    render_file_info
)
from ui.components.plot_tabs import (
    create_plot_tabs_component,
    render_plot_tabs,
    PlotHistoryManager
)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize core components
message_bus = MessageBus()
message_bus.start()
job_manager = JobManager(message_bus)

# Initialize tools
tools = [
    CorrelationTool(job_manager, message_bus),
    BootstrapTool(job_manager, message_bus),
    GetDataInfoTool(job_manager, message_bus),
    AnalyzeUploadedDataTool(job_manager, message_bus)
]

# Initialize LLM client
llm_client = LLMClient(job_manager, tools) if os.getenv("ANTHROPIC_API_KEY") else None

# Initialize UI state
ui_state = UIStateManager()
plot_history = PlotHistoryManager()

# Store for uploaded data
uploaded_data = {}

# Subscribe to messages to update UI state
def handle_progress_message(msg: Message):
    print(f"Progress update: Job {msg.job_id} - {msg.data['progress']}%")
    ui_state.update_job_progress(msg.job_id, msg.data["progress"], msg.data["message"])

def handle_plot_message(msg: Message):
    print(f"Plot received: Job {msg.job_id} - Type: {msg.data.get('type')}")
    ui_state.update_job_plot(msg.job_id, msg.data)
    plot_history.add_plot(msg.job_id, msg.data)

def handle_result_message(msg: Message):
    print(f"Result received: Job {msg.job_id}")
    ui_state.update_job_result(msg.job_id, msg.data)
    
    # Add to results ledger
    job = job_manager.get_job(msg.job_id)
    if job:
        ui_state.add_result(msg.job_id, job.tool_name, msg.data)

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
        # Left column - Chat and File Upload
        dbc.Col([
            create_chat_component("main-chat"),
            html.Div(className="mb-3"),  # Spacer
            create_file_upload_component("main-file")
        ], width=4),
        
        # Middle column - Progress and Results Ledger
        dbc.Col([
            create_progress_component("main-progress"),
            html.Div(className="mb-3"),  # Spacer
            create_results_ledger_component("main-results")
        ], width=4),
        
        # Right column - Plot Tabs
        dbc.Col([
            create_plot_tabs_component("main-plots")
        ], width=4)
    ]),
    
    # Hidden components
    dcc.Interval(id="update-interval", interval=100),
    dcc.Store(id="current-job-store"),
    dcc.Store(id="message-trigger", data=0),
    dcc.Store(id="active-tab-store", data="tab-0"),
    dcc.Download(id="download-results")
])

# Chat callback
@app.callback(
    [Output("main-chat-history", "children"),
     Output("main-chat-input", "value"),
     Output("current-job-store", "data"),
     Output("message-trigger", "data")],
    [Input("main-chat-send", "n_clicks"),
     Input("main-chat-input", "n_submit")],
    [State("main-chat-input", "value"),
     State("message-trigger", "data")],
    prevent_initial_call=True
)
def handle_chat(n_clicks, n_submit, user_input, trigger):
    if not user_input:
        return dash.no_update
    
    # Add user message
    ui_state.add_chat_message("user", user_input)
    
    # Check if user is referencing uploaded data
    if uploaded_data and any(ref in user_input.lower() for ref in ["uploaded", "data", "file"]):
        # Add context about uploaded data
        data_info = f"[User has uploaded data with {uploaded_data.get('shape', 'unknown')} shape]"
        user_input = f"{user_input} {data_info}"
    
    # Process with LLM
    if llm_client:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in ui_state.chat_messages
        ]
        
        response = llm_client.process_message(messages)
        
        if response["type"] == "tool_use":
            ui_state.add_chat_message(
                "assistant",
                response["message"],
                response["job_id"]
            )
            ui_state.create_job_state(response["job_id"])
            current_job = response["job_id"]
        else:
            ui_state.add_chat_message("assistant", response["message"])
            current_job = ui_state.current_job_id
    else:
        ui_state.add_chat_message(
            "assistant",
            "No LLM client available. Please set ANTHROPIC_API_KEY."
        )
        current_job = None
    
    chat_elements = render_chat_messages(ui_state.chat_messages)
    
    return chat_elements, "", current_job, trigger + 1

# File upload callback
@app.callback(
    Output("main-file-output", "children"),
    Input("main-file-upload", "contents"),
    State("main-file-upload", "filename"),
    prevent_initial_call=True
)
def handle_file_upload(contents, filename):
    if contents is None:
        return html.Div()
    
    df, error = parse_uploaded_file(contents, filename)
    
    if error:
        return dbc.Alert(error, color="danger", dismissable=True)
    
    # Store for UI
    uploaded_data['df'] = df
    uploaded_data['filename'] = filename
    uploaded_data['shape'] = df.shape
    
    # Store for tools to access
    dataset_name = filename.split('.')[0]  # Remove extension
    uploaded_datasets['uploaded'] = df
    uploaded_datasets[dataset_name] = df
    
    return render_file_info(df, filename)


# Progress and results update callback
@app.callback(
    [Output("main-progress-job-info", "children"),
     Output("main-progress-text", "children"),
     Output("main-progress-bar", "value"),
     Output("main-progress-bar", "label"),
     Output("main-results-content", "children")],
    [Input("update-interval", "n_intervals")],
    [State("current-job-store", "data")],
    prevent_initial_call=True
)
def update_progress_and_results(n_intervals, current_job_id):
    # Progress update
    if not current_job_id or current_job_id not in ui_state.job_states:
        job_info, message, progress, label = render_progress(None, 0, "No active job")
    else:
        job_state = ui_state.job_states[current_job_id]
        job_info, message, progress, label = render_progress(
            current_job_id,
            job_state.progress,
            job_state.message
        )
    
    # Results ledger
    results_content = render_results_ledger(ui_state.results)
    
    return job_info, message, progress, label, results_content

# Plot tabs callback
@app.callback(
    [Output("main-plots-tabs", "children"),
     Output("main-plots-content", "children"),
     Output("main-plots-tabs", "active_tab")],
    [Input("update-interval", "n_intervals"),
     Input("main-plots-tabs", "active_tab")],
    [State("active-tab-store", "data")],
    prevent_initial_call=True
)
def update_plot_tabs(n_intervals, active_tab, stored_active_tab):
    tabs, _ = render_plot_tabs(plot_history.plot_history)
    
    # Determine which tab to show
    if active_tab is None and plot_history.plot_history:
        # Show the latest plot
        active_tab = f"tab-{len(plot_history.plot_history) - 1}"
    elif active_tab is None:
        active_tab = "tab-0"
    
    # Get the plot for the active tab
    if active_tab == "tab-0" or not plot_history.plot_history:
        content = html.Div(
            "Run analyses to see visualizations here",
            className="text-muted text-center p-4"
        )
    else:
        tab_index = int(active_tab.split("-")[1])
        plot_info = plot_history.get_plot(tab_index)
        if plot_info:
            fig = render_plot(plot_info.get("plot_data"))
            content = dcc.Graph(figure=fig, style={"height": "500px"})
        else:
            content = html.Div("Plot not found")
    
    return tabs, content, active_tab

# Export results callback
@app.callback(
    Output("download-results", "data"),
    Input("main-results-export-btn", "n_clicks"),
    prevent_initial_call=True
)
def export_results(n_clicks):
    if not ui_state.results:
        return dash.no_update
    
    # For now, export as CSV. Could add a dropdown to choose format
    csv_string = export_results_to_csv(ui_state.results)
    
    return dict(
        content=csv_string,
        filename=f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

if __name__ == "__main__":
    if not llm_client:
        print("⚠️  No ANTHROPIC_API_KEY found. Running in demo mode.")
        print("   Set the environment variable to enable Claude integration.")
    else:
        print("✓ LLM client initialized")
    
    print("✓ Starting Data Science Assistant UI...")
    print("\nNew features:")
    print("  - Results Ledger: See all numerical results in one place")
    print("  - File Upload: Drag and drop CSV/Excel files")
    print("  - Plot Tabs: Each visualization in its own tab")
    print("  - Export: Download results as CSV")
    print("\nTry:")
    print("  1. Upload a CSV file")
    print("  2. Ask 'Can you analyze the correlation in my uploaded data?'")
    print("  3. Run multiple analyses to see tabs and results accumulate")
    
    app.run(debug=True)