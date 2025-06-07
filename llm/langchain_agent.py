"""
LangChain Agent for Data Science UI

This module implements a LangChain-based agent that can automatically:
1. Decide which tools to use based on user requests
2. Chain multiple tools together for complex workflows
3. Handle errors and retry with alternative approaches
4. Maintain conversation memory and context
"""

import os
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain_anthropic import ChatAnthropic
from langchain.tools import BaseTool
from langchain.schema import BaseMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import TypedDict
from langchain_core.language_models import BaseLanguageModel

from core.job_manager import JobManager
from core.message_bus import MessageBus

# Define a TypedDict for the agent's state, which is hashable
class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_scratchpad: list[BaseMessage]

class DataScienceAgent:
    """LangChain agent for data science operations"""
    
    def __init__(self, job_manager: JobManager, message_bus: MessageBus, llm: BaseLanguageModel):
        self.job_manager = job_manager
        self.message_bus = message_bus
        
        # Use the provided LLM instance
        self.llm = llm
        
        # Conversation memory
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Keep last 10 exchanges
        )
        
        # Tools will be registered here
        self.tools = []
        self.agent_executor = None
        
        print("🤖 LangChain DataScienceAgent initialized")
    
    def register_tool(self, tool: BaseTool):
        """Register a tool with the agent"""
        self.tools.append(tool)
        print(f"🔧 Registered tool: {tool.name}")
    
    def setup_agent(self):
        """Setup the agent executor with tools and prompts"""
        if not self.tools:
            raise ValueError("No tools registered. Register tools before setting up agent.")
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        ).with_types(input_type=AgentState)
        
        print(f"🚀 Agent executor setup complete with {len(self.tools)} tools")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are a personal data scientist assistant with access to powerful statistical and visualization tools.

Your role is to:
1. **Understand user requests** and break them down into actionable steps
2. **Automatically coordinate multiple tools** to complete complex workflows
3. **Generate data when needed** for demonstrations or analysis
4. **Create visualizations** with appropriate styling and parameters
5. **Perform statistical analysis** and provide insights
6. **Handle errors gracefully** and try alternative approaches

Key Capabilities:
- **Data Generation**: Create synthetic datasets for analysis and visualization
- **Statistical Analysis**: Descriptive statistics, correlations, hypothesis testing
- **Visualization**: Interactive plots with intelligent parameter handling
- **Plot Editing**: Modify existing plots with new styling or data
- **Code Generation & Execution**: Generate and execute Python code for custom tasks using a two-step process:
  1. `code_generator`: Takes a natural language query and creates a Python script.
  2. `code_executor`: Executes the script that was just created.

Tool Coordination Guidelines:
- For requests like "draw me a graph of 100 orange random points":
  1. Use `DataGenerationTool` to create scatter data (n_points=100)
  2. Use `ScatterPlotTool` with color="orange"
- For complex analysis requests, chain multiple statistical tools
- Always provide context and insights, not just raw results
- When editing plots, use the plot editing tools to modify existing visualizations

Parameter Intelligence:
- Colors: "orange", "red", "#FF0000" → direct color values
- Sizes: "large dots" → marker_size=15, "small" → marker_size=5
- Data: "random points" → generate synthetic data first
- Styling: Extract visual preferences from natural language

Using the Code Tools:
- When a user asks for a specific data generation or manipulation that is not covered by other tools, you must use the two-step code generation process.
- **Step 1: Generate Code.** Call the `code_generator` tool with a detailed query describing the task. This tool will return a file path.
- **Step 2: Execute Code.** Call the `code_executor` tool with the `file_path` you received from the previous step.
- To make data from your script available to other tools (like plotting), you MUST save the resulting pandas DataFrame into the `uploaded_datasets` dictionary, which is globally accessible.
- Example of saving data within a generated script:
  ```python
  import pandas as pd
  import numpy as np
  from tools.data_tools import uploaded_datasets

  # Your data generation logic
  data = {{'col1': np.random.random(10), 'col2': np.random.random(10)}}
  df = pd.DataFrame(data)

  # Save to the shared data store
  dataset_id = 'my_custom_data'
  uploaded_datasets[dataset_id] = df
  ```
  
Using Data Tools:
- When you use `generate_data`, it will return a unique `dataset_id`.
- To use that data in another tool (like `plotting_scatter`), you MUST pass that exact `dataset_id` to it.
- Example Workflow:
  1. User: "Generate 100 data points"
  2. Agent calls `generate_data`. It returns `{{"dataset_id": "job_1234"}}`.
  3. User: "Now plot it."
  4. Agent calls `plotting_scatter` with `dataset_id="job_1234"`.

Remember: You have full autonomy to decide which tools to use and in what order. Be proactive and intelligent about tool coordination.

Code Generation Workflow:
- **NEVER** make up file paths.
- **Step 1: Generate Code.** Call `code_generator` with a `query`. It will return a result like: `{{'success': True, 'file_path': 'temp_code\\generated_code_xyz.py'}}`
- **Step 2: Execute Code.** Call `code_executor` using the *exact* `file_path` from the previous step's result.

