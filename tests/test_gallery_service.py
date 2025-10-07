"""Unit tests for gallery service."""

import unittest
from pathlib import Path
from PIL import Image
from src.services.gallery_service import HairstyleGalleryService


class TestHairstyleGalleryService(unittest.TestCase):
    """Test hairstyle gallery service."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = HairstyleGalleryService()
    
    def test_service_initialization(self):
        """Test service initializes correctly."""
        self.assertIsNotNone(self.service)
        self.assertIsNotNone(self.service.hairstyles_dir)
    
    def test_get_categories(self):
        """Test getting categories."""
        categories = self.service.get_categories()
        self.assertIsInstance(categories, list)
        # Should have at least the default categories
        expected_categories = {'short', 'medium', 'long', 'curly', 'straight'}
        actual_categories = set(categories)
        self.assertTrue(expected_categories.issubset(actual_categories))
    
    def test_get_example_pairs(self):
        """Test getting example pairs."""
        pairs = self.service.get_example_pairs()
        self.assertIsInstance(pairs, list)
        
        # Each pair should be a tuple of two paths
        for pair in pairs:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            self.assertTrue(Path(pair[0]).exists())
            self.assertTrue(Path(pair[1]).exists())
    
    def test_get_gallery_stats(self):
        """Test getting gallery statistics."""
        stats = self.service.get_gallery_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_categories', stats)
        self.assertIn('total_hairstyles', stats)
        self.assertIn('total_examples', stats)
        
        # Values should be non-negative integers
        for key, value in stats.items():
            self.assertIsInstance(value, int)
            self.assertGreaterEqual(value, 0)


if __name__ == '__main__':
    unittest.main()
