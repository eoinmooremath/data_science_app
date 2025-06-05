# test_core_integration.py
import os
import time
import threading
from core.message_bus import MessageBus
from core.job_manager import JobManager
from core.models import Message, MessageType
from tools.statistics import CorrelationTool, BootstrapTool
from llm.client import LLMClient

def test_core_integration():
    """Test that core components work together"""
    
    print("Starting Core Integration Test")
    print("=" * 50)
    
    # Initialize message bus
    message_bus = MessageBus()
    message_bus.start()
    print("✓ Message bus started")
    
    # Initialize job manager
    job_manager = JobManager(message_bus)
    print("✓ Job manager initialized")
    
    # Initialize tools
    tools = [
        CorrelationTool(job_manager, message_bus),
        BootstrapTool(job_manager, message_bus)
    ]
    print(f"✓ Initialized {len(tools)} tools")
    
    # Initialize LLM client
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  No API key found. Set ANTHROPIC_API_KEY environment variable")
        print("   Skipping LLM test")
        llm_client = None
    else:
        llm_client = LLMClient(job_manager, tools)
        print("✓ LLM client initialized")
    
    # Set up message listeners
    messages_received = []
    
    def message_handler(msg: Message):
        messages_received.append(msg)
        print(f"\n📨 Message received:")
        print(f"   Type: {msg.type.value}")
        print(f"   Job: {msg.job_id}")
        print(f"   Data: {msg.data}")
    
    # Subscribe to all message types
    for msg_type in MessageType:
        message_bus.subscribe(msg_type, message_handler)
    
    print("\n" + "=" * 50)
    print("TEST 1: Direct Tool Execution")
    print("=" * 50)
    
    # Test direct tool execution
    correlation_tool = tools[0]
    job1 = job_manager.create_job(correlation_tool.name)
    print(f"Created job: {job1.id}")
    
    # Execute tool
    correlation_tool.execute_async(job1, {"n_points": 100})
    
    # Wait for completion
    print("Waiting for job to complete...")
    time.sleep(6)
    
    # Check job status
    final_job = job_manager.get_job(job1.id)
    print(f"\nJob completed: {final_job.status.value}")
    print(f"Final progress: {final_job.progress}%")
    print(f"Result: {final_job.result}")
    
    if llm_client:
        print("\n" + "=" * 50)
        print("TEST 2: LLM Integration")
        print("=" * 50)
        
        # Test LLM integration
        messages = [
            {"role": "user", "content": "Can you analyze the correlation between two variables?"}
        ]
        
        print("Sending message to LLM...")
        response = llm_client.process_message(messages)
        print(f"LLM Response: {response}")
        
        if response["type"] == "tool_use":
            print(f"Tool execution started: {response['tool_name']}")
            print(f"Job ID: {response['job_id']}")
            
            # Wait for this job to complete
            time.sleep(6)
            
            job2 = job_manager.get_job(response['job_id'])
            print(f"\nJob completed: {job2.status.value}")
            print(f"Result: {job2.result}")
    
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total messages received: {len(messages_received)}")
    
    # Count by type
    msg_counts = {}
    for msg in messages_received:
        msg_type = msg.type.value
        msg_counts[msg_type] = msg_counts.get(msg_type, 0) + 1
    
    print("Messages by type:")
    for msg_type, count in msg_counts.items():
        print(f"  {msg_type}: {count}")
    
    # Cleanup
    message_bus.stop()
    print("\n✓ Test completed successfully!")

if __name__ == "__main__":
    # For Windows PowerShell, set API key like this:
    # $env:ANTHROPIC_API_KEY = "your-key-here"
    test_core_integration()