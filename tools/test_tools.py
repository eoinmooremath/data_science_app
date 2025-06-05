import time
import numpy as np
import pandas as pd
import plotly.express as px
from typing import Dict, Any
from tools.base import BaseTool
from core.models import ToolInput, Message, MessageType
from pydantic import BaseModel, Field

class RandomPlotInput(BaseModel):
    """Input for random plot generation"""
    plot_type: str = Field(default="scatter", description="Type of plot to generate (scatter, histogram)")
    n_points: int = Field(default=100, description="Number of data points")

class RandomPlotTool(BaseTool):
    @property
    def name(self) -> str:
        return "generate_random_plot"
    
    @property
    def description(self) -> str:
        return "Generate a random plot for testing the visualization system"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return RandomPlotInput
    
    @property
    def estimated_duration(self) -> float:
        return 2.0
    
    def execute(self, job_id: str, inputs: RandomPlotInput) -> Dict[str, Any]:
        """Execute random plot generation"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Generating random data...")
        time.sleep(0.5)
        
        n_points = inputs.n_points
        plot_type = inputs.plot_type
        
        # Progress: Generate data
        self.update_progress(job_id, 50, f"Creating {plot_type} plot...")
        time.sleep(0.5)
        
        if plot_type == "scatter":
            x = np.random.randn(n_points)
            y = 2 * x + np.random.randn(n_points) * 0.5
            
            # Create Plotly figure directly
            fig = px.scatter(
                x=x, y=y,
                title=f"Random Scatter Plot ({n_points} points)",
                labels={"x": "X Values", "y": "Y Values"},
                template="plotly_white"
            )
            
            # Add trendline
            fig.add_scatter(
                x=x, y=2*x,  # Perfect trend line
                mode='lines',
                name='True Relationship',
                line=dict(color='red', dash='dash')
            )
            
        elif plot_type == "histogram":
            values = np.random.normal(0, 1, n_points)
            
            # Create Plotly figure directly
            fig = px.histogram(
                x=values,
                title=f"Random Histogram ({n_points} values)",
                labels={"x": "Value", "y": "Frequency"},
                template="plotly_white",
                nbins=30
            )
            
            # Add mean line
            mean_val = np.mean(values)
            fig.add_vline(
                x=mean_val,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mean: {mean_val:.2f}"
            )
            
        else:
            # Default to scatter
            x = np.random.randn(n_points)
            y = np.random.randn(n_points)
            
            fig = px.scatter(
                x=x, y=y,
                title=f"Random Plot ({n_points} points)",
                labels={"x": "X Values", "y": "Y Values"},
                template="plotly_white"
            )
        
        # Progress: Publishing plot
        self.update_progress(job_id, 90, "Publishing visualization...")
        
        # Create plot data with figure object
        plot_data = {
            "figure": fig,
            "title": fig.layout.title.text,
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        # Publish plot data
        self.message_bus.publish(Message(
            type=MessageType.PLOT,
            job_id=job_id,
            data=plot_data
        ))
        
        time.sleep(0.5)
        
        # Complete
        self.update_progress(job_id, 100, "Plot generated successfully!")
        
        # Return results
        return {
            "plot_type": plot_type,
            "n_points": n_points,
            "data_range": {
                "x_min": float(np.min(x if plot_type == "scatter" else values)),
                "x_max": float(np.max(x if plot_type == "scatter" else values)),
            },
            "message": f"Successfully generated {plot_type} plot with {n_points} data points"
        } 