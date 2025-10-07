#!/usr/bin/env python
"""
Example script demonstrating the Virtual Hairstyle Try-On API.

This script shows how to use the modular components programmatically
without the Gradio UI.
"""

import sys
from pathlib import Path
from PIL import Image

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings
from src.services import HairstyleTransferService, HairstyleGalleryService
from src.utils import setup_logger, ImageValidator, ImageProcessor
import logging


def example_basic_transfer():
    """Example: Basic hairstyle transfer."""
    print("\n" + "="*60)
    print("Example 1: Basic Hairstyle Transfer")
    print("="*60)
    
    # Initialize service
    service = HairstyleTransferService()
    service.initialize()
    
    # Load images
    face_img = Image.open("examples/example_face.png")
    hair_img = Image.open("examples/example_hair.png")
    
    # Perform transfer
    print("Processing transfer...")
    result, log = service.transfer_hairstyle(
        face_image=face_img,
        hairstyle_image=hair_img,
        style="realistic",
        smoothness=5
    )
    
    # Save result
    if result:
        result.save("output/basic_transfer_result.png")
        print("✅ Success! Result saved to output/basic_transfer_result.png")
    else:
        print(f"❌ Failed: {log}")


def example_with_enhancement():
    """Example: Transfer with image enhancement."""
    print("\n" + "="*60)
    print("Example 2: Transfer with Image Enhancement")
    print("="*60)
    
    service = HairstyleTransferService()
    service.initialize()
    
    face_img = Image.open("examples/example_face.png")
    hair_img = Image.open("examples/example_hair.png")
    
    # Transfer with enhancement
    print("Processing transfer with enhancement...")
    result, log = service.transfer_hairstyle(
        face_image=face_img,
        hairstyle_image=hair_img,
        style="fidelity",
        smoothness=3,
        enhance=True  # Enable enhancement
    )
    
    if result:
        result.save("output/enhanced_transfer_result.png")
        print("✅ Success! Result saved to output/enhanced_transfer_result.png")
    else:
        print(f"❌ Failed: {log}")


