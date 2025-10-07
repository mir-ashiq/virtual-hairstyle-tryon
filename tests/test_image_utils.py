"""Unit tests for image processing utilities."""

import unittest
from PIL import Image
import numpy as np
from src.utils.image_utils import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Test image processing utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = ImageProcessor()
        # Create a test image
        self.test_image = Image.new('RGB', (1024, 768), color='blue')
    
    def test_resize_image_smaller(self):
        """Test resizing to smaller dimensions."""
        resized = self.processor.resize_image(
            self.test_image,
            max_width=512,
            max_height=512
        )
        
        self.assertLessEqual(resized.size[0], 512)
        self.assertLessEqual(resized.size[1], 512)
    
    def test_resize_image_maintains_aspect(self):
        """Test that resize maintains aspect ratio."""
        original_ratio = self.test_image.size[0] / self.test_image.size[1]
        
        resized = self.processor.resize_image(
            self.test_image,
            max_width=512,
            max_height=512,
            maintain_aspect=True
        )
        
        new_ratio = resized.size[0] / resized.size[1]
        self.assertAlmostEqual(original_ratio, new_ratio, places=2)
    
    def test_resize_image_no_upscale(self):
        """Test that resize doesn't upscale smaller images."""
        small_img = Image.new('RGB', (256, 256), color='red')
        resized = self.processor.resize_image(
            small_img,
            max_width=1024,
            max_height=1024
        )
        
        self.assertEqual(resized.size, small_img.size)
    
    def test_convert_to_rgb(self):
        """Test RGB conversion."""
        # Test with RGBA image
        rgba_img = Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))
        rgb_img = self.processor.convert_to_rgb(rgba_img)
        self.assertEqual(rgb_img.mode, 'RGB')
        
        # Test with already RGB image
        rgb_img2 = self.processor.convert_to_rgb(self.test_image)
        self.assertEqual(rgb_img2.mode, 'RGB')
    
    def test_crop_center(self):
        """Test center cropping."""
        cropped = self.processor.crop_center(
            self.test_image,
            target_width=512,
            target_height=512
        )
        
        self.assertEqual(cropped.size, (512, 512))
    
    def test_get_image_stats(self):
        """Test image statistics calculation."""
        stats = self.processor.get_image_stats(self.test_image)
        
        self.assertIn('width', stats)
        self.assertIn('height', stats)
        self.assertIn('mode', stats)
        self.assertIn('mean_intensity', stats)
        self.assertEqual(stats['width'], 1024)
        self.assertEqual(stats['height'], 768)
        self.assertEqual(stats['mode'], 'RGB')
    
    def test_enhance_image(self):
        """Test image enhancement."""
        enhanced = self.processor.enhance_image(
            self.test_image,
            brightness=1.2,
            contrast=1.1,
            sharpness=1.1
        )
        
        self.assertEqual(enhanced.size, self.test_image.size)
        self.assertEqual(enhanced.mode, self.test_image.mode)
    
    def test_apply_blur(self):
        """Test blur application."""
        blurred = self.processor.apply_blur(self.test_image, radius=3)
        
        self.assertEqual(blurred.size, self.test_image.size)
        self.assertEqual(blurred.mode, self.test_image.mode)


if __name__ == '__main__':
    unittest.main()
