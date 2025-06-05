from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
from ui.state import UIStateManager
from ui.components.results_ledger import render_results_ledger, export_results_to_csv

def register_results_callbacks(app, ui_state: UIStateManager):
    """Register results ledger callbacks"""
    
    @app.callback(
        Output("main-results-content", "children"),
        [Input("update-interval", "n_intervals")],
        prevent_initial_call=True
    )
    def update_results_display(n_intervals):
        """Update results ledger display"""
        return render_results_ledger(ui_state.results)
    
    @app.callback(
        Output("download-results", "data"),
        Input("main-results-export-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def export_results(n_clicks):
        """Export results to CSV"""
        if not ui_state.results:
            raise PreventUpdate
        
        csv_string = export_results_to_csv(ui_state.results)
        
        return dict(
            content=csv_string,
            filename=f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )