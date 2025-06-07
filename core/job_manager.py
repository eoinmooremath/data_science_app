from typing import Dict, Optional, Any
import threading
import uuid
from .models import Job, JobStatus, Message, MessageType
from .message_bus import MessageBus
import logging

# Configure logging for this module
logger = logging.getLogger(__name__)

class JobManager:
    """Manages job lifecycle and state"""
    
    def __init__(self, message_bus: MessageBus):
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.RLock()  # Use a re-entrant lock to prevent deadlocks
        self._message_bus = message_bus
        self._job_counter = 0  # Add counter for debugging
    
    def create_job(self, tool_name: str) -> Job:
        """Create a new job with guaranteed unique ID"""
        with self._lock:
            # Use both counter and uuid to ensure uniqueness
            self._job_counter += 1
            job_id = f"job_{uuid.uuid4().hex[:8]}"
            
            # Extra check to ensure uniqueness
            while job_id in self._jobs:
                job_id = f"job_{uuid.uuid4().hex[:8]}"
            
            job = Job(
                id=job_id,
                tool_name=tool_name
            )
            self._jobs[job_id] = job
            
            logger.info(f"Created job {job_id} for tool {tool_name}")
            
            # Publish job created message
            self._message_bus.publish(
                MessageType.LOG,
                job_id=job.id,
                data={"event": "job_created", "tool": tool_name}
            )
            
            return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        with self._lock:
            return self._jobs.get(job_id)
    
    def update_progress(self, job_id: str, progress: float, message: str):
        """Update job progress"""
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.progress = progress
                job.message = message
                logger.info(f"Updating progress for job {job_id}: {progress}% - {message}")
                
                # Publish progress message
                self._message_bus.publish(
                    MessageType.PROGRESS,
                    job_id=job_id,
                    data={"progress": progress, "message": message}
                )
    
    def complete_job(self, job_id: str, result: Dict[str, Any]):
        """Mark job as completed"""
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.complete(result)
                logger.info(f"Completing job {job_id} with result.")
                
                # Publish completion message
                self._message_bus.publish(
                    MessageType.RESULT,
                    job_id=job_id,
                    data=result
                )
    
    def fail_job(self, job_id: str, error: str):
        """Mark job as failed"""
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job.fail(error)
                logger.error(f"Failing job {job_id} with error: {error}")
                
                # Publish error message
                self._message_bus.publish(
                    MessageType.ERROR,
                    job_id=job_id,
                    data={"error": error}
                )