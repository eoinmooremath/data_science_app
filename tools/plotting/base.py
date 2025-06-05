# tools/plotting/base.py
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from abc import abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Union
from pydantic import BaseModel, Field
import numpy as np

from tools.base import BaseTool
from core.models import ToolInput, Message, MessageType
from tools.data_tools import uploaded_datasets


class BasePlottingInput(BaseModel):
    """Base input model for all plotting tools"""
    title: Optional[str] = Field(default=None, description="Plot title")
    width: Optional[int] = Field(default=None, description="Plot width in pixels")
    height: Optional[int] = Field(default=None, description="Plot height in pixels")
    template: Optional[str] = Field(default="plotly_white", description="Plotly template (plotly_white, plotly_dark, etc.)")


class BasePlottingTool(BaseTool):
    """Base class for all plotting tools with column discovery and validation"""
    
    def __init__(self, job_manager, message_bus):
        super().__init__(job_manager, message_bus)
        self._available_columns = None
        self._numeric_columns = None
        self._categorical_columns = None
        self._datetime_columns = None
        self._dataframe = None
    
    @property
    def estimated_duration(self) -> float:
        return 3.0  # Most plots should complete within 3 seconds
    
    # Abstract methods that subclasses must implement
    @abstractmethod
    def create_figure(self, df: pd.DataFrame, **params) -> go.Figure:
        """Create the Plotly figure - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def get_plot_specific_parameters(self) -> List[str]:
        """Return parameters specific to this plot type"""
        pass
    
    # Column discovery and validation
    def _discover_columns(self) -> Dict[str, List[str]]:
        """Auto-discover available columns from uploaded datasets"""
        if self._dataframe is None:
            self._dataframe = self._get_dataframe()
        
        if self._dataframe is None or self._dataframe.empty:
            return {
                "all": [],
                "numeric": [],
                "categorical": [],
                "datetime": []
            }
        
        df = self._dataframe
        
        # Identify column types
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Also check for columns that could be converted to datetime
        for col in categorical_cols.copy():
            if df[col].dtype == 'object':
                # Try to detect datetime-like strings
                sample = df[col].dropna().head(10)
                if len(sample) > 0:
                    try:
                        pd.to_datetime(sample.iloc[0])
                        datetime_cols.append(col)
                        categorical_cols.remove(col)
                    except:
                        pass
        
        return {
            "all": df.columns.tolist(),
            "numeric": numeric_cols,
            "categorical": categorical_cols,
            "datetime": datetime_cols
        }
    
    def _get_dataframe(self) -> Optional[pd.DataFrame]:
        """Get the current dataframe from the data manager"""
        from tools.data_tools import uploaded_datasets
        
        # Try to get the most recent dataset
        if 'uploaded' in uploaded_datasets:
            return uploaded_datasets['uploaded']
        elif 'generated' in uploaded_datasets:
            return uploaded_datasets['generated']
        elif uploaded_datasets:
            # Return the first available dataset
            return next(iter(uploaded_datasets.values()))
        
        return None
    
    @property
    def available_columns(self) -> Dict[str, List[str]]:
        """Get available columns, discovering them if needed"""
        if self._available_columns is None:
            self._available_columns = self._discover_columns()
        return self._available_columns
    
    def validate_column(self, column_name: str, required_type: Optional[str] = None) -> Tuple[bool, str]:
        """Validate that column exists and has correct type"""
        columns = self.available_columns
        
        if column_name not in columns["all"]:
            available = ", ".join(columns["all"][:5])
            if len(columns["all"]) > 5:
                available += f" (and {len(columns['all']) - 5} more)"
            return False, f"Column '{column_name}' not found. Available columns: {available}"
        
        if required_type:
            if required_type == "numeric" and column_name not in columns["numeric"]:
                return False, f"Column '{column_name}' must be numeric. Numeric columns: {', '.join(columns['numeric'])}"
            elif required_type == "categorical" and column_name not in columns["categorical"]:
                return False, f"Column '{column_name}' must be categorical. Categorical columns: {', '.join(columns['categorical'])}"
            elif required_type == "datetime" and column_name not in columns["datetime"]:
                return False, f"Column '{column_name}' must be datetime. Datetime columns: {', '.join(columns['datetime'])}"
        
        return True, ""
    
    def suggest_columns(self, plot_type: str) -> Dict[str, List[str]]:
        """Suggest appropriate columns for a plot type"""
        columns = self.available_columns
        suggestions = {}
        
        if plot_type in ["scatter", "line"]:
            suggestions = {
                "x": columns["numeric"] + columns["datetime"],
                "y": columns["numeric"],
                "color": columns["categorical"] + columns["numeric"][:3],  # Limit numeric for color
                "size": columns["numeric"][:3]
            }
        elif plot_type == "bar":
            suggestions = {
                "x": columns["categorical"] + columns["datetime"],
                "y": columns["numeric"],
                "color": columns["categorical"]
            }
        elif plot_type == "histogram":
            suggestions = {
                "x": columns["numeric"],
                "color": columns["categorical"]
            }
        elif plot_type == "box":
            suggestions = {
                "x": columns["categorical"],
                "y": columns["numeric"],
                "color": columns["categorical"]
            }
        
        return suggestions
    
    # Parameter management
    def get_core_parameters(self) -> List[str]:
        """Return core parameters that every plot type should have"""
        return ["title", "width", "height", "template"]
    
    def filter_valid_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Filter parameters to only include valid ones for Plotly Express"""
        valid_params = {}
        core_params = self.get_core_parameters()
        plot_params = self.get_plot_specific_parameters()
        all_valid = core_params + plot_params
        
        for key, value in params.items():
            if key in all_valid and value is not None:
                valid_params[key] = value
        
        return valid_params
    
    def apply_smart_defaults(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply intelligent defaults based on data types and available columns"""
        columns = self.available_columns
        
        # Auto-suggest columns if not provided
        if "x" not in params and columns["numeric"]:
            params["x"] = columns["numeric"][0]
        
        if "y" not in params and len(columns["numeric"]) > 1:
            params["y"] = columns["numeric"][1]
        elif "y" not in params and columns["numeric"]:
            params["y"] = columns["numeric"][0]
        
        # Default styling
        if "template" not in params:
            params["template"] = "plotly_white"
        
        if "height" not in params:
            params["height"] = 500
        
        return params
    
    # Figure creation and styling
    def apply_common_styling(self, fig: go.Figure, **params) -> go.Figure:
        """Apply consistent styling across all plots"""
        fig.update_layout(
            template=params.get("template", "plotly_white"),
            height=params.get("height", 500),
            width=params.get("width"),
            title_x=0.5,  # Center title
            font=dict(size=12),
            title_font_size=16,
            margin=dict(l=50, r=50, t=60, b=50),
            hovermode='closest'
        )
        
        # Add professional color scheme
        if hasattr(fig, 'data') and fig.data:
            color_palette = px.colors.qualitative.Set3
            for i, trace in enumerate(fig.data):
                if hasattr(trace, 'marker') and trace.marker.color is None:
                    trace.marker.color = color_palette[i % len(color_palette)]
        
        return fig
    
    def add_interactivity(self, fig: go.Figure, **params) -> go.Figure:
        """Add hover, zoom, pan, download functionality"""
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            )
        )
        
        # Configure toolbar
        config = {
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': params.get("title", "plot").replace(" ", "_").lower(),
                'height': params.get("height", 500),
                'width': params.get("width", 700),
                'scale': 1
            }
        }
        
        # Store config in figure for later use
        fig._config = config
        
        return fig
    
    # Error handling
    def create_error_figure(self, error_message: str) -> go.Figure:
        """Create informative error visualization"""
        fig = go.Figure()
        fig.add_annotation(
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            text=f"❌ Error creating plot:<br><br>{error_message}",
            showarrow=False,
            font=dict(size=14, color="red"),
            align="center"
        )
        fig.update_layout(
            title="Plot Error",
            height=400,
            template="plotly_white",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    def validate_inputs(self, **params) -> Tuple[bool, str]:
        """Validate all inputs before creating plot"""
        # Check if we have data
        if self._dataframe is None:
            self._dataframe = self._get_dataframe()
        
        if self._dataframe is None or self._dataframe.empty:
            return False, "No data available. Please upload a dataset first."
        
        # Validate required columns exist
        for param_name, column_name in params.items():
            if param_name in ["x", "y", "color", "size"] and column_name:
                valid, error = self.validate_column(column_name)
                if not valid:
                    return False, error
        
        return True, ""
    
    # Main execution method
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute the plotting tool"""
        try:
            # Progress: Start
            self.update_progress(job_id, 0, "Initializing plot creation...")
            
            # Convert inputs to dict
            params = inputs.dict() if hasattr(inputs, 'dict') else inputs
            
            # Progress: Validate inputs
            self.update_progress(job_id, 20, "Validating inputs and data...")
            
            # Validate inputs
            valid, error_msg = self.validate_inputs(**params)
            if not valid:
                error_fig = self.create_error_figure(error_msg)
                self._publish_plot(job_id, error_fig, f"Error: {error_msg}")
                return {"error": error_msg}
            
            # Progress: Apply defaults
            self.update_progress(job_id, 40, "Applying smart defaults...")
            params = self.apply_smart_defaults(params)
            
            # Progress: Create figure
            self.update_progress(job_id, 60, "Creating visualization...")
            
            # Get dataframe
            df = self._dataframe
            
            # Create the figure
            fig = self.create_figure(df, **params)
            
            # Progress: Apply styling
            self.update_progress(job_id, 80, "Applying styling and interactivity...")
            
            # Apply common styling and interactivity
            fig = self.apply_common_styling(fig, **params)
            fig = self.add_interactivity(fig, **params)
            
            # Progress: Publishing
            self.update_progress(job_id, 95, "Publishing visualization...")
            
            # Publish the plot
            plot_title = params.get("title", f"{self.name.replace('_', ' ').title()}")
            self._publish_plot(job_id, fig, plot_title)
            
            # Complete
            self.update_progress(job_id, 100, "Visualization created successfully!")
            
            return {
                "plot_title": plot_title,
                "columns_used": {k: v for k, v in params.items() if k in ["x", "y", "color", "size"] and v},
                "message": f"Successfully created {plot_title}"
            }
            
        except Exception as e:
            error_msg = f"Error creating plot: {str(e)}"
            error_fig = self.create_error_figure(error_msg)
            self._publish_plot(job_id, error_fig, "Plot Error")
            return {"error": error_msg}
    
    def _publish_plot(self, job_id: str, figure: go.Figure, title: str):
        """Publish the plot to the message bus"""
        plot_data = {
            "figure": figure,
            "title": title,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        self.message_bus.publish(Message(
            type=MessageType.PLOT,
            job_id=job_id,
            data=plot_data
        )) 