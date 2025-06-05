# tools/plotting/dispatcher.py
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import time

from core.models import ToolInput
from tools.base import BaseTool


class PlotDispatcherInput(BaseModel):
    """Input for the plotting dispatcher tool"""
    plot_request: str = Field(description="Natural language description of what plot you want (e.g., 'scatter plot of 100 orange random points', 'histogram of data with blue bars and title My Data')")
    use_existing_data: bool = Field(default=False, description="Whether to use existing uploaded data (True) or generate new data (False)")


class PlotDispatcherTool(BaseTool):
    """Intelligent dispatcher that coordinates data generation and plotting based on natural language requests"""
    
    @property
    def name(self) -> str:
        return "plot_dispatcher"
    
    @property
    def description(self) -> str:
        return """Smart plotting dispatcher that understands natural language requests and coordinates the right tools.
        
        Just describe what you want in plain English:
        - "scatter plot of 100 orange random points"
        - "histogram of the data with blue bars and title 'Sales Data'"
        - "line plot with red markers and large size"
        - "bar chart of categories with green color"
        
        The dispatcher will:
        1. Parse your request to extract plot type, data needs, and styling
        2. Generate data if needed, or use existing data
        3. Call the appropriate plotting tool with correct parameters
        4. Handle all the technical coordination for you
        
        Perfect for quick plotting without worrying about tool coordination."""
    
    @property
    def input_model(self) -> type[ToolInput]:
        return PlotDispatcherInput
    
    @property
    def estimated_duration(self) -> float:
        return 5.0  # May need to call multiple tools
    
    def execute(self, job_id: str, inputs: PlotDispatcherInput) -> Dict[str, Any]:
        """Execute the plotting dispatcher"""
        
        # Progress: Start
        self.update_progress(job_id, 0, "Parsing your plotting request...")
        
        try:
            # Parse the natural language request
            parsed = self._parse_plot_request(inputs.plot_request)
            
            self.update_progress(job_id, 20, f"Planning: {parsed['plot_type']} with {len(parsed['parameters'])} styling options...")
            
            # Step 1: Handle data (generate or use existing)
            if not inputs.use_existing_data and parsed.get('needs_data_generation'):
                self.update_progress(job_id, 40, "Generating data...")
                data_result = self._generate_data(parsed['data_params'])
                if 'error' in data_result:
                    return data_result
            
            # Step 2: Create the plot
            self.update_progress(job_id, 70, f"Creating {parsed['plot_type']}...")
            plot_result = self._create_plot(parsed['plot_type'], parsed['parameters'])
            
            if 'error' in plot_result:
                return plot_result
            
            # Complete
            self.update_progress(job_id, 100, "Plot created successfully!")
            
            return {
                "plot_type": parsed['plot_type'],
                "parameters_used": parsed['parameters'],
                "data_generated": not inputs.use_existing_data and parsed.get('needs_data_generation'),
                "message": f"Successfully created {parsed['plot_type']} with your specified styling"
            }
            
        except Exception as e:
            error_msg = f"Error in plot dispatcher: {str(e)}"
            return {"error": error_msg}
    
    def _parse_plot_request(self, request: str) -> Dict[str, Any]:
        """Parse natural language plot request into structured data"""
        request_lower = request.lower()
        
        # Determine plot type
        plot_type = "scatter"  # default
        if any(word in request_lower for word in ["histogram", "hist"]):
            plot_type = "histogram"
        elif any(word in request_lower for word in ["bar chart", "bar plot", "bars"]):
            plot_type = "bar"
        elif any(word in request_lower for word in ["line plot", "line chart", "line"]):
            plot_type = "line"
        elif any(word in request_lower for word in ["scatter", "scatterplot", "points", "dots"]):
            plot_type = "scatter"
        
        # Extract parameters
        parameters = {}
        
        # Colors
        colors = ["red", "blue", "green", "orange", "purple", "yellow", "pink", "brown", "gray", "black"]
        for color in colors:
            if color in request_lower:
                parameters["color"] = color
                break
        
        # Titles (look for patterns like "title 'My Title'" or "call it 'My Title'")
        import re
        title_patterns = [
            r"title ['\"]([^'\"]+)['\"]",
            r"call it ['\"]([^'\"]+)['\"]",
            r"titled ['\"]([^'\"]+)['\"]"
        ]
        for pattern in title_patterns:
            match = re.search(pattern, request_lower)
            if match:
                parameters["title"] = match.group(1)
                break
        
        # Sizes
        if any(word in request_lower for word in ["large", "big"]):
            parameters["marker_size"] = 15
        elif any(word in request_lower for word in ["small", "tiny"]):
            parameters["marker_size"] = 5
        
        # Data generation parameters
        data_params = {}
        needs_data_generation = False
        
        # Check if they want generated data
        if any(word in request_lower for word in ["random", "generate", "synthetic", "sample"]):
            needs_data_generation = True
            data_params["data_type"] = plot_type if plot_type != "bar" else "categorical"
            
            # Extract number of points
            import re
            numbers = re.findall(r'\b(\d+)\b', request)
            if numbers:
                data_params["n_points"] = int(numbers[0])
            else:
                data_params["n_points"] = 100  # default
        
        return {
            "plot_type": plot_type,
            "parameters": parameters,
            "data_params": data_params,
            "needs_data_generation": needs_data_generation
        }
    
    def _generate_data(self, data_params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate data using the data generation tool"""
        from tools.data_generation import DataGenerationTool, DataGenerationInput
        
        # Create and execute data generation tool directly
        data_tool = DataGenerationTool(self.job_manager, self.message_bus)
        
        # Convert params to input model
        data_input = DataGenerationInput(**data_params)
        
        # Execute directly without creating sub-jobs
        result = data_tool.execute("temp_data_job", data_input)
        
        return result
    
    def _create_plot(self, plot_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Create plot using the appropriate plotting tool"""
        
        # Map plot types to tools
        tool_mapping = {
            "scatter": ("plotting_basic_scatter", "tools.plotting.basic.scatter", "ScatterPlotTool"),
            "histogram": ("plotting_basic_histogram", "tools.plotting.basic.histogram", "HistogramPlotTool"),
            "bar": ("plotting_basic_bar", "tools.plotting.basic.bar", "BarPlotTool"),
            "line": ("plotting_basic_line", "tools.plotting.basic.line", "LinePlotTool")
        }
        
        if plot_type not in tool_mapping:
            return {"error": f"Unsupported plot type: {plot_type}"}
        
        tool_name, module_path, class_name = tool_mapping[plot_type]
        
        # For now, only scatter plot is implemented
        if plot_type == "scatter":
            from tools.plotting.basic.scatter import ScatterPlotTool, ScatterPlotInput
            
            # Create plotting tool directly
            plot_tool = ScatterPlotTool(self.job_manager, self.message_bus)
            
            # Convert parameters to input model with proper parameter mapping
            plot_params = {
                "x": "x",  # default column names from data generation
                "y": "y",
            }
            
            # Map dispatcher parameters to scatter plot parameters
            if "color" in parameters:
                plot_params["color"] = parameters["color"]
            
            if "title" in parameters:
                plot_params["title"] = parameters["title"]
            
            if "marker_size" in parameters:
                plot_params["marker_size"] = parameters["marker_size"]
            
            # Add any other parameters that match directly
            for key, value in parameters.items():
                if key not in ["color", "title", "marker_size"] and value is not None:
                    plot_params[key] = value
            
            try:
                plot_input = ScatterPlotInput(**plot_params)
                
                # Execute directly without creating sub-jobs
                result = plot_tool.execute("temp_plot_job", plot_input)
                
                return result
            except Exception as e:
                return {"error": f"Error creating scatter plot input: {str(e)}"}
        else:
            return {"error": f"Plot type '{plot_type}' not yet implemented in dispatcher"} 