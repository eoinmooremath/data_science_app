import dash_bootstrap_components as dbc
from dash import html
from typing import Optional, Tuple, Any

def create_progress_component(progress_id: str = "progress"):
    """Create the progress display component"""
    return dbc.Card([
        dbc.CardHeader("Analysis Progress"),
        dbc.CardBody([
            html.Div(id=f"{progress_id}-job-info", className="mb-2"),
            html.Div(id=f"{progress_id}-text"),
            dbc.Progress(
                id=f"{progress_id}-bar",
                value=0,
                style={"height": "30px"},
                className="mt-2"
            )
        ])
    ])

def render_progress(job_id: Optional[str], progress: float, message: str) -> Tuple[Any, str, float, str]:
    """Render progress information - returns (job_info, message, progress_value, progress_label)"""
    if not job_id:
        return html.Div("No active job"), "Waiting for analysis...", 0, "0%"
    
    job_info = dbc.Alert(f"Job ID: {job_id}", color="info", dismissable=False)
    
    return job_info, message, progress, f"{int(progress)}%"