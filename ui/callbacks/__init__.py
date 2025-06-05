# ui/callbacks/__init__.py
from dash import Dash
from core.message_bus import MessageBus
from core.job_manager import JobManager
from llm.client import LLMClient
from ui.state import UIStateManager
from typing import List, Optional, Dict, Any
from core.models import MessageType
from tools.base import BaseTool

from .chat_callbacks import register_chat_callbacks
from .progress_callbacks import register_progress_callbacks
from .plot_callbacks import register_plot_callbacks
from .file_callbacks import register_file_callbacks
from .results_callbacks import register_results_callbacks

def register_all_callbacks(
    app: Dash,
    message_bus: MessageBus,
    job_manager: JobManager,
    llm_client: Optional[LLMClient],
    ui_state: UIStateManager,
    tools: List
):
    """Register all application callbacks"""
    
    # Register UI callbacks first (this creates the plot_history)
    register_chat_callbacks(app, llm_client, ui_state)
    register_progress_callbacks(app, ui_state)
    register_plot_callbacks(app, ui_state)
    register_file_callbacks(app)
    register_results_callbacks(app, ui_state)
    
    # Register message bus subscriptions after callbacks (so app.plot_history exists)
    register_message_subscriptions(app, message_bus, ui_state, job_manager, tools, llm_client)

# ui/callbacks/__init__.py - Enhanced message handling
def register_message_subscriptions(app: Dash, message_bus: MessageBus, ui_state: UIStateManager, job_manager: JobManager, tools: List[BaseTool], llm_client: Optional[LLMClient] = None):
    """Register message bus subscriptions"""
    
    # Create tool lookup
    tool_lookup = {tool.name: tool for tool in tools}
    # Add namespace lookup for enhanced tools
    for tool in tools:
        if hasattr(tool, 'namespace'):
            tool_lookup[tool.namespace] = tool

    def handle_progress(msg):
        ui_state.update_job_progress(msg.job_id, msg.data["progress"], msg.data["message"])
    
    def handle_plot(msg):
        ui_state.update_job_plot(msg.job_id, msg.data)
        # Use the app's plot history instead of module-level
        if hasattr(app, 'plot_history'):
            app.plot_history.add_plot(msg.data, msg.job_id)  # Fixed parameter order
        else:
            print("⚠️ Warning: app.plot_history not found")
    
    def handle_result(msg):
        ui_state.update_job_result(msg.job_id, msg.data)
        job = job_manager.get_job(msg.job_id)
        if job:
            ui_state.add_result(msg.job_id, job.tool_name, msg.data)
            
            # Get the tool instance
            tool = tool_lookup.get(job.tool_name)
            
            # Add result summary to chat with tool reference
            result_summary = format_result_summary(job.tool_name, msg.data, tool)
            ui_state.add_chat_message(
                "assistant",
                result_summary,
                msg.job_id
            )
            
            # For suggest_tool, trigger a follow-up LLM response
            if job.tool_name == "suggest_tool" and llm_client:
                # Extract suggestions from the FlexibleToolOutput format
                suggestions = msg.data.get('suggestions', [])  # Now properly in 'suggestions' field
                if suggestions:
                    # Create a conversational follow-up message
                    # suggestions is now a list of dicts with 'tool' and 'reason' keys
                    suggestion_text = "\n".join([f"• **{s['tool']}** - {s['reason']}" for s in suggestions])
                    
                    follow_up_message = f"""Perfect! Based on your request, here are my top recommendations:

{suggestion_text}

Which of these would you like to start with? I can run any of these analyses for you right now. Just let me know which one interests you most, or if you'd like me to explain any of them in more detail!"""
                    
                    # Add the follow-up message directly
                    ui_state.add_chat_message("assistant", follow_up_message)
    
    message_bus.subscribe(MessageType.PROGRESS, handle_progress)
    message_bus.subscribe(MessageType.PLOT, handle_plot)
    message_bus.subscribe(MessageType.RESULT, handle_result)

# ui/callbacks/__init__.py - Update the result handler
def format_result_summary(tool_name: str, results: Dict[str, Any], tool: Optional[BaseTool] = None) -> str:
    """Format results for chat display"""
    
    # Check if it's an enhanced tool with flexible output
    if tool and hasattr(tool, 'namespace'):
        from prompts.response_templates import ResponseTemplates
        return f"✅ **{tool.namespace} Complete!**\n\n" + ResponseTemplates.format_flexible_output(tool.namespace, results)
    
    # Fall back to existing formatting for standard tools
    if tool_name == "analyze_correlation":
        corr = results.get("correlation_coefficient", 0)
        n_points = results.get("n_points", 0)
        return f"""✅ **Correlation Analysis Complete!**

The correlation coefficient is **{corr:.3f}**, indicating a {'strong' if abs(corr) > 0.7 else 'moderate' if abs(corr) > 0.4 else 'weak'} {'positive' if corr > 0 else 'negative'} relationship.

Based on this result, you might want to:
- {'Run a regression analysis to model this relationship' if abs(corr) > 0.4 else 'Explore other variables for stronger relationships'}
- Check for non-linear patterns in the scatter plot
- Test if this correlation is statistically significant"""
    
    elif tool_name == "get_data_info":
        shape = results.get("shape", "unknown")
        numeric_cols = results.get("numeric_columns", [])
        return f"""✅ **Data Overview Complete!**

Your dataset has **{shape}** with {len(numeric_cols)} numeric columns available for analysis.

Here are some analyses I can help with:
- Statistical summary of all columns
- Correlation matrix to find relationships
- Distribution plots to understand your data
- Missing value analysis

What would you like to explore first?"""
    
    # Generic format for other tools
    return f"✅ Analysis complete! Check the results panel for details."
