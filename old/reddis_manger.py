# ipc/redis_manager.py
import redis
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

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
    
class RedisManager:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(
            host=host, 
            port=port, 
            db=db,
            decode_responses=True
        )
        self.pubsub = self.redis.pubsub()
        
    # For MCP Server side
    def publish_progress(self, job_id: str, progress: float, message: str):
        """Publish progress update"""
        msg = Message(
            type=MessageType.PROGRESS,
            job_id=job_id,
            timestamp=time.time(),
            data={"progress": progress, "message": message}
        )
        
        # Store in key for polling
        self.redis.setex(
            f"job:{job_id}:progress",
            300,  # 5 min TTL
            json.dumps(asdict(msg))
        )
        
        # Publish for real-time subscribers
        self.redis.publish(f"channel:{job_id}", json.dumps(asdict(msg)))
    
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
        
        # Store plot data
        self.redis.setex(
            f"job:{job_id}:plot:{int(time.time())}",
            3600,  # 1 hour TTL
            json.dumps(asdict(msg))
        )
        
        # Notify subscribers
        self.redis.publish(f"channel:{job_id}", json.dumps(asdict(msg)))
        
        # Return only description for LLM
        return description
    
    def publish_result(self, job_id: str, result: Dict[str, Any]):
        """Publish final results"""
        msg = Message(
            type=MessageType.RESULT,
            job_id=job_id,
            timestamp=time.time(),
            data=result
        )
        
        # Store in results list
        self.redis.lpush(
            f"job:{job_id}:results",
            json.dumps(asdict(msg))
        )
        self.redis.expire(f"job:{job_id}:results", 3600)
        
        # Notify
        self.redis.publish(f"channel:{job_id}", json.dumps(asdict(msg)))
    
    # For Dash side
    def subscribe_to_job(self, job_id: str):
        """Subscribe to job updates"""
        self.pubsub.subscribe(f"channel:{job_id}")
        
    def get_messages(self, timeout: float = 0.1) -> List[Message]:
        """Get all pending messages"""
        messages = []
        msg = self.pubsub.get_message(timeout=timeout)
        
        while msg:
            if msg['type'] == 'message':
                data = json.loads(msg['data'])
                messages.append(Message(**data))
            msg = self.pubsub.get_message(timeout=0.01)
            
        return messages
    
    def get_current_progress(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get current progress (for polling)"""
        data = self.redis.get(f"job:{job_id}:progress")
        if data:
            msg = json.loads(data)
            return msg['data']
        return None
    
    def get_job_plots(self, job_id: str) -> List[Dict[str, Any]]:
        """Get all plots for a job"""
        plots = []
        keys = self.redis.keys(f"job:{job_id}:plot:*")
        
        for key in sorted(keys):
            data = self.redis.get(key)
            if data:
                msg = json.loads(data)
                plots.append(msg['data'])
                
        return plots