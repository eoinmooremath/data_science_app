from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from core.models import Job, Message

@dataclass
class JobUIState:
    """UI state for a job"""
    job_id: str
    progress: float = 0.0
    message: str = ""
    plot_data: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ChatMessage:
    """Chat message for display"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    job_id: Optional[str] = None

class UIStateManager:
    """Manages UI state"""
    
    def __init__(self):
        self.job_states: Dict[str, JobUIState] = {}
        self.chat_messages: List[ChatMessage] = []
        self.current_job_id: Optional[str] = None
        self.results: List[Dict[str, Any]] = []  

    def add_chat_message(self, role: str, content: str, job_id: Optional[str] = None):
        """Add a chat message"""
        self.chat_messages.append(ChatMessage(role, content, job_id))
    
    def create_job_state(self, job_id: str) -> JobUIState:
        """Create UI state for a job"""
        state = JobUIState(job_id=job_id)
        self.job_states[job_id] = state
        self.current_job_id = job_id
        return state
    
    def update_job_progress(self, job_id: str, progress: float, message: str):
        """Update job progress"""
        if job_id in self.job_states:
            self.job_states[job_id].progress = progress
            self.job_states[job_id].message = message
    
    def update_job_plot(self, job_id: str, plot_data: Dict[str, Any]):
        """Update job plot data"""
        if job_id in self.job_states:
            self.job_states[job_id].plot_data = plot_data
    
    def update_job_result(self, job_id: str, result: Dict[str, Any]):
        """Update job result"""
        if job_id in self.job_states:
            self.job_states[job_id].result = result

    def add_result(self, job_id: str, tool_name: str, result: Dict[str, Any]):
        """Add a result to the ledger"""
        self.results.append({
            "job_id": job_id,
            "tool_name": tool_name,
            "timestamp": datetime.now(),
            "data": result
        })