from typing import Dict, Any
from core.message_bus import MessageBus
from core.job_manager import JobManager

# Import all necessary tool CLASSES
from .data_tools import GetDataInfoTool, AnalyzeUploadedDataTool
# Correcting the import path for enhanced tools
from .implementations.sklearn_tools import PreprocessingScaleTool, ModelTool, StatisticalTestsTool, CorrelationAnalysisTool
from .data_generation import DataGenerationTool
from .code_tools import CodeGeneratorTool, CodeExecutorTool
from .plot_editor import EditPlotTool
from .animation_tools import AnimationFrameTool, RealTimeAnimationTool, BoidsSimulationTool
# We will temporarily disable the function-based tools to ensure stability
# from .plotting.tools import plotting_suggest, plotting_edit

# Import all dynamically generated plotting tools
from .plotting.generated_tools import *

# Import all dynamically generated statistical tools
# Temporarily disabled due to dependency issues
# try:
#     from .statistical.generated_tools import *
# except ImportError:
#     print("⚠️ Statistical tools not available - run statistical tool generator first")
#     pass

def create_all_tools(job_manager: JobManager, message_bus: MessageBus, llm: Any) -> Dict[str, Any]:
    """
    Create and return all available tools as a dictionary.
    This function instantiates all the class-based tools and registers them.
    """
    tools: Dict[str, Any] = {}

    # --- List of all tool classes to be instantiated ---
    # Start with the standard, non-plotting tools
    tool_classes = [
        GetDataInfoTool,
        AnalyzeUploadedDataTool,
        PreprocessingScaleTool,
        ModelTool,
        StatisticalTestsTool,
        CorrelationAnalysisTool,
        DataGenerationTool,
        CodeGeneratorTool,
        CodeExecutorTool,
        EditPlotTool,
        AnimationFrameTool,
        RealTimeAnimationTool,
        BoidsSimulationTool
    ]

    # Dynamically add all the generated plotting tools
    # This assumes they are all loaded into the current scope via the wildcard import
    for name, obj in globals().items():
        if name.startswith("Plotly") and name.endswith("Tool"):
            tool_classes.append(obj)
    
    # Dynamically add all the generated statistical tools
    # Temporarily disabled due to dependency issues
    # for name, obj in globals().items():
    #     if name.startswith("Stats") and name.endswith("Tool"):
    #         tool_classes.append(obj)

    # --- Instantiate and register each tool ---
    for tool_class in tool_classes:
        try:
            # Pass the LLM instance to all tools; they will only use it if they need it
            instance = tool_class(job_manager, message_bus, llm=llm)
            # Use the tool's self-declared name as the key
            if hasattr(instance, 'name'):
                tools[instance.name] = instance
            else:
                print(f"⚠️ Warning: Tool {tool_class.__name__} has no 'name' attribute and will be skipped.")
        except Exception as e:
            print(f"🔥 Failed to instantiate tool {tool_class.__name__}: {e}")


    # --- Handle remaining function-based tools (if any) ---
    # For now, we are disabling these to solve the crash.
    # function_based_tools = {
    #     "plotting_suggest": plotting_suggest,
    #     "plotting_edit": plotting_edit,
    # }
    # tools.update(function_based_tools)

    print(f"✓ Created {len(tools)} tools: {list(tools.keys())}")
    return tools