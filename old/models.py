# models.py
from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime

class MessageType(str, Enum):
    PROGRESS = "progress"
    PLOT = "plot"
    RESULT = "result"
    ERROR = "error"

class Message(BaseModel):
    type: MessageType
    job_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Dict[str, Any]

class Job(BaseModel):
    id: str
    tool_name: str
    status: str = "created"
    progress: float = 0.0
    message: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    result: Optional[Dict[str, Any]] = None

class ToolInput(BaseModel):
    n_points: Optional[int] = 1000
    n_iterations: Optional[int] = 1000