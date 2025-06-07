from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

class MessageType(str, Enum):
    PROGRESS = "progress"
    PLOT = "plot"
    RESULT = "result"
    ERROR = "error"
    LOG = "log"
    JOB_STATUS = "job_status"

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    job_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any]

class JobStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Job(BaseModel):
    id: str
    tool_name: str
    status: JobStatus = JobStatus.CREATED
    progress: float = 0.0
    message: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def complete(self, result: Dict[str, Any]):
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result
        self.progress = 100.0
    
    def fail(self, error: str):
        self.status = JobStatus.FAILED
        self.error = error
        self.completed_at = datetime.now()

class ToolInput(BaseModel):
    """Base class for tool inputs"""
    model_config = {'arbitrary_types_allowed': True}

class CorrelationInput(ToolInput):
    n_points: int = Field(default=1000, ge=10, le=100000)

class BootstrapInput(ToolInput):
    n_iterations: int = Field(default=1000, ge=100, le=10000)