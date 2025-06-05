import multiprocessing as mp
import queue
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import threading


_queue_manager_instance = None

def get_queue_manager():
    """Get the singleton QueueManager instance"""
    global _queue_manager_instance
    if _queue_manager_instance is None:
        _queue_manager_instance = QueueManager()
    return _queue_manager_instance

class MessageType(Enum):
    PROGRESS = "progress"
    PLOT = "plot"
    RESULT = "result"
    LOG = "log"
    STATUS = "status"

@dataclass
class Message:
    type: MessageType
    job_id: str
    timestamp: float
    data: Dict[str, Any]

class QueueManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.messages = {}  # job_id -> list of messages
        self.subscribers = {}  # job_id -> list of queues
        self.lock = threading.Lock()
        self._initialized = True
    
    def publish_progress(self, job_id: str, progress: float, message: str):
        """Publish progress update"""
        msg = Message(
            type=MessageType.PROGRESS,
            job_id=job_id,
            timestamp=time.time(),
            data={"progress": progress, "message": message}
        )
        
        with self.lock:
            # Store message
            if job_id not in self.messages:
                self.messages[job_id] = []
            self.messages[job_id].append(msg)
            
            # Keep only last 1000 messages per job
            if len(self.messages[job_id]) > 1000:
                self.messages[job_id] = self.messages[job_id][-1000:]
            
            # Notify subscribers
            if job_id in self.subscribers:
                for q in self.subscribers[job_id]:
                    try:
                        q.put_nowait(msg)
                    except queue.Full:
                        pass
    

    def publish_result(self, job_id: str, result: Dict[str, Any]):
        """Publish final result"""
        msg = Message(
            type=MessageType.RESULT,
            job_id=job_id,
            timestamp=time.time(),
            data=result
        )
        
        with self.lock:
            if job_id not in self.messages:
                self.messages[job_id] = []
            self.messages[job_id].append(msg)
            
            if job_id in self.subscribers:
                for q in self.subscribers[job_id]:
                    try:
                        q.put_nowait(msg)
                    except queue.Full:
                        pass

    def publish_plot(self, job_id: str, plot_data: Dict[str, Any], 
                     description: Dict[str, Any]):
        """Publish plot data and description"""
        msg = Message(
            type=MessageType.PLOT,
            job_id=job_id,
            timestamp=time.time(),
            data={
                "plot_data": plot_data,
                "description": description
            }
        )
        
        with self.lock:
            if job_id not in self.messages:
                self.messages[job_id] = []
            self.messages[job_id].append(msg)
            
            # Notify subscribers
            if job_id in self.subscribers:
                for q in self.subscribers[job_id]:
                    try:
                        q.put_nowait(msg)
                    except queue.Full:
                        pass
        
        return description
    
    def subscribe_to_job(self, job_id: str) -> queue.Queue:
        """Subscribe to job updates, returns a queue"""
        q = queue.Queue(maxsize=1000)
        
        with self.lock:
            if job_id not in self.subscribers:
                self.subscribers[job_id] = []
            self.subscribers[job_id].append(q)
            
        return q
    
    def get_messages(self, q: queue.Queue, timeout: float = 0.1) -> List[Message]:
        """Get all pending messages from queue"""
        messages = []
        
        try:
            while True:
                msg = q.get(timeout=timeout)
                messages.append(msg)
                timeout = 0.01  # Subsequent messages with shorter timeout
        except queue.Empty:
            pass
            
        return messages
    
    def get_current_progress(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get current progress"""
        with self.lock:
            if job_id in self.messages:
                # Find most recent progress message
                for msg in reversed(self.messages[job_id]):
                    if msg.type == MessageType.PROGRESS:
                        return msg.data
        return None