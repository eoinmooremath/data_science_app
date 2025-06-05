from typing import Dict, List, Callable, Any
import threading
import queue
from .models import Message, MessageType

class MessageBus:
    """Central message bus for component communication"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        self._message_queue = queue.Queue()
        self._running = False
        self._processor_thread = None
    
    def start(self):
        """Start message processing"""
        self._running = True
        self._processor_thread = threading.Thread(target=self._process_messages)
        self._processor_thread.daemon = True
        self._processor_thread.start()
    
    def stop(self):
        """Stop message processing"""
        self._running = False
        if self._processor_thread:
            self._processor_thread.join()
    
    def publish(self, message: Message):
        """Publish a message"""
        self._message_queue.put(message)
    
    def subscribe(self, message_type: MessageType, callback: Callable[[Message], None]):
        """Subscribe to messages of a specific type"""
        with self._lock:
            if message_type.value not in self._subscribers:
                self._subscribers[message_type.value] = []
            self._subscribers[message_type.value].append(callback)
    
    def subscribe_to_job(self, job_id: str, callback: Callable[[Message], None]):
        """Subscribe to all messages for a specific job"""
        with self._lock:
            key = f"job:{job_id}"
            if key not in self._subscribers:
                self._subscribers[key] = []
            self._subscribers[key].append(callback)
    
    def _process_messages(self):
        """Process messages in background thread"""
        while self._running:
            try:
                message = self._message_queue.get(timeout=0.1)
                self._dispatch_message(message)
            except queue.Empty:
                continue
    
    def _dispatch_message(self, message: Message):
        """Dispatch message to subscribers"""
        with self._lock:
            # Dispatch to type subscribers
            if message.type.value in self._subscribers:
                for callback in self._subscribers[message.type.value]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"Error in message handler: {e}")
            
            # Dispatch to job subscribers
            job_key = f"job:{message.job_id}"
            if job_key in self._subscribers:
                for callback in self._subscribers[job_key]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"Error in job handler: {e}")