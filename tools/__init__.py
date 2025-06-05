from typing import List
from core.message_bus import MessageBus
from core.job_manager import JobManager
from tools.base import BaseTool
from tools.registry import tool_registry

# Import existing tools
from tools.statistics import CorrelationTool, BootstrapTool
from tools.data_tools import GetDataInfoTool, AnalyzeUploadedDataTool
# Removed test tools - using proper plotting tools instead

# Import new enhanced tools
from tools.implementations.stats_descriptive import DescriptiveStatsTool
from tools.implementations.meta_tools import ListToolsTool, SuggestToolTool
from tools.implementations.sklearn_tools import (
    PreprocessingScaleTool, ModelTool, StatisticalTestsTool, CorrelationAnalysisTool
)

# Import plotting tools
from tools.plotting import PlotSuggestionTool, PlotEditTool
from tools.plotting.basic import ScatterPlotTool

# Import data generation tool
from tools.data_generation import DataGenerationTool



def create_all_tools(job_manager: JobManager, message_bus: MessageBus) -> List[BaseTool]:
    """Create and return all available tools"""
    
    # Create tool instances
    tools = [
        # Existing tools
        CorrelationTool(job_manager, message_bus),
        BootstrapTool(job_manager, message_bus),
        GetDataInfoTool(job_manager, message_bus),
        AnalyzeUploadedDataTool(job_manager, message_bus),
        # Removed test tool - using proper plotting tools instead
        
        # New enhanced tools
        DescriptiveStatsTool(job_manager, message_bus),
        ListToolsTool(job_manager, message_bus),
        SuggestToolTool(job_manager, message_bus),
        
        # Sklearn and statsmodels tools
        PreprocessingScaleTool(job_manager, message_bus),
        ModelTool(job_manager, message_bus),
        StatisticalTestsTool(job_manager, message_bus),
        CorrelationAnalysisTool(job_manager, message_bus),
        
        # Plotting tools
        PlotSuggestionTool(job_manager, message_bus),
        PlotEditTool(job_manager, message_bus),
        ScatterPlotTool(job_manager, message_bus),
        
        # Data generation tool
        DataGenerationTool(job_manager, message_bus),
    ]
    
    # Register ALL tools with the registry (both enhanced and regular)
    for tool in tools:
        if hasattr(tool, 'namespace'):  # It's an EnhancedBaseTool
            tool_registry.register_tool(type(tool))
        else:  # It's a regular BaseTool
            tool_registry.register_regular_tool(tool)
    
    # Auto-discover more tools if available
    tool_registry.auto_discover_and_register("tools.implementations")
    
    return tools