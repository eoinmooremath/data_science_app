import os
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import queue
import threading
from langchain_anthropic import ChatAnthropic
import logging

from llm.langchain_agent import create_langchain_agent, DataScienceAgent
from core.job_manager import JobManager
from core.message_bus import MessageBus, Message, MessageType


class LLMClient:
    """LangChain-powered LLM client for data science operations"""
    
    def __init__(self, job_manager: JobManager, message_bus: MessageBus):
        self.job_manager = job_manager
        self.message_bus = message_bus
        
        # Instantiate the LLM here, making it available immediately
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.1,
            max_tokens=4000
        )
        
        self.agent: Optional[DataScienceAgent] = None
        self.tools: Dict[str, Any] = {}
        self.request_thread = None
        self.message_queue = queue.Queue()
        self.stop_event = threading.Event()
        
        print("✓ LangChain LLM client initialized")
    
    def start(self):
        """Start the background processing thread after the app is configured."""
        if not self.request_thread:
            self._start_processing_thread()
            logging.info("LLMClient background thread started.")
    
    def register_tools(self, tools: Dict[str, Any]):
        """Register tools with the LangChain agent"""
        self.tools = tools
        
        # Create the LangChain agent with all tools, passing the llm
        self.agent = create_langchain_agent(
            job_manager=self.job_manager,
            message_bus=self.message_bus,
            tools_registry=self.tools,
            llm=self.llm
        )
        
        print(f"🤖 LangChain agent created with {len(self.tools)} tools")
    
    def _start_processing_thread(self):
        """Start the background thread that processes messages from the queue."""
        self.request_thread = threading.Thread(
            target=self.process_request_thread,
            daemon=True
        )
        self.request_thread.start()

    def process_request_thread(self):
        """The target function for the background processing thread."""
        while not self.stop_event.is_set():
            try:
                # Wait for a message to appear in the queue
                message, user_id, job_id = self.message_queue.get(timeout=1)
                
                print(f"🧵 Dequeued message for job {job_id}: '{message[:50]}...'")
                
                # Use a synchronous-friendly method to call the async agent
                result = self.process_message_sync(message, user_id)
                
                # Use the message bus to notify that the job is done
                self.message_bus.publish(
                    MessageType.JOB_STATUS,
                    job_id=job_id,
                    data={"status": "completed", "result": result}
                )
                self.message_queue.task_done()

            except queue.Empty:
                # This is expected when the queue is empty
                continue
            except Exception as e:
                logging.error(f"❌ Error in LLM processing thread: {e}", exc_info=True)
                # Optionally, publish an error status
                if 'job_id' in locals():
                    self.message_bus.publish(
                        MessageType.JOB_STATUS,
                        job_id=job_id,
                        data={"status": "failed", "error": str(e)}
                    )

    async def process_message(self, message: str, user_id: str = "default", job_id_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process a user message through the LangChain agent"""
        if not self.agent:
            return {
                "response": "❌ Agent not initialized. Please register tools first.",
                "success": False,
                "error": "Agent not initialized"
            }
        
        try:
            print(f"🎯 Processing message via LangChain: {message[:100]}...")
            
            # This is a bit of a placeholder; in a real scenario, the agent would create jobs.
            # For now, we'll just create a dummy job to track the LLM call.
            job = self.job_manager.create_job(tool_name="langchain_agent")
            if job_id_callback:
                job_id_callback(job.id)

            # Process through LangChain agent
            result = await self.agent.process_message(message, user_id)
            
            self.job_manager.complete_job(job.id, result)

            print(f"✅ LangChain processing complete: {result.get('success', False)}")
            return result
            
        except Exception as e:
            print(f"❌ LangChain client error: {str(e)}")
            if 'job' in locals() and job:
                self.job_manager.fail_job(job.id, str(e))
            return {
                "response": f"I encountered an error processing your request: {str(e)}",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def process_message_sync(self, message: str, user_id: str = "default", job_id_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Synchronous wrapper for async message processing"""
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self._run_in_new_loop, message, user_id, job_id_callback)
                        return future.result(timeout=120)
                else:
                    return loop.run_until_complete(self.process_message(message, user_id, job_id_callback))
            except RuntimeError:
                return asyncio.run(self.process_message(message, user_id, job_id_callback))
                
        except Exception as e:
            print(f"❌ Sync wrapper error: {str(e)}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _run_in_new_loop(self, message: str, user_id: str, job_id_callback: Optional[Callable]) -> Dict[str, Any]:
        """Run async code in a new event loop (for thread execution)"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.process_message(message, user_id, job_id_callback))
        finally:
            loop.close()

    def process_message_in_background(self, message: str, user_id: str, job_id: str):
        """Queue a message for the agent to process in the background."""
        self.message_queue.put((message, user_id, job_id))

    def stop(self):
        """Stop the background processing thread."""
        self.stop_event.set()
        if self.request_thread:
            self.request_thread.join()
    
    def clear_conversation_history(self):
        """Clear the agent's conversation memory"""
        if self.agent:
            self.agent.clear_memory()
            print("🧹 Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history"""
        if not self.agent:
            return []
        
        messages = self.agent.get_conversation_history()
        return [
            {
                "role": "human" if msg.type == "human" else "assistant",
                "content": msg.content,
                "timestamp": getattr(msg, 'timestamp', None)
            }
            for msg in messages
        ]
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        if tool_name not in self.tools:
            return None
        
        tool = self.tools[tool_name]
        return {
            "name": tool_name,
            "description": getattr(tool, 'description', 'No description available'),
            "doc": getattr(tool, '__doc__', None)
        }