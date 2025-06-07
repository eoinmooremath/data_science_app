"""
Plot Editor Tool - Modify existing plots in place
"""
from typing import Dict, Any, Optional, List
import plotly.graph_objects as go
from pydantic import Field

from tools.base import BaseTool
from core.models import ToolInput
from core.plot_manager import global_plot_manager


class EditPlotInput(ToolInput):
    plot_id: str = Field(description="ID of the plot to edit. Use 'latest' for the most recent plot.")
    
    # Marker properties
    marker_size: Optional[float] = Field(default=None, description="Set uniform marker size for all points (e.g., 10, 15, 20)")
    marker_symbol: Optional[str] = Field(default=None, description="Set uniform marker symbol for all points (e.g., 'circle', 'square', 'diamond', 'triangle-up')")
    marker_color: Optional[str] = Field(default=None, description="Set uniform marker color for all points (e.g., 'red', 'blue', '#FF5733')")
    marker_opacity: Optional[float] = Field(default=None, description="Set marker opacity (0.0 to 1.0)")
    
    # Line properties (for line plots)
    line_width: Optional[float] = Field(default=None, description="Set line width for line plots")
    line_color: Optional[str] = Field(default=None, description="Set line color for line plots")
    line_dash: Optional[str] = Field(default=None, description="Set line dash style ('solid', 'dash', 'dot', 'dashdot')")
    
    # Layout properties
    title: Optional[str] = Field(default=None, description="Update the plot title")
    x_axis_title: Optional[str] = Field(default=None, description="Update the x-axis title")
    y_axis_title: Optional[str] = Field(default=None, description="Update the y-axis title")
    
    # Color scale properties
    color_scale: Optional[str] = Field(default=None, description="Change color scale for heatmaps/continuous color plots (e.g., 'viridis', 'plasma', 'blues')")
    
    # Advanced properties
    show_legend: Optional[bool] = Field(default=None, description="Show or hide the legend")
    grid: Optional[bool] = Field(default=None, description="Show or hide grid lines")


