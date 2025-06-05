from tools.base import EnhancedBaseTool, FlexibleToolOutput, ToolInput, BaseTool
from pydantic import Field
from typing import Optional, Dict, Any, List
from tools.registry import tool_registry

class ListToolsInput(ToolInput):
    pattern: str = Field(default="*", description="Pattern to match tools (e.g., 'stats.*', 'preprocessing.scale.*')")

class ListToolsTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "meta.discovery.list_tools"
    
    @property
    def name(self) -> str:
        return "list_tools"
    
    @property
    def description(self) -> str:
        return "List available tools by namespace pattern"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return ListToolsInput
    
    def _execute_analysis(self, job_id: str, inputs: ListToolsInput) -> Any:
        """List available tools in a namespace"""
        pattern = inputs.pattern
        tools = tool_registry.discover_tools(pattern)
        
        return {
            "pattern": pattern,
            "tools": tools,
            "count": len(tools)
        }
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        tools = raw_result["tools"]
        
        # Categorize tools better
        tool_info = []
        for tool_name in tools:
            if '.' in tool_name:
                # Enhanced tool with namespace
                category = tool_name.split('.')[0]
            else:
                # Regular tool - infer category from name
                if 'correlation' in tool_name.lower():
                    category = 'stats'
                elif 'bootstrap' in tool_name.lower():
                    category = 'stats'
                elif 'data' in tool_name.lower():
                    category = 'data'
                else:
                    category = 'analysis'
            
            tool_info.append({"tool": tool_name, "category": category})
        
        return FlexibleToolOutput(
            summary={"found": raw_result["count"], "pattern": raw_result["pattern"]},
            tables=tool_info,
            interpretation=f"Found {raw_result['count']} tools matching pattern '{raw_result['pattern']}'"
        )

class SuggestToolInput(ToolInput):
    task: str = Field(description="Description of the task you want to perform")
    data_characteristics: Optional[Dict[str, Any]] = Field(default=None, description="Characteristics of your data")

class SuggestToolTool(EnhancedBaseTool):
    @property
    def namespace(self) -> str:
        return "meta.discovery.suggest_tool"
    
    @property
    def name(self) -> str:
        return "suggest_tool"
    
    @property
    def description(self) -> str:
        return "Get tool recommendations based on your task"
    
    @property
    def input_model(self) -> type[ToolInput]:
        return SuggestToolInput
    
    def _execute_analysis(self, job_id: str, inputs: SuggestToolInput) -> Any:
        """Suggest appropriate tools based on task description and data characteristics"""
        task = inputs.task
        data_characteristics = inputs.data_characteristics or {}
        
        # Get all available tools from registry
        all_tools = tool_registry.discover_tools("*")
        
        # Categorize tools by their capabilities
        tool_categories = {
            "data_exploration": ["get_data_info", "analyze_uploaded_data", "stats.descriptive.summary"],
            "preprocessing": ["preprocessing.scale"],
            "statistical_analysis": ["stats.correlation", "stats.tests", "analyze_correlation", "bootstrap_analysis"],
            "machine_learning": ["models.sklearn"],
            "meta_tools": ["meta.discovery.list_tools", "meta.discovery.suggest_tool"]
        }
        
        # Create comprehensive suggestions based on available tools
        suggestions = []
        
        # Always suggest data exploration first if user seems to be starting
        exploration_keywords = ["analyze", "explore", "understand", "what can", "how to", "help me"]
        if any(keyword in task.lower() for keyword in exploration_keywords):
            suggestions.extend([
                ("get_data_info", "Get an overview of your dataset structure and basic statistics"),
                ("stats.descriptive.summary", "Comprehensive descriptive statistics with visualizations"),
                ("meta.discovery.list_tools", "See all available analysis tools")
            ])
        
        # Statistical analysis suggestions
        stats_keywords = ["correlation", "test", "hypothesis", "statistical", "relationship", "significant"]
        if any(keyword in task.lower() for keyword in stats_keywords):
            suggestions.extend([
                ("stats.correlation", "Analyze correlations between variables"),
                ("stats.tests", "Perform statistical hypothesis tests"),
                ("analyze_correlation", "Create correlation plots and analysis"),
                ("bootstrap_analysis", "Bootstrap sampling for confidence intervals")
            ])
        
        # Machine learning suggestions
        ml_keywords = ["predict", "model", "classify", "cluster", "machine learning", "ml", "train"]
        if any(keyword in task.lower() for keyword in ml_keywords):
            suggestions.extend([
                ("models.sklearn", "Train classification, regression, or clustering models"),
                ("preprocessing.scale", "Scale data before machine learning")
            ])
        
        # Preprocessing suggestions
        prep_keywords = ["scale", "normalize", "preprocess", "clean", "prepare"]
        if any(keyword in task.lower() for keyword in prep_keywords):
            suggestions.extend([
                ("preprocessing.scale", "Scale and normalize your data using various methods")
            ])
        
        # If no specific keywords found, provide general workflow suggestions
        if not suggestions:
            suggestions = [
                ("get_data_info", "Start by understanding your data structure"),
                ("stats.descriptive.summary", "Get comprehensive statistics and distributions"),
                ("stats.correlation", "Explore relationships between variables"),
                ("models.sklearn", "Build predictive models"),
                ("meta.discovery.list_tools", "Browse all available tools")
            ]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for tool, reason in suggestions:
            if tool not in seen and tool in all_tools:  # Only suggest tools that actually exist
                seen.add(tool)
                unique_suggestions.append((tool, reason))
        
        # Limit to top 5 suggestions to avoid overwhelming
        unique_suggestions = unique_suggestions[:5]
        
        return {
            "task": inputs.task,
            "suggestions": unique_suggestions,
            "available_tools": len(all_tools),
            "data_characteristics": data_characteristics
        }
    
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        suggestions = raw_result["suggestions"]
        
        return FlexibleToolOutput(
            summary={"task": raw_result["task"], "n_suggestions": len(suggestions)},
            suggestions=[{"tool": s[0], "reason": s[1]} for s in suggestions],  # Use suggestions field
            interpretation=f"Based on your task, I recommend these {len(suggestions)} tools",
            next_steps=[
                f"Use {s[0]} to {s[1]}" for s in suggestions[:3]
            ]
        )