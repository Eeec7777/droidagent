#!/usr/bin/env python3
"""
Test script to verify thinking_config compatibility with different Gemini models
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from droidagent.model import get_next_assistant_message, APIUsageManager
from droidagent.config import GEMINI_1_5_FLASH, GEMINI_2_5_FLASH, GEMINI_1_5_PRO

def test_model_compatibility():
    """Test different Gemini models to ensure thinking_config compatibility"""
    print("Testing model compatibility with thinking_config...")
    
    system_message = "You are a helpful assistant."
    user_messages = ["What is 1+1? Please give a brief answer."]
    
    # Test models (in order of preference for testing)
    test_models = [
        GEMINI_1_5_FLASH,  # Should work without thinking_config
        GEMINI_2_5_FLASH,  # Should work with thinking_config
        GEMINI_1_5_PRO,    # Should work without thinking_config
    ]
    
    for model in test_models:
        print(f"\n🧪 Testing model: {model}")
        print("-" * 50)
        
        try:
            response = get_next_assistant_message(
                system_message=system_message,
                user_messages=user_messages,
                model=model
            )
            print(f"✅ Success! Response: {response}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error with {model}: {error_msg}")
            
            # Check if it's a thinking_config related error
            if "thinking_config" in error_msg.lower() or "thinking" in error_msg.lower():
                print(f"   💡 This appears to be a thinking_config compatibility issue")
            elif "429" in error_msg or "quota" in error_msg.lower():
                print(f"   ⚠️  API quota exceeded - cannot test further")
                break
            else:
                print(f"   🔍 Other error type")
    
    print("\n📊 Final Usage Summary:")
    APIUsageManager.print_usage_summary()

if __name__ == "__main__":
    test_model_compatibility()
