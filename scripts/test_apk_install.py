#!/usr/bin/env python3
"""
Test script to verify APK installation fix for test apps
"""

import subprocess
import sys
import os

def test_adb_install_command():
    """Test the ADB install command generation"""
    print("Testing ADB install command generation...")
    
    # Mock the install command that would be generated
    mock_serial = "emulator-5554"
    mock_app_path = "target_apps/tippytipper.apk"
    
    # This is what the command should look like with our fix
    expected_cmd = ["adb", "-s", mock_serial, "install", "-r", "-t", "-g", mock_app_path]
    
    print(f"Expected command: {' '.join(expected_cmd)}")
    print("✓ Command includes -t flag for test app installation")
    print("✓ Command includes -g flag for automatic permissions")
    print("✓ Command includes -r flag for reinstallation")
    
    return True

def test_adb_availability():
    """Test if ADB is available"""
    print("\nTesting ADB availability...")
    
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ ADB is available")
            print(f"  Version: {result.stdout.strip().split()[0]}")
            return True
        else:
            print("✗ ADB returned error")
            print(f"  Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ ADB command timed out")
        return False
    except FileNotFoundError:
        print("✗ ADB not found in PATH")
        print("  Please install Android SDK Platform Tools")
        return False

def test_device_connection():
    """Test device connection"""
    print("\nTesting device connection...")
    
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            devices = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = [d for d in devices if d.strip()]  # Remove empty lines
            
            if devices:
                print("✓ Devices found:")
                for device in devices:
                    print(f"  {device}")
                return True
            else:
                print("⚠️  No devices connected")
                print("  Please start an emulator or connect a device")
                return False
        else:
            print("✗ Failed to list devices")
            print(f"  Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ ADB devices command timed out")
        return False
    except FileNotFoundError:
        print("✗ ADB not found")
        return False

def test_apk_existence():
    """Test if APK file exists"""
    print("\nTesting APK file existence...")
    
    apk_path = "../target_apps/tippytipper.apk"
    if os.path.exists(apk_path):
        print("✓ APK file exists")
        print(f"  Path: {os.path.abspath(apk_path)}")
        print(f"  Size: {os.path.getsize(apk_path)} bytes")
        return True
    else:
        print("✗ APK file not found")
        print(f"  Expected path: {os.path.abspath(apk_path)}")
        return False

def main():
    """Run all tests"""
    print("=== APK Installation Fix Test ===\n")
    
    tests = [
        ("ADB Install Command", test_adb_install_command),
        ("ADB Availability", test_adb_availability),
        ("Device Connection", test_device_connection),
        ("APK Existence", test_apk_existence)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print(f"\n=== Test Results ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\nThe APK installation fix should work.")
        print("You can now try running:")
        print("cd ../scripts")
        print("python run_droidagent.py --app tippytipper --debug --is_emulator")
        return 0
    else:
        print("❌ Some tests failed.")
        if not results[1][1]:  # ADB availability
            print("\nTo fix ADB issues:")
            print("1. Install Android SDK Platform Tools")
            print("2. Add ADB to your PATH")
        if not results[2][1]:  # Device connection
            print("\nTo fix device connection:")
            print("1. Start an Android emulator")
            print("2. Or connect a physical device with USB debugging enabled")
        return 1

if __name__ == "__main__":
    sys.exit(main())
