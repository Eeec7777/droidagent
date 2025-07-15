#!/usr/bin/env python3
"""
Installation verification script for DroidAgent
"""

import sys
import subprocess
import importlib

def check_module(module_name, description=""):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} {description}")
        return True
    except ImportError as e:
        print(f"✗ {module_name} {description} - Error: {e}")
        return False

def check_specific_imports():
    """Check specific imports that are commonly problematic"""
    try:
        from droidbot.device import Device
        from droidbot.app import App
        from droidbot.input_event import IntentEvent, KeyEvent
        print("✓ DroidBot specific imports (Device, App, IntentEvent, KeyEvent)")
        return True
    except ImportError as e:
        print(f"✗ DroidBot specific imports - Error: {e}")
        return False

def check_gemini_integration():
    """Check Gemini integration"""
    try:
        from droidagent.model import client, get_next_assistant_message
        print("✓ Gemini integration")
        return True
    except ImportError as e:
        print(f"✗ Gemini integration - Error: {e}")
        return False

def check_droidagent():
    """Check DroidAgent components"""
    try:
        from droidagent import TaskBasedAgent
        print("✓ DroidAgent core components")
        return True
    except ImportError as e:
        print(f"✗ DroidAgent core components - Error: {e}")
        return False

def main():
    print("=== DroidAgent Installation Verification ===\n")
    
    # Check core dependencies
    modules_to_check = [
        ("setuptools", "- Required for pkg_resources"),
        ("requests", "- HTTP library"),
        ("dotenv", "- Environment variable management"),
        ("google.genai", "- Google Gemini API"),
        ("timeout_decorator", "- Timeout functionality"),
        ("chromadb", "- Vector database"),
        ("pandas", "- Data analysis"),
        ("friendlywords", "- Word generation"),
        ("droidbot", "- Android testing framework"),
        ("androguard", "- Android APK analysis"),
        ("networkx", "- Graph algorithms"),
        ("PIL", "- Image processing (Pillow)"),
    ]
    
    print("Checking core dependencies:")
    all_passed = True
    for module, desc in modules_to_check:
        if not check_module(module, desc):
            all_passed = False
    
    print("\nChecking specific imports:")
    if not check_specific_imports():
        all_passed = False
    
    if not check_gemini_integration():
        all_passed = False
    
    if not check_droidagent():
        all_passed = False
    
    print("\n=== Results ===")
    if all_passed:
        print("🎉 All checks passed! DroidAgent is ready to use.")
        print("\nTo run DroidAgent:")
        print("cd scripts")
        print("python run_droidagent.py --app AnkiDroid --debug")
    else:
        print("❌ Some checks failed. Please install missing dependencies.")
        print("\nTo install missing dependencies:")
        print("pip install -r requirements.txt")
        print("cd droidbot && pip install -e .")
        print("cd .. && pip install -e .")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
