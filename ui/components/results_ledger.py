import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime

def create_results_ledger_component(ledger_id: str = "results"):
    """Create the results ledger component"""
    return dbc.Card([
        dbc.CardHeader([
            "Results Summary",
            dbc.Button(
                "Export",
                id=f"{ledger_id}-export-btn",
                color="secondary",
                size="sm",
                className="float-end"
            )
        ]),
        dbc.CardBody([
            html.Div(id=f"{ledger_id}-content", style={"maxHeight": "400px", "overflowY": "auto"})
        ])
    ])

def render_results_ledger(results: List[Dict[str, Any]]) -> html.Div:
    """Render results in a formatted ledger"""
    if not results:
        return html.Div(
            "No results yet. Run some analyses to see results here.",
            className="text-muted text-center p-4"
        )
    
    # Group results by analysis type
    ledger_content = []
    
    for i, result in enumerate(results):
        # Create a section for each result
        timestamp = result.get("timestamp", datetime.now()).strftime("%H:%M:%S")
        tool_name = result.get("tool_name", "Unknown Analysis")
        job_id = result.get("job_id", "")
        
        # Format the result data
        result_items = []
        data = result.get("data", {})
        
        for key, value in data.items():
            if key not in ["interpretation", "job_id", "tool_name", "timestamp"]:
                if isinstance(value, float):
                    formatted_value = f"{value:.4f}"
                else:
                    formatted_value = str(value)
                
                result_items.append(
                    html.Div([
                        html.Strong(f"{key.replace('_', ' ').title()}: "),
                        html.Span(formatted_value)
                    ], className="mb-1")
                )
        
        # Add interpretation if available
        if "interpretation" in data:
            result_items.append(
                html.Div([
                    html.Em(data["interpretation"])
                ], className="mt-2 text-muted")
            )
        
        # Create result card
        ledger_content.append(
            dbc.Card([
                dbc.CardHeader([
                    html.Strong(f"[{timestamp}] {tool_name}"),
                    html.Small(f" ({job_id})", className="text-muted")
                ], className="py-2"),
                dbc.CardBody(result_items, className="py-2")
            ], className="mb-2")
        )
    
    return html.Div(ledger_content)

def export_results_to_csv(results: List[Dict[str, Any]]) -> str:
    """Export results to CSV format"""
    if not results:
        return ""
    
    # Flatten results for CSV
    rows = []
    for result in results:
        row = {
            "timestamp": result.get("timestamp", ""),
            "tool": result.get("tool_name", ""),
            "job_id": result.get("job_id", "")
        }
        # Add all data fields
        data = result.get("data", {})
        for key, value in data.items():
            if key != "interpretation":
                row[key] = value
        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df.to_csv(index=False)

def export_results_to_latex(results: List[Dict[str, Any]]) -> str:
    """Export results to LaTeX format"""
    if not results:
        return ""
    
    latex = "\\begin{table}[h]\n\\centering\n"
    latex += "\\caption{Analysis Results}\n"
    latex += "\\begin{tabular}{llr}\n"
    latex += "\\hline\n"
    latex += "Analysis & Metric & Value \\\\\n"
    latex += "\\hline\n"
    
    for result in results:
        tool_name = result.get("tool_name", "Unknown")
        data = result.get("data", {})
        
        for key, value in data.items():
            if key not in ["interpretation", "job_id", "tool_name", "timestamp"]:
                if isinstance(value, float):
                    formatted_value = f"{value:.4f}"
                else:
                    formatted_value = str(value)
                
                key_formatted = key.replace("_", " ").title()
                latex += f"{tool_name} & {key_formatted} & {formatted_value} \\\\\n"
        
        latex += "\\hline\n"
    
    latex += "\\end{tabular}\n"
    latex += "\\end{table}"
    
    return latex