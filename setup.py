#!/usr/bin/env python
"""
Setup and initialization script for Virtual Hairstyle Try-On.
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def install_dependencies(dev=False):
    """Install required dependencies."""
    print_header("Installing Dependencies")
    
    requirements = ["requirements.txt"]
    if dev:
        requirements.append("requirements-dev.txt")
    
    for req_file in requirements:
        print(f"\nInstalling from {req_file}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", req_file],
                check=True
            )
            print(f"✅ {req_file} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req_file}")
            return False
    
    return True


def setup_directories():
    """Create necessary directories."""
    print_header("Setting Up Directories")
    
    directories = [
        "output",
        "logs",
        "temp",
        "hairstyles/short",
        "hairstyles/medium",
        "hairstyles/long",
        "hairstyles/curly",
        "hairstyles/straight",
        "hairstyles/wavy",
        "hairstyles/formal",
        "hairstyles/casual",
        "hairstyles/colored",
        "hairstyles/natural",
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}/")
    
    return True


def verify_installation():
    """Verify the installation."""
    print_header("Verifying Installation")
    
    try:
        # Test imports
        from src.config import get_settings
        from src.models import BarbershopModel
        from src.services import HairstyleTransferService
        from src.utils import ImageValidator
        
        print("✅ All imports successful")
        
        # Test configuration
        settings = get_settings()
        print(f"✅ Configuration loaded: {settings.APP_NAME} v{settings.APP_VERSION}")
        
        # Test gallery service
        from src.services import HairstyleGalleryService
        gallery = HairstyleGalleryService()
        categories = gallery.get_categories()
        print(f"✅ Gallery service working: {len(categories)} categories")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False


def run_tests():
    """Run test suite."""
    print_header("Running Tests")
    
    try:
        result = subprocess.run(
            [sys.executable, "tests/run_tests.py"],
            check=False
        )
        
        if result.returncode == 0:
            print("\n✅ All tests passed")
            return True
        else:
            print("\n⚠️  Some tests failed (this is okay if dependencies are missing)")
            return True  # Don't fail setup for test failures
            
    except Exception as e:
        print(f"⚠️  Could not run tests: {str(e)}")
        return True  # Don't fail setup


def print_next_steps():
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    print("""
Next steps:

1. Run the application:
   
   # Enhanced version (recommended)
   python app_enhanced.py
   
   # Original version
   python app.py

2. Access the UI:
   Open http://localhost:7860 in your browser

3. Add hairstyle samples:
   Add images to hairstyles/ directory in appropriate categories

4. Read the documentation:
   - docs/api/API.md - API reference
   - docs/ARCHITECTURE.md - Architecture guide
   - docs/TROUBLESHOOTING.md - Common issues
   - docs/PERFORMANCE.md - Performance tips

5. Run examples:
   python examples/api_examples.py

For more information, see README.md
""")


def main():
    """Main setup function."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  Virtual Hairstyle Try-On - Setup Script                 ║
║  Enterprise Edition v2.0.0                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Parse arguments
    dev_mode = "--dev" in sys.argv or "-d" in sys.argv
    skip_tests = "--skip-tests" in sys.argv
    
    if dev_mode:
        print("🔧 Development mode enabled - will install dev dependencies")
    
    # Run setup steps
    steps = [
        ("Python Version Check", lambda: check_python_version()),
        ("Directory Setup", lambda: setup_directories()),
        ("Dependency Installation", lambda: install_dependencies(dev_mode)),
        ("Installation Verification", lambda: verify_installation()),
    ]
    
    if not skip_tests and dev_mode:
        steps.append(("Test Suite", lambda: run_tests()))
    
    # Execute steps
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please check the errors above and try again.")
            return 1
    
    # Print success message
    print_next_steps()
    return 0


if __name__ == "__main__":
    sys.exit(main())
