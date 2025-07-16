#!/usr/bin/env python3
"""
Simple test to debug token usage issue with enhanced debugging
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from droidagent.model import get_next_assistant_message

def test_debug_tokens():
    """Test with enhanced debugging to see actual metadata structure"""
    print("Testing with enhanced debugging...")
    
    system_message = "You are a helpful assistant."
    user_messages = ["Just say 'Hi' - one word only."]
    
    try:
        # Use gemini-2.0-flash since that's what you mentioned
        response = get_next_assistant_message(
            system_message=system_message,
            user_messages=user_messages,
            model="gemini-2.0-flash"
        )
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
        # This might give us insights into quota or other issues

if __name__ == "__main__":
    test_debug_tokens()
