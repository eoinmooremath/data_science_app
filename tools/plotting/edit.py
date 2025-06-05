# tools/plotting/edit.py
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import copy

from core.models import ToolInput
from core.plot_manager import global_plot_manager
from .base import BasePlottingTool, BasePlottingInput


class PlotEditInput(BasePlottingInput):
    """Input model for plot editing tool"""
    plot_id: str = Field(description="ID of the plot to edit (use 'latest' for most recent plot)")
    
    # Title and labels
    new_title: Optional[str] = Field(default=None, description="New plot title")
    x_axis_title: Optional[str] = Field(default=None, description="New x-axis title")
    y_axis_title: Optional[str] = Field(default=None, description="New y-axis title")
    
    # Colors and styling
    marker_color: Optional[str] = Field(default=None, description="New marker/line color (e.g., 'red', '#FF0000', 'rgb(255,0,0)')")
    marker_size: Optional[int] = Field(default=None, description="New marker size (for scatter plots)")
    line_width: Optional[int] = Field(default=None, description="New line width (for line plots)")
    opacity: Optional[float] = Field(default=None, description="New opacity (0-1)")
    
    # Color scales for continuous data
    color_scale: Optional[str] = Field(default=None, description="New color scale (e.g., 'viridis', 'plasma', 'blues')")
    
    # Layout changes
    background_color: Optional[str] = Field(default=None, description="New background color")
    grid_color: Optional[str] = Field(default=None, description="New grid color")
    show_legend: Optional[bool] = Field(default=None, description="Show or hide legend")
    
    # Axis ranges
    x_range: Optional[List[float]] = Field(default=None, description="New x-axis range [min, max]")
    y_range: Optional[List[float]] = Field(default=None, description="New y-axis range [min, max]")
    
    # Template
    new_template: Optional[str] = Field(default=None, description="New template (plotly_white, plotly_dark, ggplot2, etc.)")


