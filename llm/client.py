from typing import List, Dict, Any, Optional
from anthropic import Anthropic
import os
from core.models import Job
from core.job_manager import JobManager
from tools.base import BaseTool
from prompts import get_system_prompt, get_tool_context, get_conversation_guidelines
from prompts.response_templates import ResponseTemplates
import json

class LLMClient:
    """Enhanced client for conversational interactions"""
    
    def __init__(self, job_manager: JobManager, tools: List[BaseTool]):
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.job_manager = job_manager
        self.tools = {tool.name: tool for tool in tools}
        self.tools_schema = [tool.get_schema() for tool in tools]
        self.templates = ResponseTemplates()
        
        # Build enhanced system prompt
        self.system_prompt = f"""{get_system_prompt()}

{get_tool_context(tools)}

{get_conversation_guidelines()}

Always be helpful, educational, and suggest next steps based on the results."""
    
    def process_message(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Process a message with enhanced context"""
        
        try:
            # Call Claude with enhanced context - system prompt goes as separate parameter
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                temperature=0.3,  # Slightly more creative
                system=self.system_prompt,  # System prompt as separate parameter
                messages=messages,
                tools=self.tools_schema
            )
            
            # Process response...
            if response.stop_reason == "tool_use":
                # Get the full response text AND all tool uses
                response_text = ""
                tool_uses = []
                
                for block in response.content:
                    if hasattr(block, 'text'):
                        response_text = block.text
                    elif hasattr(block, 'name'):
                        tool_uses.append(block)
                
                if tool_uses:
                    # Handle multiple tool calls
                    job_ids = []
                    tool_names = []
                    
                    for tool_use in tool_uses:
                        tool = self.tools.get(tool_use.name)
                        if tool:
                            try:
                                job = self.job_manager.create_job(tool_use.name)
                                tool.execute_async(job, tool_use.input)
                                job_ids.append(job.id)
                                tool_names.append(tool_use.name)
                            except Exception as e:
                                return {
                                    "type": "error",
                                    "message": f"I encountered an error while trying to run {tool_use.name}: {str(e)}. Let me try a different approach."
                                }
                    
                    # Create response message for multiple tools
                    if len(job_ids) == 1:
                        # Single tool call
                        full_message = response_text
                        if full_message:
                            full_message += f"\n\n*(Job ID: {job_ids[0]})*"
                        else:
                            full_message = f"Starting {tool_names[0]} analysis (Job ID: {job_ids[0]})"
                        
                        return {
                            "type": "tool_use",
                            "job_id": job_ids[0],
                            "tool_name": tool_names[0],
                            "message": full_message
                        }
                    else:
                        # Multiple tool calls
                        job_list = ", ".join([f"{name} ({job_id})" for name, job_id in zip(tool_names, job_ids)])
                        full_message = response_text
                        if full_message:
                            full_message += f"\n\n*Running: {job_list}*"
                        else:
                            full_message = f"Running multiple analyses: {job_list}"
                        
                        return {
                            "type": "tool_use_multiple",
                            "job_ids": job_ids,
                            "tool_names": tool_names,
                            "message": full_message
                        }
            
            # Regular response
            return {
                "type": "message",
                "message": response.content[0].text if response.content else "I'm not sure how to respond to that."
            }
            
        except Exception as e:
            return {
                "type": "error",
                "message": f"I'm having trouble processing that request. Could you try rephrasing it? (Error: {str(e)})"
            }