class EditPlotTool(BaseTool):
    name = "edit_plot"
    description = "Edit properties of an existing plot (markers, colors, titles, etc.) without recreating it"
    input_model = EditPlotInput

    def execute(self, job_id: str, inputs: EditPlotInput) -> Dict[str, Any]:
        """Edit an existing plot in place"""
        
        self.update_progress(job_id, 0, "Initializing plot editor...")
        
        # Check if plot manager is available
        if not global_plot_manager.is_available():
            return {"error": "Plot manager not available"}
        
        # Get the plot to edit
        plot_id = inputs.plot_id
        if plot_id == "latest":
            figure, plot_info = global_plot_manager.get_latest_plot()
            if figure is None:
                return {"error": "No plots available to edit"}
            actual_plot_id = plot_info["id"]
        else:
            figure, plot_info = global_plot_manager.get_plot_by_id(plot_id)
            if figure is None:
                return {"error": f"Plot with ID '{plot_id}' not found"}
            actual_plot_id = plot_id
        
        self.update_progress(job_id, 20, f"Found plot: {plot_info['title']}")
        
        # Create a copy of the figure to modify
        modified_figure = go.Figure(figure)
        changes_made = []
        
        self.update_progress(job_id, 40, "Analyzing current plot properties...")
        
        # Get current plot information for context
        current_info = self._analyze_plot(modified_figure)
        
        self.update_progress(job_id, 60, "Applying modifications...")
        
        # Apply marker modifications
        if inputs.marker_size is not None:
            modified_figure.update_traces(marker_size=inputs.marker_size)
            changes_made.append(f"marker size → {inputs.marker_size}")
        
        if inputs.marker_symbol is not None:
            modified_figure.update_traces(marker_symbol=inputs.marker_symbol)
            changes_made.append(f"marker symbol → {inputs.marker_symbol}")
        
        if inputs.marker_color is not None:
            modified_figure.update_traces(marker_color=inputs.marker_color)
            changes_made.append(f"marker color → {inputs.marker_color}")
        
        if inputs.marker_opacity is not None:
            modified_figure.update_traces(marker_opacity=inputs.marker_opacity)
            changes_made.append(f"marker opacity → {inputs.marker_opacity}")
        
        # Apply line modifications
        if inputs.line_width is not None:
            modified_figure.update_traces(line_width=inputs.line_width)
            changes_made.append(f"line width → {inputs.line_width}")
        
        if inputs.line_color is not None:
            modified_figure.update_traces(line_color=inputs.line_color)
            changes_made.append(f"line color → {inputs.line_color}")
        
        if inputs.line_dash is not None:
            modified_figure.update_traces(line_dash=inputs.line_dash)
            changes_made.append(f"line dash → {inputs.line_dash}")
        
        # Apply layout modifications
        layout_updates = {}
        
        if inputs.title is not None:
            layout_updates['title'] = inputs.title
            changes_made.append(f"title → '{inputs.title}'")
        
        if inputs.x_axis_title is not None:
            layout_updates['xaxis_title'] = inputs.x_axis_title
            changes_made.append(f"x-axis title → '{inputs.x_axis_title}'")
        
        if inputs.y_axis_title is not None:
            layout_updates['yaxis_title'] = inputs.y_axis_title
            changes_made.append(f"y-axis title → '{inputs.y_axis_title}'")
        
        if inputs.show_legend is not None:
            layout_updates['showlegend'] = inputs.show_legend
            changes_made.append(f"legend → {'shown' if inputs.show_legend else 'hidden'}")
        
        if inputs.grid is not None:
            layout_updates['xaxis_showgrid'] = inputs.grid
            layout_updates['yaxis_showgrid'] = inputs.grid
            changes_made.append(f"grid → {'shown' if inputs.grid else 'hidden'}")
        
        if layout_updates:
            modified_figure.update_layout(**layout_updates)
        
        # Apply color scale modifications
        if inputs.color_scale is not None:
            modified_figure.update_traces(colorscale=inputs.color_scale)
            changes_made.append(f"color scale → {inputs.color_scale}")
        
        self.update_progress(job_id, 80, "Updating plot...")
        
        # Update the plot in the manager
        success = global_plot_manager.update_existing_plot(actual_plot_id, modified_figure)
        
        if not success:
            return {"error": f"Failed to update plot {actual_plot_id}"}
        
        self.update_progress(job_id, 100, "Plot updated successfully")
        
        return {
            "success": True,
            "message": f"Successfully updated plot '{plot_info['title']}'",
            "plot_id": actual_plot_id,
            "changes_made": changes_made,
            "current_properties": current_info
        }
    
    def _analyze_plot(self, figure: go.Figure) -> Dict[str, Any]:
        """Analyze the current plot to provide context about its properties"""
        info = {
            "plot_type": "unknown",
            "trace_count": len(figure.data),
            "traces": []
        }
        
        for i, trace in enumerate(figure.data):
            trace_info = {
                "index": i,
                "type": trace.type,
                "name": getattr(trace, 'name', f"Trace {i}"),
            }
            
            # Analyze marker properties if present
            if hasattr(trace, 'marker') and trace.marker:
                marker_info = {}
                if hasattr(trace.marker, 'size'):
                    marker_info['size'] = trace.marker.size
                if hasattr(trace.marker, 'symbol'):
                    marker_info['symbol'] = trace.marker.symbol
                if hasattr(trace.marker, 'color'):
                    marker_info['color'] = trace.marker.color
                if hasattr(trace.marker, 'opacity'):
                    marker_info['opacity'] = trace.marker.opacity
                
                if marker_info:
                    trace_info['marker'] = marker_info
            
            # Analyze line properties if present
            if hasattr(trace, 'line') and trace.line:
                line_info = {}
                if hasattr(trace.line, 'width'):
                    line_info['width'] = trace.line.width
                if hasattr(trace.line, 'color'):
                    line_info['color'] = trace.line.color
                if hasattr(trace.line, 'dash'):
                    line_info['dash'] = trace.line.dash
                
                if line_info:
                    trace_info['line'] = line_info
            
            info["traces"].append(trace_info)
        
        # Analyze layout
        layout_info = {}
        if figure.layout.title:
            layout_info['title'] = figure.layout.title.text if hasattr(figure.layout.title, 'text') else str(figure.layout.title)
        if figure.layout.xaxis and figure.layout.xaxis.title:
            layout_info['x_axis_title'] = figure.layout.xaxis.title.text if hasattr(figure.layout.xaxis.title, 'text') else str(figure.layout.xaxis.title)
        if figure.layout.yaxis and figure.layout.yaxis.title:
            layout_info['y_axis_title'] = figure.layout.yaxis.title.text if hasattr(figure.layout.yaxis.title, 'text') else str(figure.layout.yaxis.title)
        
        info["layout"] = layout_info
        
        return info 