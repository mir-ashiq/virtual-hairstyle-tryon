"""Unit tests for validators."""

import unittest
from pathlib import Path
from PIL import Image
import numpy as np
from src.utils.validators import ImageValidator, ValidationError


class TestImageValidator(unittest.TestCase):
    """Test image validation utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ImageValidator()
    
    def test_validator_initialization(self):
        """Test validator initializes correctly."""
        self.assertIsNotNone(self.validator)
        self.assertIsNotNone(self.validator.settings)
    
    def test_validate_file_type_valid(self):
        """Test file type validation with valid extensions."""
        valid_files = [
            Path("test.jpg"),
            Path("test.jpeg"),
            Path("test.png"),
            Path("TEST.JPG"),
        ]
        
        for file_path in valid_files:
            is_valid, msg = self.validator.validate_file_type(file_path)
            self.assertTrue(is_valid, f"Failed for {file_path}: {msg}")
    
    def test_validate_file_type_invalid(self):
        """Test file type validation with invalid extensions."""
        invalid_files = [
            Path("test.gif"),
            Path("test.bmp"),
            Path("test.txt"),
        ]
        
        for file_path in invalid_files:
            is_valid, msg = self.validator.validate_file_type(file_path)
            self.assertFalse(is_valid, f"Should fail for {file_path}")
    
    def test_validate_image_content_valid(self):
        """Test image content validation with valid image."""
        # Create a valid test image
        img = Image.new('RGB', (512, 512), color='white')
        is_valid, msg = self.validator.validate_image_content(img)
        self.assertTrue(is_valid, msg)
    
    def test_validate_image_content_too_small(self):
        """Test image content validation with small image."""
        # Create a small image
        img = Image.new('RGB', (100, 100), color='white')
        is_valid, msg = self.validator.validate_image_content(img)
        self.assertFalse(is_valid)
        self.assertIn("width", msg.lower())
    
    def test_validate_image_content_invalid_mode(self):
        """Test image content validation with invalid mode."""
        # Create a grayscale image
        img = Image.new('L', (512, 512), color=128)
        is_valid, msg = self.validator.validate_image_content(img)
        self.assertFalse(is_valid)
        self.assertIn("mode", msg.lower())
    
    def test_validate_image_rgba_accepted(self):
        """Test that RGBA images are accepted."""
        img = Image.new('RGBA', (512, 512), color=(255, 255, 255, 255))
        is_valid, msg = self.validator.validate_image_content(img)
        self.assertTrue(is_valid, msg)


if __name__ == '__main__':
    unittest.main()
