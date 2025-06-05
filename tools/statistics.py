import time
import numpy as np
from typing import Dict, Any
from tools.base import BaseTool
from core.models import ToolInput, CorrelationInput, BootstrapInput, Message, MessageType
from pydantic import Field

class CorrelationTool(BaseTool):
    @property
    def name(self) -> str:
        return "analyze_correlation"
    
    @property
    def description(self) -> str:
        return "Analyze correlation between two variables with visualization"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return CorrelationInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0
    
    def execute(self, job_id: str, inputs: CorrelationInput) -> Dict[str, Any]:
        """Execute correlation analysis"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Starting correlation analysis...")
        time.sleep(1)
        
        # Progress: Generate data
        self.update_progress(job_id, 30, "Generating data...")
        time.sleep(1)
        
        n_points = inputs.n_points
        x = np.random.randn(n_points)
        y = 2 * x + np.random.randn(n_points) * 0.5
        
        # Progress: Compute correlation
        self.update_progress(job_id, 60, "Computing correlation...")
        time.sleep(1)
        
        correlation = float(np.corrcoef(x, y)[0, 1])
        
        # Progress: Create visualization
        self.update_progress(job_id, 90, "Creating visualization...")
        
        # Publish plot data
        plot_data = {
            "type": "scatter",
            "x": x[:100].tolist(),  # Limit for performance
            "y": y[:100].tolist(),
            "title": f"Correlation Analysis (r={correlation:.3f})",
            "xlabel": "Variable X",
            "ylabel": "Variable Y"
        }
        
        self.message_bus.publish(Message(
            type=MessageType.PLOT,
            job_id=job_id,
            data=plot_data
        ))
        
        time.sleep(0.5)
        
        # Complete
        self.update_progress(job_id, 100, "Analysis complete!")
        
        # Return results (this goes to Claude, not the plot data)
        return {
            "correlation_coefficient": correlation,
            "n_points": n_points,
            "interpretation": "Strong positive correlation" if correlation > 0.7 else "Moderate correlation",
            "confidence_level": 0.95,
            "p_value": 0.001  # Simplified for demo
        }


class BootstrapTool(BaseTool):
    @property
    def name(self) -> str:
        return "bootstrap_analysis"
    
    @property
    def description(self) -> str:
        return "Perform bootstrap analysis to estimate sampling distribution"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return BootstrapInput
    
    @property
    def estimated_duration(self) -> float:
        return 10.0
    
    def execute(self, job_id: str, inputs: BootstrapInput) -> Dict[str, Any]:
        """Execute bootstrap analysis"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Starting bootstrap analysis...")
        time.sleep(0.5)
        
        # Generate base data
        base_data = np.random.randn(100)
        bootstrap_means = []
        n_iterations = inputs.n_iterations
        
        # Run bootstrap
        for i in range(n_iterations):
            if i % 100 == 0:
                progress = (i / n_iterations) * 80  # Leave 20% for final steps
                self.update_progress(
                    job_id, 
                    progress, 
                    f"Bootstrap iteration {i}/{n_iterations}"
                )
                time.sleep(0.1)
            
            # Bootstrap sample
            sample = np.random.choice(base_data, size=len(base_data), replace=True)
            bootstrap_means.append(float(np.mean(sample)))
        
        # Progress: Create visualization
        self.update_progress(job_id, 90, "Creating visualization...")
        
        # Publish plot data
        plot_data = {
            "type": "histogram",
            "values": bootstrap_means,
            "title": "Bootstrap Distribution of Means",
            "xlabel": "Sample Mean",
            "ylabel": "Frequency"
        }
        
        self.message_bus.publish(Message(
            type=MessageType.PLOT,
            job_id=job_id,
            data=plot_data
        ))
        
        time.sleep(0.5)
        
        # Complete
        self.update_progress(job_id, 100, "Bootstrap analysis complete!")
        
        # Return results
        return {
            "mean_of_means": float(np.mean(bootstrap_means)),
            "std_of_means": float(np.std(bootstrap_means)),
            "ci_lower": float(np.percentile(bootstrap_means, 2.5)),
            "ci_upper": float(np.percentile(bootstrap_means, 97.5)),
            "n_iterations": n_iterations,
            "original_sample_size": len(base_data)
        }