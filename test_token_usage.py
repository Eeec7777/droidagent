#!/usr/bin/env python3
"""
Test script to verify token usage display functionality
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from droidagent.model import get_next_assistant_message, APIUsageManager

def test_token_usage_display():
    """Test token usage display"""
    print("Testing token usage display...")
    
    # Test 1: Simple request
    print("\n1. Testing simple request with token display:")
    system_message = "You are a helpful assistant."
    user_messages = ["What is 2+2? Please give a brief answer."]
    
    try:
        response = get_next_assistant_message(system_message, user_messages)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Multiple requests
    print("\n2. Testing multiple requests:")
    user_messages = ["What is the capital of France?"]
    
    try:
        response = get_next_assistant_message(system_message, user_messages)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Show usage summary
    print("\n3. Showing usage summary:")
    APIUsageManager.print_usage_summary()
    
    # Test 4: Get specific model usage
    print("\n4. Getting specific model usage:")
    model_usage = APIUsageManager.get_model_usage("gemini-2.0-flash")
    print(f"Gemini 2.0 Flash usage: {model_usage}")

if __name__ == "__main__":
    test_token_usage_display()
