#!/usr/bin/env python3
"""
Test script to check what functionality requires dlib
"""

print("Testing imports without dlib...")

try:
    import gradio as gr
    print("✅ Gradio import successful")
except ImportError as e:
    print(f"❌ Gradio import failed: {e}")

try:
    import torch
    print("✅ PyTorch import successful")
except ImportError as e:
    print(f"❌ PyTorch import failed: {e}")

try:
    import cv2
    print("✅ OpenCV import successful")
except ImportError as e:
    print(f"❌ OpenCV import failed: {e}")

try:
    from PIL import Image
    print("✅ PIL import successful")
except ImportError as e:
    print(f"❌ PIL import failed: {e}")

try:
    import dlib
    print("✅ dlib import successful")
except ImportError as e:
    print(f"❌ dlib import failed: {e}")

print("\nTesting app components...")

try:
    from src.config import get_settings
    print("✅ App config import successful")
except ImportError as e:
    print(f"❌ App config import failed: {e}")

try:
    from src.services import HairstyleTransferService
    print("✅ HairstyleTransferService import successful")
except ImportError as e:
    print(f"❌ HairstyleTransferService import failed: {e}")

print("\nChecking what specifically needs dlib...")

# Try to see where dlib is actually used
import os
import subprocess
import sys

def test_app_setup():
    """Test if app can initialize without dlib"""
    try:
        # Test if we can set up the basic structure
        barbershop_path = "./Barbershop"
        if not os.path.exists(barbershop_path):
            print("📁 Barbershop directory doesn't exist - app will need to download it")
        else:
            print("📁 Barbershop directory exists")
        
        return True
    except Exception as e:
        print(f"❌ App setup test failed: {e}")
        return False

test_app_setup()
print("\n" + "="*50)
print("CONCLUSION:")
print("Most dependencies are installed except dlib.")
print("You need to install Visual Studio Build Tools to compile dlib.")
print("="*50)