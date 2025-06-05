from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from ui.state import UIStateManager
from ui.components.progress import render_progress

def register_progress_callbacks(app, ui_state: UIStateManager):
    """Register progress-related callbacks"""
    
    @app.callback(
        [Output("main-progress-job-info", "children"),
         Output("main-progress-text", "children"),
         Output("main-progress-bar", "value"),
         Output("main-progress-bar", "label")],
        [Input("update-interval", "n_intervals")],
        [State("current-job-store", "data")],
        prevent_initial_call=True
    )
    def update_progress_display(n_intervals, current_job_id):
        if not current_job_id or current_job_id not in ui_state.job_states:
            return render_progress(None, 0, "No active job")
        
        job_state = ui_state.job_states[current_job_id]
        return render_progress(
            current_job_id,
            job_state.progress,
            job_state.message
        )