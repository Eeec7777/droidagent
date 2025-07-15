#!/usr/bin/env python3
"""
Test script to verify Gemini 2.5 Flash integration
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from droidagent.model import get_next_assistant_message, client
from droidagent.config import agent_config

def test_gemini_basic():
    """Test basic Gemini functionality"""
    print("Testing Gemini 2.5 Flash basic functionality...")
    
    system_message = "You are a helpful assistant that responds concisely."
    user_messages = ["What is 2+2?"]
    
    try:
        response = get_next_assistant_message(system_message, user_messages)
        print(f"✓ Basic test passed")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"✗ Basic test failed: {e}")
        return False

def test_gemini_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    print(f"Actor model: {agent_config.actor_model}")
    print(f"Observer model: {agent_config.observer_model}")
    print(f"Planner model: {agent_config.planner_model}")
    print(f"Reflector model: {agent_config.reflector_model}")
    
    # Verify all models are using Gemini 2.5 Flash
    expected_model = "gemini-2.5-flash"
    if (agent_config.actor_model == expected_model and 
        agent_config.observer_model == expected_model and
        agent_config.planner_model == expected_model and
        agent_config.reflector_model == expected_model):
        print("✓ All models correctly configured to use Gemini 2.5 Flash")
        return True
    else:
        print("✗ Models not properly configured")
        return False

def test_gemini_conversation():
    """Test conversation flow"""
    print("\nTesting conversation flow...")
    
    system_message = "You are a helpful assistant."
    user_messages = ["Hello", "What's your name?"]
    assistant_messages = ["Hello! How can I help you today?"]
    
    try:
        response = get_next_assistant_message(system_message, user_messages, assistant_messages)
        print(f"✓ Conversation test passed")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"✗ Conversation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Gemini 2.5 Flash Integration Test ===\n")
    
    tests = [
        test_gemini_basic,
        test_gemini_config,
        test_gemini_conversation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Gemini 2.5 Flash integration is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
