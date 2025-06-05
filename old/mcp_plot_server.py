import asyncio
import json
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import tempfile
import os
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Shared state file for plot data
PLOT_DATA_FILE = os.path.join(tempfile.gettempdir(), 'mcp_plot_data.json')

class PlotMCPServer:
    def __init__(self):
        self.server = Server("plot-test-server")
        
    async def list_tools_handler(self):
        return [
            Tool(
                name="analyze_correlation",
                description="Analyze correlation between two variables and create scatter plot",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n_points": {"type": "integer", "description": "Number of data points", "default": 100}
                    }
                }
            ),
            Tool(
                name="analyze_distribution",
                description="Analyze data distribution and create histogram",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n_samples": {"type": "integer", "description": "Number of samples", "default": 1000}
                    }
                }
            )
        ]
    
    async def call_tool_handler(self, name: str, arguments: dict):
        if name == "analyze_correlation":
            return await self._analyze_correlation(arguments.get("n_points", 100))
        elif name == "analyze_distribution":
            return await self._analyze_distribution(arguments.get("n_samples", 1000))
    
    async def _analyze_correlation(self, n_points: int):
        """Generate correlation data and save plot data"""
        # Generate correlated data
        x = np.random.randn(n_points)
        y = 2 * x + np.random.randn(n_points) * 0.5
        
        # Calculate correlation
        correlation = np.corrcoef(x, y)[0, 1]
        
        # Save plot data for Dash app
        plot_data = {
            "type": "scatter",
            "x": x.tolist(),
            "y": y.tolist(),
            "title": f"Correlation Analysis (r={correlation:.3f})",
            "xlabel": "Variable X",
            "ylabel": "Variable Y"
        }
        
        with open(PLOT_DATA_FILE, 'w') as f:
            json.dump(plot_data, f)
        
        # Return description to LLM (not the actual plot)
        return [TextContent(
            type="text",
            text=json.dumps({
                "analysis_type": "correlation",
                "plot_displayed": True,
                "plot_type": "scatter",
                "n_points": n_points,
                "correlation_coefficient": float(correlation),
                "interpretation": f"Strong positive correlation (r={correlation:.3f})" if correlation > 0.7 
                                else f"Moderate correlation (r={correlation:.3f})" if correlation > 0.3
                                else f"Weak correlation (r={correlation:.3f})",
                "summary_statistics": {
                    "x_mean": float(np.mean(x)),
                    "y_mean": float(np.mean(y)),
                    "x_std": float(np.std(x)),
                    "y_std": float(np.std(y))
                }
            }, indent=2)
        )]
    
    async def _analyze_distribution(self, n_samples: int):
        """Generate distribution data and save plot data"""
        # Generate mixture of gaussians
        data = np.concatenate([
            np.random.normal(0, 1, n_samples // 2),
            np.random.normal(4, 1.5, n_samples // 2)
        ])
        
        # Save plot data
        hist, bins = np.histogram(data, bins=50)
        
        plot_data = {
            "type": "histogram",
            "values": data.tolist(),
            "bins": bins.tolist(),
            "title": "Distribution Analysis",
            "xlabel": "Value",
            "ylabel": "Frequency"
        }
        
        with open(PLOT_DATA_FILE, 'w') as f:
            json.dump(plot_data, f)
        
        # Return description to LLM
        return [TextContent(
            type="text",
            text=json.dumps({
                "analysis_type": "distribution",
                "plot_displayed": True,
                "plot_type": "histogram",
                "n_samples": n_samples,
                "distribution_characteristics": {
                    "appears_bimodal": True,
                    "peaks_at": [0, 4],
                    "mean": float(np.mean(data)),
                    "std": float(np.std(data)),
                    "min": float(np.min(data)),
                    "max": float(np.max(data)),
                    "skewness": float(((data - np.mean(data)) ** 3).mean() / np.std(data) ** 3)
                },
                "interpretation": "The data shows a bimodal distribution with two distinct peaks"
            }, indent=2)
        )]
    
    async def run(self):
        @self.server.list_tools()
        async def list_tools():
            return await self.list_tools_handler()
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            return await self.call_tool_handler(name, arguments)
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

if __name__ == "__main__":
    server = PlotMCPServer()
    asyncio.run(server.run())