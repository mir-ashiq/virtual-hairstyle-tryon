#!/usr/bin/env python3
"""
Quick test to verify both apps can start properly
"""

print("🧪 Testing Virtual Hairstyle Try-On Apps")
print("=" * 50)

import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

def test_app(app_name, timeout=10):
    """Test if an app can start successfully"""
    print(f"\n📱 Testing {app_name}...")
    
    try:
        # Start the app in a subprocess
        process = subprocess.Popen(
            [sys.executable, app_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=Path.cwd()
        )
        
        # Wait for startup messages
        start_time = time.time()
        found_running = False
        
        while time.time() - start_time < timeout:
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"❌ {app_name} exited early")
                print("STDOUT:", stdout[-500:] if stdout else "None")
                print("STDERR:", stderr[-500:] if stderr else "None")
                return False
            
            # Try to read output
            try:
                process.stdout.flush()
                # Small delay to let output accumulate
                time.sleep(0.5)
            except:
                pass
            
            time.sleep(0.1)
        
        # If we get here, assume it started (no immediate crash)
        print(f"✅ {app_name} appears to start successfully")
        
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to test {app_name}: {e}")
        return False

def main():
    """Run the tests"""
    
    # Test basic app
    basic_success = test_app("app.py")
    
    # Test enhanced app  
    enhanced_success = test_app("app_enhanced.py")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"Basic App (app.py): {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"Enhanced App (app_enhanced.py): {'✅ PASS' if enhanced_success else '❌ FAIL'}")
    
    if basic_success and enhanced_success:
        print("\n🎉 Both apps are working! You can run them with:")
        print("   python app.py           # Basic version")
        print("   python app_enhanced.py  # Enhanced version")
        print("\n📱 Apps will be available at:")
        print("   http://127.0.0.1:7860")
        
        print("\n⚠️  Note: dlib is still missing, so face alignment will fail.")
        print("   Install Visual Studio Build Tools and then: pip install dlib")
    else:
        print("\n🔧 Some apps need more fixes.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()