Remember: You have full autonomy to decide which tools to use and in what order. Be proactive and intelligent about tool coordination."""

    async def process_message(self, message: str, user_id: str = "default", job_id_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process a user message through the LangChain agent"""
        if not self.agent_executor:
            raise ValueError("Agent not setup. Call setup_agent() first.")
        
        try:
            print(f"🎯 Processing message: {message[:100]}...")
            
            # Run the agent
            result = await self.agent_executor.ainvoke({
                "input": message,
                "chat_history": self.memory.chat_memory.messages
            })
            
            # Extract the response text, handling different possible output formats
            output = result.get("output")
            response_text = ""
            if isinstance(output, str):
                response_text = output
            elif isinstance(output, list) and output:
                # Handle cases where output is like [{'text': '...'}]
                first_item = output[0]
                if isinstance(first_item, dict) and 'text' in first_item:
                    response_text = first_item.get('text', 'Could not parse response.')
            
            if not response_text:
                 response_text = "I encountered an issue processing your request."

            # Get any intermediate steps for debugging
            intermediate_steps = result.get("intermediate_steps", [])
            
            return {
                "response": response_text,
                "success": True,
                "intermediate_steps": len(intermediate_steps),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Agent error: {str(e)}")
            return {
                "response": f"I encountered an error: {str(e)}. Please try rephrasing your request.",
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
        print("🧹 Agent memory cleared")
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the current conversation history"""
        return self.memory.chat_memory.messages

    async def _arun(self, **kwargs) -> str:
        # For now, we'll just call the sync version.
        # Ideally, this would be a truly async implementation.
        return self._run(**kwargs)


class LangChainToolWrapper(BaseTool):
    """Wrapper to convert our existing tools to LangChain tools"""
    
    name: str = Field(...)
    description: str = Field(...)
    tool_instance: Any = Field(...)
    job_manager: JobManager = Field(...)
    message_bus: MessageBus = Field(...)
    
    class Config:
        arbitrary_types_allowed = True
    
    def _run(self, **kwargs) -> str:
        """
        Executes the tool synchronously, handling parameter validation
        and providing clear error feedback to the agent to enable self-correction.
        """
        job_id = None
        tool_name = self.name
        try:
            actual_params = kwargs.get('kwargs', kwargs)
            if not isinstance(actual_params, dict):
                actual_params = {}

            print(f"\n[DEBUG] Tool: {tool_name}")
            print(f"[DEBUG] Params: {actual_params}")
            print(f"[DEBUG] Tool instance: {self.tool_instance}")
            
            tool_class = type(self.tool_instance)
            
            print(f"[DEBUG] Tool class: {tool_class}")

            if not hasattr(tool_class, 'input_model'):
                raise TypeError(f"Tool '{tool_name}' is not a valid class-based tool with an input model.")

            input_model = tool_class.input_model
            print(f"[DEBUG] Tool input_model: {input_model}")

            try:
                # Validate parameters using the tool's input_model
                validated_inputs = input_model(**actual_params)
            except ValidationError as e:
                print(f"[DEBUG] ValidationError: {e}")
                import traceback
                traceback.print_exc()
                # Provide a more helpful error message to the LLM
                return f"❌ Invalid parameters for tool '{tool_name}'.\nError: {e}\nSchema: {input_model.schema_json(indent=2)}"
            
            # If validation is successful, proceed to create and execute the job
            job = self.job_manager.create_job(tool_name=tool_name)
            job_id = job.id
            
            try:
                # The tool's execute method should handle the job_id and validated inputs
                result = self.tool_instance.execute(job_id=job_id, inputs=validated_inputs)
                
                # Check if the tool returned an error
                if isinstance(result, dict) and "error" in result:
                    self.job_manager.fail_job(job_id, result["error"])
                    return f"❌ Error in '{tool_name}': {result['error']}"
                
                self.job_manager.complete_job(job_id, result)
            except Exception as e:
                print(f"[DEBUG] Exception during tool execution: {e}")
                import traceback
                traceback.print_exc()
                self.job_manager.fail_job(job_id, str(e))
                return f"❌ An unexpected error occurred in '{tool_name}': {e}"

            # Return a confirmation message with the result for the agent to use
            return f"✅ Tool '{tool_name}' executed successfully. Result: {result}"

        except Exception as e:
            print(f"❌ An unexpected error occurred in '{tool_name}': {e}")
            import traceback
            traceback.print_exc()
            if job_id:
                self.job_manager.fail_job(job_id, str(e))
            # Fallback error message if the error is outside the main try-except block
            return f"❌ An unexpected error occurred while trying to run '{tool_name}': {e}"


def create_langchain_agent(job_manager: JobManager, message_bus: MessageBus, tools_registry: Dict[str, Any], llm: BaseLanguageModel) -> DataScienceAgent:
    """Creates and configures the DataScienceAgent."""
    
    # Create an instance of the agent
    agent = DataScienceAgent(job_manager, message_bus, llm)
    
    # Create LangChain tool wrappers
    langchain_tools = []
    for tool_name, tool_instance in tools_registry.items():
        # Get tool description
        description = getattr(tool_instance, 'description', f"Tool for {tool_name}")
        if hasattr(tool_instance, '__doc__') and tool_instance.__doc__:
            description = tool_instance.__doc__.strip()
        
        # Create LangChain wrapper
        langchain_tool = LangChainToolWrapper(
            name=tool_name,
            description=description,
            tool_instance=tool_instance,
            job_manager=job_manager,
            message_bus=message_bus
        )
        
        agent.register_tool(langchain_tool)
    
    # Setup the agent
    agent.setup_agent()
    
    return agent 