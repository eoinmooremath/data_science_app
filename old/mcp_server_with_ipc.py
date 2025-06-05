import asyncio
import json
import numpy as np
import threading
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from ipc.queue_manager import get_queue_manager
import uuid

class DataScienceMCPServer:
    def __init__(self):
        self.server = Server("datascience-server")
        self.queue_manager = get_queue_manager()
        
    async def list_tools_handler(self):
        return [
            Tool(
                name="start_correlation_analysis",
                description="Start correlation analysis (returns job ID immediately)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n_points": {"type": "integer", "default": 1000}
                    }
                }
            ),
            Tool(
                name="start_bootstrap_analysis", 
                description="Start bootstrap analysis (returns job ID immediately)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n_iterations": {"type": "integer", "default": 1000}
                    }
                }
            ),
            Tool(
                name="check_job_status",
                description="Check status of a running job",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "string", "required": True}
                    }
                }
            )
        ]
    
    async def call_tool_handler(self, name: str, arguments: dict):
        if name == "start_correlation_analysis":
            return await self._start_correlation_analysis(arguments.get("n_points", 1000))
        elif name == "start_bootstrap_analysis":
            return await self._start_bootstrap_analysis(arguments.get("n_iterations", 1000))
        elif name == "check_job_status":
            return await self._check_job_status(arguments["job_id"])
    
    async def _start_correlation_analysis(self, n_points: int):
        """Start analysis and return immediately"""
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        
        # Start analysis in background thread
        thread = threading.Thread(
            target=self._run_correlation_analysis,
            args=(job_id, n_points)
        )
        thread.daemon = True
        thread.start()
        
        # Return immediately with job ID
        return [TextContent(
            type="text",
            text=json.dumps({
                "job_id": job_id,
                "status": "started",
                "message": f"Correlation analysis started with {n_points} points. Monitor job_id: {job_id}"
            }, indent=2)
        )]
    
    def _run_correlation_analysis(self, job_id: str, n_points: int):
        """Run analysis in background"""
        import time
        
        # Progress: Generating data
        self.queue_manager.publish_progress(job_id, 0, "Generating data...")
        time.sleep(1)
        
        x = np.random.randn(n_points)
        y = 2 * x + np.random.randn(n_points) * 0.5
        
        self.queue_manager.publish_progress(job_id, 50, "Computing correlation...")
        time.sleep(1)
        
        correlation = np.corrcoef(x, y)[0, 1]
        
        # Create plot data
        plot_data = {
            "type": "scatter",
            "x": x.tolist()[:100],  # Limit points for performance
            "y": y.tolist()[:100],
            "title": f"Correlation Analysis (r={correlation:.3f})",
            "xlabel": "Variable X",
            "ylabel": "Variable Y"
        }
        
        description = {
            "correlation_coefficient": float(correlation),
            "n_points": n_points,
            "interpretation": f"Strong positive correlation" if correlation > 0.7 else "Moderate correlation"
        }
        
        self.queue_manager.publish_progress(job_id, 90, "Creating visualization...")
        time.sleep(0.5)
        
        # Publish plot
        self.queue_manager.publish_plot(job_id, plot_data, description)
        
        self.queue_manager.publish_progress(job_id, 100, "Complete!")
        
        # Store final result
        self.queue_manager.publish_result(job_id, {
            "analysis_type": "correlation",
            "status": "complete",
            **description
        })
    
    async def _start_bootstrap_analysis(self, n_iterations: int):
        """Start bootstrap and return immediately"""
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        
        thread = threading.Thread(
            target=self._run_bootstrap_analysis,
            args=(job_id, n_iterations)
        )
        thread.daemon = True
        thread.start()
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "job_id": job_id,
                "status": "started",
                "message": f"Bootstrap analysis started with {n_iterations} iterations. Monitor job_id: {job_id}"
            }, indent=2)
        )]
    
    def _run_bootstrap_analysis(self, job_id: str, n_iterations: int):
        """Run bootstrap in background"""
        import time
        
        # Simulate data
        data = np.random.randn(100)
        bootstrap_means = []
        
        for i in range(n_iterations):
            if i % 10 == 0:
                progress = (i / n_iterations) * 100
                self.queue_manager.publish_progress(
                    job_id, 
                    progress,
                    f"Bootstrap iteration {i}/{n_iterations}"
                )
            
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_means.append(np.mean(sample))
            
            if i % 100 == 0:
                time.sleep(0.1)
        
        self.queue_manager.publish_progress(job_id, 100, "Complete!")
        
        # Create histogram
        plot_data = {
            "type": "histogram",
            "values": bootstrap_means,
            "title": "Bootstrap Distribution of Means",
            "xlabel": "Sample Mean",
            "ylabel": "Frequency"
        }
        
        description = {
            "mean_of_means": float(np.mean(bootstrap_means)),
            "std_of_means": float(np.std(bootstrap_means)),
            "ci_lower": float(np.percentile(bootstrap_means, 2.5)),
            "ci_upper": float(np.percentile(bootstrap_means, 97.5))
        }
        
        self.queue_manager.publish_plot(job_id, plot_data, description)
        self.queue_manager.publish_result(job_id, {
            "analysis_type": "bootstrap",
            "status": "complete",
            **description
        })
    
    async def _check_job_status(self, job_id: str):
        """Check job status"""
        progress = self.queue_manager.get_current_progress(job_id)
        
        if progress:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "job_id": job_id,
                    "progress": progress["progress"],
                    "message": progress["message"],
                    "status": "complete" if progress["progress"] >= 100 else "running"
                }, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "job_id": job_id,
                    "status": "not_found",
                    "message": "Job not found or not started yet"
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
    server = DataScienceMCPServer()
    asyncio.run(server.run())