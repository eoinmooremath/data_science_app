from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from core.models import Job, JobStatus, ToolInput
from core.job_manager import JobManager
from core.message_bus import MessageBus

class BaseTool(ABC):
    """Base class for all analysis tools"""
    
    # --- Refactored Attributes ---
    # These are now class attributes, not properties.
    # Subclasses should override these directly.
    name: str = "base_tool"
    description: str = "A base tool and should not be used directly."
    input_model: Optional[type[ToolInput]] = None
    
    # --- Existing __init__ ---
    def __init__(self, job_manager: JobManager, message_bus: MessageBus, **kwargs):
        self.job_manager = job_manager
        self.message_bus = message_bus
    
    @property
    def estimated_duration(self) -> float:
        """Estimated duration in seconds"""
        return 10.0
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for Claude"""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_model.model_json_schema()
        }
    
    def execute_async(self, job: Job, inputs: Dict[str, Any]):
        """Execute tool asynchronously"""
        import threading
        thread = threading.Thread(
            target=self._execute_wrapper,
            args=(job, inputs)
        )
        thread.daemon = True
        thread.start()
    
    def _execute_wrapper(self, job: Job, inputs: Dict[str, Any]):
        """Wrapper to handle execution lifecycle"""
        try:
            # Validate inputs
            validated_inputs = self.input_model(**inputs)
            
            # Update job status
            job.status = JobStatus.RUNNING
            self.job_manager.update_progress(job.id, 0, f"Starting {self.name}")
            
            # Execute tool
            result = self.execute(job.id, validated_inputs)
        
            # Complete job
            self.job_manager.complete_job(job.id, result)
            
        except Exception as e:
            # Handle errors
            self.job_manager.fail_job(job.id, str(e))
    
    @abstractmethod
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Execute the tool and return results"""
        pass
    
    def update_progress(self, job_id: str, progress: float, message: str):
        """Helper to update progress"""
        self.job_manager.update_progress(job_id, progress, message)


class FlexibleToolOutput(BaseModel):
    """Flexible output format that can handle various response types"""
    # Core fields
    summary: Dict[str, Any] = Field(description="Key results summary")
    
    # Optional structured data
    tables: Optional[List[Dict[str, Any]]] = Field(default=None, description="Tabular results")
    statistics: Optional[Dict[str, float]] = Field(default=None, description="Statistical measures")
    suggestions: Optional[List[Dict[str, str]]] = Field(default=None, description="Tool suggestions with reasons")
    
    # Flexible fields
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    interpretation: Optional[str] = Field(default=None, description="Human-readable interpretation")
    next_steps: Optional[List[str]] = Field(default=None, description="Suggested follow-up analyses")
    
    # Visualization hints
    visualizations: Optional[List[Dict[str, Any]]] = Field(default=None, description="Suggested plots")
    
    # Raw output for maximum flexibility
    raw: Optional[Any] = Field(default=None, description="Raw output from the underlying function")

class EnhancedBaseTool(BaseTool):
    """Enhanced base tool with namespace support and flexible outputs
    
    Inherits all functionality from BaseTool:
    - estimated_duration
    - input validation
    - execute_async
    - update_progress
    - etc.
    """
    
    # --- Refactored Namespace ---
    # This is now a class attribute to be overridden by subclasses.
    namespace: str = "base.enhanced"
    
    @property
    def category(self) -> str:
        """Extract category from namespace"""
        return self.namespace.split('.')[0]
    
    @property
    def subcategory(self) -> str:
        """Extract subcategory from namespace"""
        parts = self.namespace.split('.')
        return parts[1] if len(parts) > 1 else ""
    
    @property
    def output_format(self) -> str:
        """Describe expected output format for LLM"""
        return "Flexible format with summary, tables, statistics, and interpretations"
    
    def get_schema(self) -> Dict[str, Any]:
        """Get tool schema for Claude (compatible with Anthropic API)"""
        # Only return the standard schema fields that Anthropic API expects
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_model.model_json_schema()
        }
    
    @abstractmethod
    def format_output(self, raw_result: Any) -> FlexibleToolOutput:
        """Format raw results into flexible output"""
        pass
    
    def execute(self, job_id: str, inputs: ToolInput) -> Dict[str, Any]:
        """Override to ensure flexible output format"""
        # Subclasses implement _execute_analysis instead
        raw_result = self._execute_analysis(job_id, inputs)
        output = self.format_output(raw_result)
        return output.dict()
    
    @abstractmethod
    def _execute_analysis(self, job_id: str, inputs: ToolInput) -> Any:
        """Perform the actual analysis - replaces execute()"""
        pass