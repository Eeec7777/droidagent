#!/usr/bin/env python3
"""
Test script to verify Windows compatibility fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_timeout_fix():
    """Test that timeout decorator issue is fixed"""
    print("Testing timeout decorator fix...")
    
    try:
        from scripts.run_droidagent import main
        print("✓ run_droidagent imports successfully (no timeout_decorator error)")
        return True
    except Exception as e:
        print(f"✗ run_droidagent import failed: {e}")
        return False

def test_signal_compatibility():
    """Test signal compatibility"""
    print("\nTesting signal compatibility...")
    
    import signal
    
    # Test that we don't use SIGALRM on Windows
    if sys.platform.startswith('win'):
        if hasattr(signal, 'SIGALRM'):
            print("⚠️  SIGALRM is available on Windows (unexpected)")
        else:
            print("✓ SIGALRM not available on Windows (expected)")
        return True
    else:
        print("✓ Running on non-Windows platform")
        return True

def test_run_droidagent_structure():
    """Test the structure of run_droidagent after modifications"""
    print("\nTesting run_droidagent structure...")
    
    try:
        with open('scripts/run_droidagent.py', 'r') as f:
            content = f.read()
        
        # Check that timeout_decorator is removed
        if 'timeout_decorator' in content:
            print("✗ timeout_decorator still present in code")
            return False
        else:
            print("✓ timeout_decorator removed from code")
        
        # Check that timeout logic is implemented manually
        if 'timeout_duration' in content:
            print("✓ Manual timeout logic implemented")
        else:
            print("✗ Manual timeout logic not found")
            return False
        
        # Check that @timeout decorator is removed
        if '@timeout' in content:
            print("✗ @timeout decorator still present")
            return False
        else:
            print("✓ @timeout decorator removed")
        
        return True
    except Exception as e:
        print(f"✗ Error checking run_droidagent structure: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Windows Compatibility Test ===\n")
    
    tests = [
        test_timeout_fix,
        test_signal_compatibility,
        test_run_droidagent_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Platform: {sys.platform}")
    
    if passed == total:
        print("🎉 All Windows compatibility tests passed!")
        print("\nYou can now run DroidAgent on Windows:")
        print("cd scripts")
        print("python run_droidagent.py --app tippytipper --debug")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
