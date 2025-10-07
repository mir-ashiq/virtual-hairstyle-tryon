#!/usr/bin/env python
"""
Verification script to ensure all components are properly installed.
"""

import sys
from pathlib import Path

def print_status(message, status):
    """Print a status message."""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")
    return status

def verify_structure():
    """Verify directory structure."""
    print("\n📁 Checking Directory Structure...")
    
    directories = [
        "src/config",
        "src/models", 
        "src/services",
        "src/utils",
        "tests",
        "docs",
        "hairstyles",
        "examples"
    ]
    
    all_exist = True
    for directory in directories:
        exists = Path(directory).is_dir()
        all_exist &= print_status(f"{directory}/", exists)
    
    return all_exist

def verify_imports():
    """Verify all imports work."""
    print("\n📦 Checking Imports...")
    
    try:
        from src.config import get_settings
        print_status("src.config", True)
        
        from src.models import BarbershopModel, BaseModel
        print_status("src.models", True)
        
        from src.services import HairstyleTransferService, HairstyleGalleryService
        print_status("src.services", True)
        
        from src.utils import ImageValidator, ImageProcessor, setup_logger
        print_status("src.utils", True)
        
        return True
    except Exception as e:
        print_status(f"Import failed: {e}", False)
        return False

def verify_tests():
    """Check if tests can be loaded."""
    print("\n🧪 Checking Tests...")
    
    test_files = [
        "tests/test_config.py",
        "tests/test_validators.py",
        "tests/test_image_utils.py",
        "tests/test_gallery_service.py"
    ]
    
    all_exist = True
    for test_file in test_files:
        exists = Path(test_file).is_file()
        all_exist &= print_status(f"{test_file}", exists)
    
    return all_exist

def verify_documentation():
    """Verify documentation files."""
    print("\n📚 Checking Documentation...")
    
    docs = [
        "docs/api/API.md",
        "docs/ARCHITECTURE.md",
        "docs/PERFORMANCE.md",
        "docs/TROUBLESHOOTING.md",
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "README.md"
    ]
    
    all_exist = True
    for doc in docs:
        exists = Path(doc).is_file()
        all_exist &= print_status(f"{doc}", exists)
    
    return all_exist

def verify_configuration():
    """Verify configuration."""
    print("\n⚙️  Checking Configuration...")
    
    try:
        from src.config import get_settings
        settings = get_settings()
        
        print_status(f"App Name: {settings.APP_NAME}", True)
        print_status(f"Version: {settings.APP_VERSION}", True)
        print_status(f"Default Style: {settings.DEFAULT_STYLE}", True)
        
        return True
    except Exception as e:
        print_status(f"Config failed: {e}", False)
        return False

def verify_gallery():
    """Verify gallery structure."""
    print("\n🎨 Checking Gallery Structure...")
    
    categories = [
        "hairstyles/short",
        "hairstyles/medium",
        "hairstyles/long",
        "hairstyles/curly",
        "hairstyles/straight",
        "hairstyles/wavy",
        "hairstyles/formal",
        "hairstyles/casual",
        "hairstyles/colored",
        "hairstyles/natural"
    ]
    
    all_exist = True
    for category in categories:
        exists = Path(category).is_dir()
        all_exist &= print_status(f"{category}/", exists)
    
    return all_exist

def main():
    """Run all verifications."""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  Virtual Hairstyle Try-On - Installation Verification    ║
║  Enterprise Edition v2.0.0                                ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    checks = [
        ("Directory Structure", verify_structure),
        ("Python Imports", verify_imports),
        ("Test Files", verify_tests),
        ("Documentation", verify_documentation),
        ("Configuration", verify_configuration),
        ("Gallery Structure", verify_gallery),
    ]
    
    results = []
    for name, check in checks:
        results.append(check())
    
    print("\n" + "="*60)
    if all(results):
        print("✅ All verification checks passed!")
        print("🎉 Installation is complete and ready to use.")
        print("\nNext steps:")
        print("  1. Run: python app_enhanced.py")
        print("  2. Open: http://localhost:7860")
        print("  3. Read: docs/api/API.md for API usage")
        return 0
    else:
        print("❌ Some verification checks failed.")
        print("Please review the errors above and re-run setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
