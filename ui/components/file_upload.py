import dash_bootstrap_components as dbc
from dash import dcc, html
import base64
import io
import pandas as pd
from typing import Optional, Tuple, Any

def create_file_upload_component(upload_id: str = "file"):
    """Create file upload component"""
    return dbc.Card([
        dbc.CardHeader("Data Upload"),
        dbc.CardBody([
            dcc.Upload(
                id=f"{upload_id}-upload",
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files'),
                    ' (CSV, Excel)'
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id=f"{upload_id}-output", className="mt-2")
        ])
    ])

def parse_uploaded_file(contents: str, filename: str) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Parse uploaded file and return DataFrame and error message"""
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, "Unsupported file type. Please upload CSV or Excel files."
        
        return df, None
    
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

def render_file_info(df: Optional[pd.DataFrame], filename: str = None) -> html.Div:
    """Render information about uploaded file"""
    if df is None:
        return html.Div()
    
    return html.Div([
        dbc.Alert(f"Successfully loaded: {filename}", color="success", dismissable=True),
        html.P(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns"),
        html.P("Columns: " + ", ".join(df.columns[:5]) + ("..." if len(df.columns) > 5 else "")),
        html.P("Data types: " + ", ".join([f"{col}({dtype})" for col, dtype in df.dtypes.items()][:3]) + "...")
    ])