class PlotEditTool(BasePlottingTool):
    """Edit existing plots by modifying colors, titles, styling, and other properties"""
    
    @property
    def name(self) -> str:
        return "plotting_edit"
    
    @property
    def description(self) -> str:
        return """Edit existing plots to change their appearance and styling.
        
        You can modify:
        - Titles and axis labels
        - Colors (markers, lines, backgrounds)
        - Marker sizes and line widths
        - Opacity and transparency
        - Color scales for continuous data
        - Axis ranges and limits
        - Templates and themes
        - Legend visibility
        - Grid colors and styling
        
        Use 'latest' as plot_id to edit the most recent plot, or specify a specific plot ID."""
    
    @property
    def input_model(self) -> type[ToolInput]:
        return PlotEditInput
    
    def get_plot_specific_parameters(self) -> List[str]:
        return [
            "plot_id", "new_title", "x_axis_title", "y_axis_title",
            "marker_color", "marker_size", "line_width", "opacity",
            "color_scale", "background_color", "grid_color", "show_legend",
            "x_range", "y_range", "new_template"
        ]
    
    def create_figure(self, df: pd.DataFrame, **params) -> go.Figure:
        """This method is not used for editing - we override execute instead"""
        pass
    
    def execute(self, job_id: str, inputs: PlotEditInput) -> Dict[str, Any]:
        """Execute the plot editing"""
        try:
            # Progress: Start
            self.update_progress(job_id, 0, "Starting plot editing...")
            
            # Get the plot to edit
            plot_id = inputs.plot_id
            original_figure, plot_info = self._get_plot_to_edit(plot_id)
            
            if original_figure is None:
                error_msg = f"Plot not found: {plot_id}"
                error_fig = self.create_error_figure(error_msg)
                self._publish_plot(job_id, error_fig, f"Error: {error_msg}")
                return {"error": error_msg}
            
            # Progress: Analyzing plot
            self.update_progress(job_id, 20, "Analyzing plot structure...")
            
            # Create a deep copy of the figure to avoid modifying the original
            edited_figure = copy.deepcopy(original_figure)
            
            # Progress: Applying edits
            self.update_progress(job_id, 40, "Applying modifications...")
            
            # Apply all the edits
            changes_made = self._apply_edits(edited_figure, inputs)
            
            # Progress: Finalizing
            self.update_progress(job_id, 80, "Finalizing edited plot...")
            
            # Create a new title for the edited plot
            original_title = plot_info.get("title", "Plot") if plot_info else "Plot"
            new_title = inputs.new_title if inputs.new_title else f"{original_title} (Edited)"
            
            # Update the figure title if a new one was provided
            if inputs.new_title:
                edited_figure.update_layout(title=inputs.new_title)
            
            # Progress: Updating existing plot
            self.update_progress(job_id, 95, "Updating existing plot...")
            
            # Update the existing plot in place instead of creating a new one
            self._update_existing_plot(plot_id, edited_figure, new_title, plot_info)
            
            # Complete
            self.update_progress(job_id, 100, "Plot editing completed!")
            
            return {
                "plot_title": new_title,
                "original_plot_id": plot_id,
                "changes_made": changes_made,
                "message": f"Successfully edited plot: {new_title}",
                "updated_in_place": True
            }
            
        except Exception as e:
            error_msg = f"Error editing plot: {str(e)}"
            error_fig = self.create_error_figure(error_msg)
            self._publish_plot(job_id, error_fig, "Plot Edit Error")
            return {"error": error_msg}
    
    def _get_plot_to_edit(self, plot_id: str) -> tuple[Optional[go.Figure], Optional[Dict]]:
        """Get the plot figure and info to edit"""
        try:
            if not global_plot_manager.is_available():
                print("⚠️ Plot history not available")
                return None, None
            
            if plot_id == "latest":
                # Get the latest plot
                return global_plot_manager.get_latest_plot()
            else:
                # Get specific plot by ID
                return global_plot_manager.get_plot_by_id(plot_id)
                
        except Exception as e:
            print(f"Error getting plot to edit: {e}")
            return None, None
    
    def _get_latest_plot(self) -> tuple[Optional[go.Figure], Optional[Dict]]:
        """Get the most recent plot"""
        return global_plot_manager.get_latest_plot()
    
    def _get_plot_by_id(self, plot_id: str) -> tuple[Optional[go.Figure], Optional[Dict]]:
        """Get a specific plot by ID"""
        return global_plot_manager.get_plot_by_id(plot_id)
    
    def _update_existing_plot(self, plot_id: str, edited_figure: go.Figure, new_title: str, plot_info: Dict):
        """Update an existing plot in place instead of creating a new one"""
        try:
            if not global_plot_manager.is_available():
                print("⚠️ Plot history not available for updating")
                return
            
            # Update the plot in the global plot manager
            success = global_plot_manager.update_existing_plot(plot_id, edited_figure, new_title)
            
            if success:
                print(f"✅ Successfully updated plot {plot_id} in place")
            else:
                print(f"⚠️ Failed to update plot {plot_id} in place")
                
        except Exception as e:
            print(f"Error updating existing plot: {e}")
    
    def _apply_edits(self, figure: go.Figure, inputs: PlotEditInput) -> List[str]:
        """Apply all the edits to the figure and return a list of changes made"""
        changes_made = []
        
        # Title and labels
        if inputs.new_title:
            figure.update_layout(title=inputs.new_title)
            changes_made.append(f"Updated title to '{inputs.new_title}'")
        
        if inputs.x_axis_title:
            figure.update_xaxes(title_text=inputs.x_axis_title)
            changes_made.append(f"Updated x-axis title to '{inputs.x_axis_title}'")
        
        if inputs.y_axis_title:
            figure.update_yaxes(title_text=inputs.y_axis_title)
            changes_made.append(f"Updated y-axis title to '{inputs.y_axis_title}'")
        
        # Colors and styling
        if inputs.marker_color:
            self._update_trace_colors(figure, inputs.marker_color)
            changes_made.append(f"Changed color to '{inputs.marker_color}'")
        
        if inputs.marker_size is not None:
            self._update_marker_sizes(figure, inputs.marker_size)
            changes_made.append(f"Changed marker size to {inputs.marker_size}")
        
        if inputs.line_width is not None:
            self._update_line_widths(figure, inputs.line_width)
            changes_made.append(f"Changed line width to {inputs.line_width}")
        
        if inputs.opacity is not None:
            self._update_opacity(figure, inputs.opacity)
            changes_made.append(f"Changed opacity to {inputs.opacity}")
        
        if inputs.color_scale:
            self._update_color_scale(figure, inputs.color_scale)
            changes_made.append(f"Changed color scale to '{inputs.color_scale}'")
        
        # Layout changes
        layout_updates = {}
        
        if inputs.background_color:
            layout_updates['plot_bgcolor'] = inputs.background_color
            layout_updates['paper_bgcolor'] = inputs.background_color
            changes_made.append(f"Changed background color to '{inputs.background_color}'")
        
        if inputs.grid_color:
            figure.update_xaxes(gridcolor=inputs.grid_color)
            figure.update_yaxes(gridcolor=inputs.grid_color)
            changes_made.append(f"Changed grid color to '{inputs.grid_color}'")
        
        if inputs.show_legend is not None:
            layout_updates['showlegend'] = inputs.show_legend
            changes_made.append(f"{'Showed' if inputs.show_legend else 'Hid'} legend")
        
        if inputs.new_template:
            layout_updates['template'] = inputs.new_template
            changes_made.append(f"Changed template to '{inputs.new_template}'")
        
        if layout_updates:
            figure.update_layout(**layout_updates)
        
        # Axis ranges
        if inputs.x_range:
            figure.update_xaxes(range=inputs.x_range)
            changes_made.append(f"Set x-axis range to {inputs.x_range}")
        
        if inputs.y_range:
            figure.update_yaxes(range=inputs.y_range)
            changes_made.append(f"Set y-axis range to {inputs.y_range}")
        
        return changes_made
    
    def _update_trace_colors(self, figure: go.Figure, color: str):
        """Update colors for all traces"""
        for trace in figure.data:
            if hasattr(trace, 'marker') and trace.marker:
                trace.marker.color = color
            if hasattr(trace, 'line') and trace.line:
                trace.line.color = color
    
    def _update_marker_sizes(self, figure: go.Figure, size: int):
        """Update marker sizes for scatter plots"""
        for trace in figure.data:
            if hasattr(trace, 'marker') and trace.marker:
                trace.marker.size = size
    
    def _update_line_widths(self, figure: go.Figure, width: int):
        """Update line widths for line plots"""
        for trace in figure.data:
            if hasattr(trace, 'line') and trace.line:
                trace.line.width = width
    
    def _update_opacity(self, figure: go.Figure, opacity: float):
        """Update opacity for all traces"""
        for trace in figure.data:
            if hasattr(trace, 'marker') and trace.marker:
                trace.marker.opacity = opacity
            if hasattr(trace, 'opacity'):
                trace.opacity = opacity
    
    def _update_color_scale(self, figure: go.Figure, color_scale: str):
        """Update color scale for traces that support it"""
        for trace in figure.data:
            if hasattr(trace, 'marker') and trace.marker and hasattr(trace.marker, 'colorscale'):
                trace.marker.colorscale = color_scale
            if hasattr(trace, 'colorscale'):
                trace.colorscale = color_scale 