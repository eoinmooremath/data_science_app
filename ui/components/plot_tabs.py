# ui/components/plot_tabs.py
import dash_bootstrap_components as dbc
from dash import dcc, html
from typing import Dict, List, Any, Optional
from datetime import datetime
import plotly.graph_objects as go
import uuid

class PlotHistoryManager:
    """Manages plot history with native Plotly Figure objects"""
    
    def __init__(self):
        self.plot_history = []
        self.figure_cache = {}
        print(f"🔄 PlotHistoryManager created at {datetime.now().strftime('%H:%M:%S')} - Fresh start")
    
    def add_plot(self, plot_data, job_id):
        """Add a new plot to history"""
        plot_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # Extract the figure from plot_data
        # Tools will now provide a 'figure' key with the actual Plotly Figure object
        figure = plot_data.get('figure')
        if not figure:
            print(f"⚠️ Warning: No figure found in plot_data for job {job_id}")
            figure = self._create_error_figure("No figure provided by tool")
        
        plot_info = {
            "id": plot_id,
            "timestamp": timestamp,
            "job_id": job_id,
            "plot_data": plot_data,
            "title": plot_data.get("title", f"Plot {len(self.plot_history) + 1}"),
            "last_updated": timestamp
        }
        
        self.plot_history.append(plot_info)
        self.figure_cache[plot_id] = figure
        
        print(f"📊 Added plot {plot_id} (title: {plot_info['title']}) - Total plots: {len(self.plot_history)}")
        return plot_id
    
    def get_plot_by_index(self, index):
        """Get plot info by index"""
        if 0 <= index < len(self.plot_history):
            return self.plot_history[index]
        return None
    
    def get_plot_figure(self, plot_id):
        """Get cached figure by plot ID"""
        return self.figure_cache.get(plot_id)
    
    def get_latest_plot(self):
        """Get the most recent plot info and figure"""
        if not self.plot_history:
            return None, None
        
        latest_plot = self.plot_history[-1]
        figure = self.figure_cache.get(latest_plot["id"])
        return figure, latest_plot
    
    def get_plot_by_id(self, plot_id):
        """Get plot info and figure by plot ID"""
        for plot_info in self.plot_history:
            if plot_info["id"] == plot_id:
                figure = self.figure_cache.get(plot_id)
                return figure, plot_info
        return None, None
    
    def get_all_plot_ids(self):
        """Get all available plot IDs with their titles"""
        return [(plot["id"], plot["title"]) for plot in self.plot_history]
    
    def update_existing_plot(self, plot_id: str, new_figure: go.Figure, new_title: str = None) -> bool:
        """Update an existing plot in place"""
        # Find the plot in history
        for i, plot_info in enumerate(self.plot_history):
            if plot_info["id"] == plot_id:
                # Update the figure cache
                self.figure_cache[plot_id] = new_figure
                
                # Update the plot info if new title provided
                if new_title:
                    self.plot_history[i]["title"] = new_title
                
                # Update timestamp to force UI refresh
                self.plot_history[i]["last_updated"] = datetime.now()
                
                print(f"🔄 Updated plot {plot_id} in place")
                return True
        
        print(f"⚠️ Plot {plot_id} not found for updating")
        return False
    
    def clear_all(self):
        """Clear all plots and reset"""
        old_count = len(self.plot_history)
        self.plot_history.clear()
        self.figure_cache.clear()
        print(f"🧹 Cleared {old_count} plots - Fresh start")
    
    def _create_error_figure(self, error_message: str):
        """Create a simple error figure"""
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text=f"❌ Error: {error_message}",
            showarrow=False,
            font=dict(size=14, color="red")
        )
        fig.update_layout(
            title="Plot Error",
            height=400,
            template="plotly_white",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig

def create_plot_tabs_component(tabs_id: str = "plots"):
    """Create modern tabbed plot component with native Dash graphs"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5("📊 Visualizations", className="mb-0"),
            html.Small("Interactive plots powered by Plotly", className="text-muted")
        ]),
        dbc.CardBody([
            dcc.Tabs(
                id=f"{tabs_id}-tabs",
                value="tab-empty",
                children=[dcc.Tab(label="No plots yet", value="tab-empty")],
                style={"marginBottom": "15px"}
            ),
            html.Div(
                id=f"{tabs_id}-content",
                style={"minHeight": "500px"}
            )
        ], style={"padding": "15px"})
    ], style={"height": "100%"})