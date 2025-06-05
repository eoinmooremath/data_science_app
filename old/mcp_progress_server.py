# mcp_progress_server.py
import asyncio
import json
import time
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Shared progress state (in production, use proper IPC)
PROGRESS_FILE = "/tmp/mcp_progress.json"

class ProgressMCPServer:
    def __init__(self):
        self.server = Server("progress-test-server")
        
    async def list_tools_handler(self):
        return [
            Tool(
                name="compute_fibonacci",
                description="Compute large Fibonacci numbers (slow operation)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "n": {"type": "integer", "description": "Which Fibonacci number to compute"}
                    },
                    "required": ["n"]
                }
            ),
            Tool(
                name="matrix_multiplication",
                description="Multiply large random matrices (slow operation)",
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "size": {"type": "integer", "description": "Matrix dimension (size x size)"}
                    },
                    "required": ["size"]
                }
            )
        ]
    
    async def call_tool_handler(self, name: str, arguments: dict):
        if name == "compute_fibonacci":
            return await self._compute_fibonacci(arguments["n"])
        elif name == "matrix_multiplication":
            return await self._matrix_multiplication(arguments["size"])

    async def _compute_fibonacci(self, n: int):
        """Compute Fibonacci with progress updates"""
        # Reset progress
        self._update_progress(0, f"Starting Fibonacci({n})")
        
        # Make it slower so we can see real progress
        n = min(n, 50)  # Lower limit
        
        if n <= 1:
            self._update_progress(100, "Complete")
            return [TextContent(
                type="text",
                text=json.dumps({"fibonacci_number": n, "result": n})
            )]
        
        a, b = 0, 1
        for i in range(2, n + 1):
            a, b = b, a + b
            
            # Update progress for EVERY iteration with delay
            progress = (i / n) * 100
            self._update_progress(progress, f"Computing F({i}) = {b}")
            
            # Deliberate delay so you can watch progress
            await asyncio.sleep(0.2)  # 200ms per iteration
        
        self._update_progress(100, f"Complete! F({n}) = {b}")
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "fibonacci_number": n,
                "result": b,
                "computation_time": f"{n * 0.2:.1f} seconds"
            })
        )]

    async def _matrix_multiplication(self, size: int):
        """Matrix multiplication with progress"""
        import numpy as np
        
        # Limit size for demo
        size = min(size, 1000)
        
        self._update_progress(0, f"Creating {size}x{size} matrices")
        
        A = np.random.rand(size, size)
        B = np.random.rand(size, size)
        
        self._update_progress(20, "Starting multiplication")
        
        # Chunked multiplication to show progress
        result = np.zeros((size, size))
        chunk_size = max(1, size // 10)
        
        for i in range(0, size, chunk_size):
            end_i = min(i + chunk_size, size)
            for j in range(0, size, chunk_size):
                end_j = min(j + chunk_size, size)
                
                # Compute chunk
                result[i:end_i, j:end_j] = A[i:end_i, :] @ B[:, j:end_j]
                
                # Update progress
                progress = 20 + (i * size + j) / (size * size) * 80
                self._update_progress(progress, f"Processing chunk ({i},{j})")
                
                # Simulate slower computation
                await asyncio.sleep(0.1)
        
        self._update_progress(100, "Complete")
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "matrix_size": f"{size}x{size}",
                "result_sum": float(np.sum(result)),
                "result_mean": float(np.mean(result))
            })
        )]
    
    def _update_progress(self, percent: float, message: str):
        """Write progress to shared file"""
        # For Windows, use temp directory
        import tempfile
        import os
        
        progress_file = os.path.join(tempfile.gettempdir(), 'mcp_progress.json')
        
        with open(progress_file, 'w') as f:
            json.dump({
                "progress": percent,
                "message": message,
                "timestamp": time.time()
            }, f)
    
    async def run(self):
        # Initialize progress file
        self._update_progress(0, "Ready")
        
        # Register handlers using the @server decorator pattern
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
    server = ProgressMCPServer()
    asyncio.run(server.run())