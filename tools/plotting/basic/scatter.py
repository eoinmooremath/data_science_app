# tools/plotting/basic/scatter.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
import re

from core.models import ToolInput
from ..base import BasePlottingTool, BasePlottingInput


class ScatterPlotInput(BasePlottingInput):
    """Input model for scatter plot tool with intelligent parameter handling"""
    x: str = Field(description="Column name for x-axis (numeric or datetime)")
    y: str = Field(description="Column name for y-axis (numeric)")
    
    # Intelligent parameters - can be column names OR direct values
    color: Optional[str] = Field(default=None, description="Column name OR direct color (red, blue, #FF0000, etc.)")
    size: Optional[Any] = Field(default=None, description="Column name OR fixed size number")
    symbol: Optional[str] = Field(default=None, description="Column name OR symbol name (circle, square, etc.)")
    opacity: Optional[float] = Field(default=0.7, description="Marker opacity (0-1)")
    
    # Direct styling parameters
    marker_size: Optional[int] = Field(default=None, description="Fixed marker size for all points")
    marker_symbol: Optional[str] = Field(default=None, description="Fixed marker symbol")
    
    # Advanced options
    color_discrete_sequence: Optional[List[str]] = Field(default=None, description="Custom color palette")
    color_continuous_scale: Optional[str] = Field(default=None, description="Color scale (viridis, plasma, etc.)")
    size_max: Optional[int] = Field(default=20, description="Maximum marker size")
    
    # Hover and interaction
    hover_name: Optional[str] = Field(default=None, description="Column for hover labels")
    hover_data: Optional[List[str]] = Field(default=None, description="Additional hover columns")
    
    # Layout options
    log_x: Optional[bool] = Field(default=False, description="Logarithmic x-axis")
    log_y: Optional[bool] = Field(default=False, description="Logarithmic y-axis")
    range_x: Optional[List[float]] = Field(default=None, description="X-axis range [min, max]")
    range_y: Optional[List[float]] = Field(default=None, description="Y-axis range [min, max]")
    
    # Trendline
    trendline: Optional[str] = Field(default=None, description="Trendline type (ols, lowess, etc.)")
    
    # Marginal plots
    marginal_x: Optional[str] = Field(default=None, description="X marginal plot type")
    marginal_y: Optional[str] = Field(default=None, description="Y marginal plot type")


