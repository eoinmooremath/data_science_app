from typing import Optional, List
import pandas as pd
import plotly.express as px
from pydantic import Field

from core.models import ToolInput
from tools.plotting.base import BasePlottingTool

class ScatterInput(ToolInput):
    """Input model for the scatter plot tool, mirroring plotly.express.scatter."""
    dataset_id: str = Field("generated", description="The ID of the dataset to use (e.g., 'generated', 'uploaded').")
    x: str = Field(..., description="The name of the column for the x-axis.")
    y: str = Field(..., description="The name of the column for the y-axis.")
    color: Optional[str] = Field(None, description="The name of the column to use for coloring the points.")
    size: Optional[str] = Field(None, description="The name of the column to determine marker size.")
    title: Optional[str] = Field("Scatter Plot", description="The title of the plot.")
    labels: Optional[dict] = Field(None, description="A dictionary to rename axis labels (e.g., {'x_column_name': 'New X Label'}).")
    template: Optional[str] = Field("plotly_white", description="Plotly template to use for styling.")
    hover_data: Optional[List[str]] = Field(None, description="List of columns to appear in the hover tooltip.")
    facet_row: Optional[str] = Field(None, description="Column to use for creating faceted subplots, stacked vertically.")
    facet_col: Optional[str] = Field(None, description="Column to use for creating faceted subplots, arranged horizontally.")

class ScatterTool(BasePlottingTool):
    """A tool to create a scatter plot, powered by Plotly Express."""
    
    name: str = "plotting_scatter"
    description: str = "Creates a highly customizable 2D scatter plot from a dataset's columns. Supports coloring, sizing, and faceting."
    input_model: type[ToolInput] = ScatterInput

    def _create_figure(self, df: pd.DataFrame, inputs: ScatterInput) -> any:
        """Creates a scatter plot using plotly.express.scatter."""
        
        # Prepare arguments for Plotly Express
        plot_args = {
            "x": inputs.x,
            "y": inputs.y,
            "title": inputs.title or f"Scatter Plot of {inputs.dataset_id}",
            "labels": {"x": inputs.x_label, "y": inputs.y_label}
        }
        
        # Smartly handle the 'color' argument
        if inputs.color:
            if inputs.color in df.columns:
                plot_args['color'] = inputs.color  # Color by a data column
            else:
                # Use the color as a static value for all markers
                plot_args['color_discrete_sequence'] = [inputs.color]
        
        # Handle other optional plot arguments
        if inputs.size and inputs.size in df.columns:
            plot_args['size'] = inputs.size
        
        # Filter out None values so we use plotly's defaults
        plot_kwargs = {k: v for k, v in plot_args.items() if v is not None}
        
        fig = px.scatter(df, **plot_kwargs)
        
        return fig 