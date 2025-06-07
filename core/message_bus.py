from typing import Dict, List, Callable, Any
import threading
import queue
from .models import Message, MessageType
from collections import defaultdict

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [MessageBus] - %(message)s')

class MessageBus:
    """
    A simple, thread-safe, in-memory message queue.
    This bus is designed to decouple background workers from the main UI thread.
    Workers can publish messages to the queue, and the UI can poll for them.
    """
    
    def __init__(self):
        self._queue = queue.Queue()
        logging.info("Queue-based MessageBus initialized.")

    def publish(self, topic, **kwargs):
        """
        Publish a message by putting it onto the internal queue.
        This method is thread-safe.
        """
        try:
            message = Message(type=topic, **kwargs)
            self._queue.put(message)
            logging.info(f"Published message to queue - Type: {message.type.name}, JobID: {message.job_id}")
        except Exception as e:
            logging.error(f"Failed to publish message: {e}", exc_info=True)

    def get_all_messages(self) -> List[Message]:
        """
        Retrieve all messages currently in the queue.
        This method is non-blocking and thread-safe.
        """
        messages = []
        while not self._queue.empty():
            try:
                messages.append(self._queue.get_nowait())
            except queue.Empty:
                break
        
        if messages:
            logging.info(f"Retrieved {len(messages)} messages from the queue.")
        
        return messages

    def subscribe(self, message_type: MessageType, callback: Callable):
        """Subscribe a callback to a specific message type."""
        with self._lock:
            if callback not in self._listeners[message_type]:
                self.remove_subscription(callback) # Remove previous subscriptions of same callback
                self._listeners[message_type].append(callback)
                logging.info(f"Subscribed '{callback.__name__}' to {message_type.name}")

    def remove_subscription(self, callback_to_remove: Callable):
        """Remove a callback from all message types."""
        with self._lock:
            for message_type in self._listeners:
                self._listeners[message_type] = [
                    cb for cb in self._listeners[message_type] if cb != callback_to_remove
                ]

    def publish_message(self, message: Message):
        """Publish a pre-constructed Message object."""
        logging.info(f"Publishing message - Type: {message.type.name}, JobID: {message.job_id}")
        
        listeners_to_notify = []
        with self._lock:
            if message.type in self._listeners:
                listeners_to_notify = self._listeners[message.type][:]

        if not listeners_to_notify:
            logging.warning(f"No listeners for message type {message.type.name}")
            return

        for callback in listeners_to_notify:
            try:
                # To prevent long-running callbacks from blocking the bus,
                # consider running them in a separate thread.
                callback(message)
                logging.info(f"Notified {callback.__name__} for {message.type.name} (Job: {message.job_id})")
            except Exception as e:
                logging.error(f"Error in callback '{callback.__name__}' for {message.type.name}: {e}", exc_info=True)
    
    def subscribe_to_job(self, job_id: str, callback: Callable[[Message], None]):
        """Subscribe to all messages for a specific job"""
        with self._lock:
            key = f"job:{job_id}"
            if key not in self._listeners:
                self._listeners[key] = []
            self._listeners[key].append(callback)
    
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
            if message.type in self._listeners:
                for callback in self._listeners[message.type]:
                    try:
                        callback(message)
                        logging.info(f"Notified {callback.__name__} for {message.type.name}")
                    except Exception as e:
                        logging.error(f"Error in callback for {message.type.name}: {e}")
            
            # Dispatch to job subscribers
            job_key = f"job:{message.job_id}"
            if job_key in self._listeners:
                for callback in self._listeners[job_key]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"Error in job handler: {e}")