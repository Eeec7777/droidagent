#!/usr/bin/env python3
"""
Debug script to test token usage parsing with mock data
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from droidagent.model import APIUsageManager

class MockUsageMetadata:
    """Mock usage metadata to test different attribute structures"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def test_token_parsing():
    """Test token parsing with different attribute structures"""
    print("Testing token usage parsing with different metadata structures...")
    
    # Test case 1: Standard structure
    print("\n1. Testing standard structure (input_tokens, output_tokens):")
    mock_usage1 = MockUsageMetadata(input_tokens=100, output_tokens=50)
    APIUsageManager.record_usage("test-model-1", mock_usage1)
    
    # Test case 2: Alternative structure
    print("\n2. Testing alternative structure (prompt_tokens, completion_tokens):")
    mock_usage2 = MockUsageMetadata(prompt_tokens=80, completion_tokens=40)
    APIUsageManager.record_usage("test-model-2", mock_usage2)
    
    # Test case 3: Total tokens only
    print("\n3. Testing total tokens only:")
    mock_usage3 = MockUsageMetadata(total_tokens=200)
    APIUsageManager.record_usage("test-model-3", mock_usage3)
    
    # Test case 4: Mixed structure
    print("\n4. Testing mixed structure (inputTokens, outputTokens, totalTokens):")
    mock_usage4 = MockUsageMetadata(inputTokens=120, outputTokens=60, totalTokens=180)
    APIUsageManager.record_usage("test-model-4", mock_usage4)
    
    # Test case 5: Empty structure
    print("\n5. Testing empty structure:")
    mock_usage5 = MockUsageMetadata()
    APIUsageManager.record_usage("test-model-5", mock_usage5)
    
    print("\n📊 Final Usage Summary:")
    APIUsageManager.print_usage_summary()
    
    print("\n🔍 Individual model usage:")
    for model_name in ["test-model-1", "test-model-2", "test-model-3", "test-model-4", "test-model-5"]:
        usage = APIUsageManager.get_model_usage(model_name)
        print(f"{model_name}: {usage}")

if __name__ == "__main__":
    test_token_parsing()
