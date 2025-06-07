"""
Base class for statistical tools

This module provides the base class for all statistical function tools,
following the same pattern as the plotting tools.
"""

import time
import numpy as np
from typing import Dict, Any, Optional
from tools.base import BaseTool
from core.models import ToolInput, Message, MessageType


class BaseStatisticalTool(BaseTool):
    """Base class for all statistical function tools"""
    
    name: str = ""
    description: str = ""
    input_model = ToolInput
    _statistical_function = None
    
    @property
    def estimated_duration(self) -> float:
        return 3.0  # Most statistical tests are quick
    
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute the statistical function"""
        
        # Start progress
        self.update_progress(job_id, 0, f"Starting {self.name}...")
        time.sleep(0.1)
        
        try:
            # Prepare arguments
            kwargs = {}
            for field_name, field_info in inputs.__fields__.items():
                value = getattr(inputs, field_name, None)
                if value is not None and field_name not in ['create_plot', 'alpha']:
                    kwargs[field_name] = value
            
            # Update progress
            self.update_progress(job_id, 50, "Running statistical analysis...")
            time.sleep(0.2)
            
            # Execute function
            if self._statistical_function is None:
                raise ValueError(f"No statistical function defined for {self.name}")
            
            result = self._statistical_function(**kwargs)
            
            # Format results
            self.update_progress(job_id, 90, "Formatting results...")
            formatted_result = self._format_statistical_result(result)
            
            # Create plot if requested
            if getattr(inputs, 'create_plot', False):
                self._create_statistical_plot(job_id, result, kwargs)
            
            self.update_progress(job_id, 100, "Analysis complete!")
            return formatted_result
            
        except Exception as e:
            self.update_progress(job_id, 100, f"Error: {str(e)}")
            return {"error": str(e), "success": False}
    
    def _format_statistical_result(self, result: Any) -> Dict[str, Any]:
        """Format statistical results for return to Claude"""
        if hasattr(result, '_asdict'):  # Named tuple
            return result._asdict()
        elif isinstance(result, tuple):
            if len(result) == 2:
                return {"statistic": float(result[0]), "p_value": float(result[1])}
            elif len(result) == 3:
                return {"statistic": float(result[0]), "p_value": float(result[1]), "additional": result[2]}
            else:
                return {"result": list(result)}
        elif isinstance(result, (int, float)):
            return {"result": float(result)}
        elif hasattr(result, 'summary'):  # Statsmodels result
            return {
                "summary": str(result.summary()),
                "params": result.params.to_dict() if hasattr(result, 'params') else None,
                "pvalues": result.pvalues.to_dict() if hasattr(result, 'pvalues') else None,
                "rsquared": getattr(result, 'rsquared', None),
                "aic": getattr(result, 'aic', None),
                "bic": getattr(result, 'bic', None)
            }
        else:
            return {"result": str(result)}
    
    def _create_statistical_plot(self, job_id: str, result: Any, kwargs: Dict[str, Any]):
        """Create visualization for statistical results"""
        # This can be overridden by specific tools that support visualization
        # For now, we'll create basic plots based on the data type
        
        try:
            plot_data = None
            
            # Check if we have data arrays to plot
            if 'x' in kwargs and 'y' in kwargs:
                # Scatter plot for correlation analysis
                plot_data = {
                    "type": "scatter",
                    "x": list(kwargs['x']),
                    "y": list(kwargs['y']),
                    "title": f"Data Visualization - {self.name}",
                    "xlabel": "X Variable",
                    "ylabel": "Y Variable"
                }
            elif 'data' in kwargs:
                # Histogram for single variable analysis
                data = kwargs['data']
                if isinstance(data, (list, np.ndarray)):
                    plot_data = {
                        "type": "histogram",
                        "values": list(data),
                        "title": f"Data Distribution - {self.name}",
                        "xlabel": "Value",
                        "ylabel": "Frequency"
                    }
            elif any(key in kwargs for key in ['sample1', 'sample2']):
                # Box plot for comparing samples
                samples = []
                labels = []
                if 'sample1' in kwargs:
                    samples.append(list(kwargs['sample1']))
                    labels.append("Sample 1")
                if 'sample2' in kwargs:
                    samples.append(list(kwargs['sample2']))
                    labels.append("Sample 2")
                
                if samples:
                    plot_data = {
                        "type": "box",
                        "samples": samples,
                        "labels": labels,
                        "title": f"Sample Comparison - {self.name}",
                        "ylabel": "Value"
                    }
            
            # Publish plot if we created one
            if plot_data:
                self.message_bus.publish(Message(
                    type=MessageType.PLOT,
                    job_id=job_id,
                    data=plot_data
                ))
                
        except Exception as e:
            # Don't fail the whole analysis if plotting fails
            print(f"Warning: Could not create plot for {self.name}: {e}")
            pass 