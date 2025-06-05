# ui/callbacks/file_callbacks.py
from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from ui.components.file_upload import parse_uploaded_file, render_file_info
from tools.data_tools import uploaded_datasets

def register_file_callbacks(app):
    """Register file upload callbacks"""
    
    @app.callback(
        Output("main-file-output", "children"),
        Input("main-file-upload", "contents"),
        State("main-file-upload", "filename"),
        prevent_initial_call=True
    )
    def handle_file_upload(contents, filename):
        if contents is None:
            raise PreventUpdate
        
        df, error = parse_uploaded_file(contents, filename)
        
        if error:
            return dbc.Alert(error, color="danger", dismissable=True)
        
        # Store for tools to access
        dataset_name = filename.split('.')[0]  # Remove extension
        uploaded_datasets['uploaded'] = df
        uploaded_datasets[dataset_name] = df
        
        return render_file_info(df, filename)