class ScatterPlotTool(BasePlottingTool):
    """Intelligent scatter plot tool with automatic parameter interpretation"""
    
    @property
    def name(self) -> str:
        return "plotting_basic_scatter"
    
    @property
    def description(self) -> str:
        return """Create scatter plots with intelligent parameter handling.
        
        This tool automatically interprets parameters as either:
        - Column names (if they exist in the data)
        - Direct values (colors, sizes, symbols, etc.)
        
        Examples:
        - color="red" → all points red
        - color="category" → color by category column
        - size=10 → all points size 10
        - size="value" → size by value column
        
        Can auto-generate data if none is available."""
    
    @property
    def input_model(self) -> type[ToolInput]:
        return ScatterPlotInput
    
    def get_plot_specific_parameters(self) -> List[str]:
        return [
            "x", "y", "color", "size", "symbol", "opacity", "marker_size", "marker_symbol",
            "color_discrete_sequence", "color_continuous_scale", "size_max",
            "hover_name", "hover_data", "log_x", "log_y", "range_x", "range_y",
            "trendline", "marginal_x", "marginal_y"
        ]
    
    def _interpret_parameter(self, param_name: str, param_value: Any, df: pd.DataFrame) -> Dict[str, Any]:
        """Intelligently interpret a parameter as either column name or direct value"""
        if param_value is None:
            return {}
        
        # For string parameters, check if it's a column name first
        if isinstance(param_value, str) and param_value in df.columns:
            # It's a valid column name
            return {param_name: param_value}
        
        # Handle specific parameter types
        if param_name == "color":
            if isinstance(param_value, str):
                # Check if it's a color name or hex
                color_names = {
                    'red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown',
                    'black', 'white', 'gray', 'grey', 'cyan', 'magenta', 'lime', 'navy',
                    'maroon', 'olive', 'teal', 'silver', 'gold', 'indigo', 'violet',
                    'crimson', 'coral', 'salmon', 'khaki', 'plum', 'orchid', 'turquoise'
                }
                
                if (param_value.lower() in color_names or 
                    param_value.startswith('#') or 
                    param_value.startswith('rgb')):
                    # It's a direct color - we'll apply it after creating the figure
                    return {"_direct_color": param_value}
                else:
                    # Treat as column name even if not found (will error appropriately)
                    return {param_name: param_value}
        
        elif param_name == "size":
            if isinstance(param_value, (int, float)):
                # Direct size value
                return {"_direct_size": param_value}
            elif isinstance(param_value, str):
                # Column name
                return {param_name: param_value}
        
        elif param_name == "symbol":
            if isinstance(param_value, str):
                symbol_names = {
                    'circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 
                    'triangle-down', 'triangle-left', 'triangle-right', 'pentagon',
                    'hexagon', 'star', 'hourglass', 'bowtie'
                }
                
                if param_value.lower() in symbol_names:
                    return {"_direct_symbol": param_value}
                else:
                    return {param_name: param_value}
        
        # For all other parameters, pass through directly
        return {param_name: param_value}
    
    def create_figure(self, df: pd.DataFrame, **params) -> go.Figure:
        """Create scatter plot with intelligent parameter interpretation"""
        
        if df is None or df.empty:
            raise ValueError("No data available. Please upload a dataset or generate data first.")
        
        # Validate required columns
        x_col = params["x"]
        y_col = params["y"]
        
        if x_col not in df.columns:
            raise ValueError(f"Column '{x_col}' not found. Available: {list(df.columns)}")
        if y_col not in df.columns:
            raise ValueError(f"Column '{y_col}' not found. Available: {list(df.columns)}")
        
        # Build plotly express parameters
        px_params = {
            "data_frame": df,
            "x": x_col,
            "y": y_col,
            "title": params.get("title", f"{y_col} vs {x_col}"),
            "template": params.get("template", "plotly_white"),
            "height": params.get("height", 500),
            "width": params.get("width")
        }
        
        # Interpret intelligent parameters
        direct_styling = {}
        
        for param_name in ["color", "size", "symbol", "hover_name", "hover_data"]:
            if param_name in params:
                interpreted = self._interpret_parameter(param_name, params[param_name], df)
                
                # Separate direct styling from plotly parameters
                for key, value in interpreted.items():
                    if key.startswith("_direct_"):
                        direct_styling[key] = value
                    else:
                        px_params[key] = value
        
        # Add other parameters directly
        for param in ["opacity", "size_max", "log_x", "log_y", "range_x", "range_y", 
                     "trendline", "marginal_x", "marginal_y", "color_discrete_sequence", 
                     "color_continuous_scale"]:
            if params.get(param) is not None:
                px_params[param] = params[param]
        
        # Create the figure
        fig = px.scatter(**px_params)
        
        # Apply direct styling
        if "_direct_color" in direct_styling:
            fig.update_traces(marker_color=direct_styling["_direct_color"])
        
        if "_direct_size" in direct_styling:
            fig.update_traces(marker_size=direct_styling["_direct_size"])
        
        if "_direct_symbol" in direct_styling:
            fig.update_traces(marker_symbol=direct_styling["_direct_symbol"])
        
        # Apply marker_size and marker_symbol if specified directly
        if params.get("marker_size"):
            fig.update_traces(marker_size=params["marker_size"])
        
        if params.get("marker_symbol"):
            fig.update_traces(marker_symbol=params["marker_symbol"])
        
        return fig 