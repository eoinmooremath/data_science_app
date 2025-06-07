# ui/callbacks/__init__.py
from dash import Dash, Input, Output, State, no_update
from core.message_bus import MessageBus
from core.job_manager import JobManager
from llm.client import LLMClient
from ui.state import UIStateManager
from typing import List, Optional, Dict, Any
from core.models import MessageType
from tools.base import BaseTool
import logging

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
    
    register_chat_callbacks(app, llm_client, ui_state)
    register_progress_callbacks(app, ui_state)
    register_plot_callbacks(app, ui_state)
    register_file_callbacks(app)
    register_results_callbacks(app, ui_state)
    
    # This is the new central callback for processing messages from the bus
    @app.callback(
        Output("message-trigger", "data"), # Dummy output to trigger the callback
        Input("update-interval", "n_intervals"),
        prevent_initial_call=True
    )
    def process_message_queue(n_intervals):
        messages = message_bus.get_all_messages()
        if not messages:
            return no_update

        tool_lookup = {tool.name: tool for tool in tools}

        for msg in messages:
            try:
                if msg.type == MessageType.PROGRESS:
                    logging.info(f"UI handling PROGRESS: {msg.job_id} - {msg.data['progress']}%")
                    ui_state.update_job_progress(msg.job_id, msg.data["progress"], msg.data["message"])
                
                elif msg.type == MessageType.RESULT:
                    logging.info(f"UI handling RESULT for job: {msg.job_id}")
                    ui_state.update_job_progress(msg.job_id, 100, "Completed")
                    
                    job = job_manager.get_job(msg.job_id)
                    if job:
                        # Silently add the result to the ledger without creating a chat message
                        ui_state.add_result(msg.job_id, job.tool_name, msg.data)
                
                elif msg.type == MessageType.ERROR:
                     logging.error(f"UI handling ERROR for job: {msg.job_id} - {msg.data.get('error')}")
                     ui_state.update_job_progress(msg.job_id, 100, f"Failed: {msg.data.get('error')}")

            except Exception as e:
                logging.error(f"Error processing message in UI callback: {e}", exc_info=True)
        
        # Return a value to indicate the trigger has fired
        return n_intervals

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
    return f"✅ Analysis '{tool_name}' complete! Check the results panel for details."
