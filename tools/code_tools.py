# tools/code_tools.py
import subprocess
import os
import uuid
from typing import Dict, Any, Type

from pydantic import Field
from langchain_core.language_models import BaseLanguageModel

from tools.base import BaseTool
from core.models import ToolInput

# --- Constants ---
TEMP_CODE_DIR = "temp_code"
os.makedirs(TEMP_CODE_DIR, exist_ok=True)

# --- Tool Inputs ---
class CodeGeneratorInput(ToolInput):
    """Input for the Code Generator Tool."""
    query: str = Field(..., description="A detailed natural language description of the code to be generated.")

class CodeExecutorInput(ToolInput):
    """Input for the Code Executor Tool."""
    file_path: str = Field(..., description="The local file path of the Python script to execute.")

# --- Tools ---
class CodeGeneratorTool(BaseTool):
    """
    A tool that generates Python code from a natural language query and saves it to a file.
    """
    name: str = "code_generator"
    description: str = "Generates Python code from a query and saves it to a file. Returns the file path."
    input_model: Type[ToolInput] = CodeGeneratorInput
    llm: BaseLanguageModel

    def __init__(self, job_manager, message_bus, llm: BaseLanguageModel, **kwargs):
        super().__init__(job_manager, message_bus, **kwargs)
        self.llm = llm

    def execute(self, job_id: str, inputs: CodeGeneratorInput) -> Dict[str, Any]:
        self.update_progress(job_id, 0, "Generating code from query...")
        
        prompt = f"""
        You are a code generation expert. Based on the following query, write a self-contained Python script.
        The script should not require any user input.
        To make data available to other tools, save pandas DataFrames to the `uploaded_datasets` dictionary.
        Example of saving data:
        ```python
        import pandas as pd
        from tools.data_tools import uploaded_datasets
        df = pd.DataFrame(...)
        uploaded_datasets['my_data'] = df
        ```
        
        ONLY output the raw Python code. Do not include markdown like ```python or any explanations.

        Query: "{inputs.query}"
        """
        
        try:
            response = self.llm.invoke(prompt)
            code = response.content
        except Exception as e:
            return {"error": f"LLM invocation failed: {str(e)}"}

        self.update_progress(job_id, 50, "Code generated. Saving to file...")

        # Clean up potential markdown backticks
        if code.strip().startswith("```python"):
            code = code.strip()[9:]
            if code.strip().endswith("```"):
                code = code.strip()[:-3]
        
        file_name = f"generated_code_{uuid.uuid4()}.py"
        file_path = os.path.join(TEMP_CODE_DIR, file_name)

        with open(file_path, "w") as f:
            f.write(code)

        self.update_progress(job_id, 100, f"Code saved to {file_path}")
        return {"success": True, "file_path": file_path, "message": f"Code saved to {file_path}"}


class CodeExecutorTool(BaseTool):
    """
    A tool that executes Python code from a specified file path.
    """
    name: str = "code_executor"
    description: str = "Executes a Python script from a local file path and returns the output."
    input_model: Type[ToolInput] = CodeExecutorInput

    def execute(self, job_id: str, inputs: CodeExecutorInput) -> Dict[str, Any]:
        self.update_progress(job_id, 0, f"Executing code from {inputs.file_path}...")
        
        if not os.path.exists(inputs.file_path):
            return {"error": f"File not found: {inputs.file_path}"}

        try:
            process = subprocess.run(
                ["python", inputs.file_path],
                capture_output=True, text=True, timeout=60, check=False
            )
            self.update_progress(job_id, 80, "Execution finished.")

            if process.returncode == 0:
                output = process.stdout or "Script executed successfully with no output."
                return {"success": True, "output": output}
            else:
                return {"error": "Code execution failed", "stderr": process.stderr}

        except subprocess.TimeoutExpired:
            return {"error": "Code execution timed out after 60 seconds."}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}
        finally:
            self.update_progress(job_id, 100, "Cleanup complete.")
            # We might not want to delete the file immediately for debugging
            # if os.path.exists(inputs.file_path):
            #     os.remove(inputs.file_path) 