def example_validation():
    """Example: Image validation before transfer."""
    print("\n" + "="*60)
    print("Example 3: Image Validation")
    print("="*60)
    
    validator = ImageValidator()
    
    # Load and validate image
    img = Image.open("examples/example_face.png")
    is_valid, message = validator.validate_image(image=img)
    
    print(f"Validation result: {'✅ Valid' if is_valid else '❌ Invalid'}")
    print(f"Message: {message}")
    
    # Validate file
    file_path = Path("examples/example_face.png")
    is_valid, message = validator.validate_file_type(file_path)
    print(f"\nFile type validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
    print(f"Message: {message}")


def example_image_processing():
    """Example: Image preprocessing."""
    print("\n" + "="*60)
    print("Example 4: Image Processing")
    print("="*60)
    
    processor = ImageProcessor()
    
    # Load image
    img = Image.open("examples/example_face.png")
    print(f"Original size: {img.size}")
    
    # Resize
    resized = processor.resize_image(img, max_width=512, max_height=512)
    print(f"Resized: {resized.size}")
    
    # Enhance
    enhanced = processor.enhance_image(
        resized,
        brightness=1.1,
        contrast=1.1,
        sharpness=1.2
    )
    print("Applied enhancements")
    
    # Get statistics
    stats = processor.get_image_stats(enhanced)
    print(f"\nImage statistics:")
    print(f"  - Mode: {stats['mode']}")
    print(f"  - Mean intensity: {stats['mean_intensity']:.2f}")
    print(f"  - Std deviation: {stats['std_intensity']:.2f}")
    
    # Save processed image
    enhanced.save("output/processed_image.png")
    print("\n✅ Processed image saved to output/processed_image.png")


def example_gallery():
    """Example: Using the hairstyle gallery."""
    print("\n" + "="*60)
    print("Example 5: Hairstyle Gallery")
    print("="*60)
    
    gallery = HairstyleGalleryService()
    
    # Get categories
    categories = gallery.get_categories()
    print(f"Available categories ({len(categories)}):")
    for cat in categories:
        print(f"  - {cat}")
    
    # Get gallery statistics
    stats = gallery.get_gallery_stats()
    print(f"\nGallery statistics:")
    print(f"  - Total categories: {stats['total_categories']}")
    print(f"  - Total hairstyles: {stats['total_hairstyles']}")
    print(f"  - Total examples: {stats['total_examples']}")
    
    # Get example pairs
    pairs = gallery.get_example_pairs()
    if pairs:
        print(f"\nExample pairs ({len(pairs)}):")
        for i, (face, hair) in enumerate(pairs, 1):
            print(f"  {i}. Face: {Path(face).name}, Hair: {Path(hair).name}")


def example_configuration():
    """Example: Working with configuration."""
    print("\n" + "="*60)
    print("Example 6: Configuration Management")
    print("="*60)
    
    settings = get_settings()
    
    print("Application settings:")
    print(f"  - App name: {settings.APP_NAME}")
    print(f"  - Version: {settings.APP_VERSION}")
    print(f"  - Default style: {settings.DEFAULT_STYLE}")
    print(f"  - Default smoothness: {settings.DEFAULT_SMOOTHNESS}")
    print(f"  - Process timeout: {settings.PROCESS_TIMEOUT}s")
    print(f"  - Max image size: {settings.MAX_IMAGE_SIZE / (1024*1024):.1f}MB")
    
    print("\nPaths:")
    print(f"  - Base dir: {settings.BASE_DIR}")
    print(f"  - Barbershop: {settings.BARBERSHOP_PATH}")
    print(f"  - Hairstyles: {settings.HAIRSTYLES_DIR}")


def example_model_info():
    """Example: Get model information."""
    print("\n" + "="*60)
    print("Example 7: Model Information")
    print("="*60)
    
    service = HairstyleTransferService()
    info = service.get_model_info()
    
    print("Model information:")
    print(f"  - Name: {info['name']}")
    print(f"  - Version: {info['version']}")
    print(f"  - Architecture: {info['architecture']}")
    print(f"  - Authors: {info['authors']}")
    print(f"  - Year: {info['year']}")
    print(f"  - Paper: {info['paper']}")
    print(f"  - Supported styles: {', '.join(info['supported_styles'])}")
    print(f"  - Smoothness range: {info['smoothness_range']}")
    print(f"  - Initialized: {info['is_initialized']}")


def example_with_progress():
    """Example: Transfer with progress tracking."""
    print("\n" + "="*60)
    print("Example 8: Transfer with Progress Tracking")
    print("="*60)
    
    service = HairstyleTransferService()
    service.initialize()
    
    face_img = Image.open("examples/example_face.png")
    hair_img = Image.open("examples/example_hair.png")
    
    # Define progress callback
    def progress_callback(progress, desc):
        bar_length = 40
        filled = int(bar_length * progress)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f'\r{bar} {progress*100:.0f}% - {desc}', end='', flush=True)
    
    print("Processing with progress tracking:")
    result, log = service.transfer_hairstyle(
        face_image=face_img,
        hairstyle_image=hair_img,
        style="realistic",
        smoothness=5,
        progress_callback=progress_callback
    )
    
    print()  # New line after progress bar
    
    if result:
        result.save("output/progress_transfer_result.png")
        print("✅ Success!")
    else:
        print(f"❌ Failed: {log}")


def main():
    """Run all examples."""
    # Setup logging
    setup_logger(level=logging.INFO)
    
    print("\n" + "="*60)
    print("Virtual Hairstyle Try-On - API Examples")
    print("="*60)
    
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    
    try:
        # Run examples
        example_configuration()
        example_model_info()
        example_validation()
        example_image_processing()
        example_gallery()
        
        # Check if example images exist
        if Path("examples/example_face.png").exists():
            example_basic_transfer()
            example_with_enhancement()
            example_with_progress()
        else:
            print("\n⚠️  Example images not found. Skipping transfer examples.")
            print("Add example_face.png and example_hair.png to the examples/ directory.")
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
