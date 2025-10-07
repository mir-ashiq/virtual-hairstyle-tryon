"""Unit tests for configuration settings."""

import unittest
from pathlib import Path
from src.config import Settings, get_settings


class TestSettings(unittest.TestCase):
    """Test configuration settings."""
    
    def test_settings_initialization(self):
        """Test settings can be initialized."""
        settings = Settings()
        self.assertIsNotNone(settings)
        self.assertEqual(settings.APP_NAME, "Virtual Hairstyle Try-On")
        self.assertEqual(settings.APP_VERSION, "2.0.0")
    
    def test_settings_singleton(self):
        """Test settings returns same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        self.assertIs(settings1, settings2)
    
    def test_settings_paths(self):
        """Test that all required paths are defined."""
        settings = Settings()
        self.assertIsInstance(settings.BASE_DIR, Path)
        self.assertIsInstance(settings.BARBERSHOP_PATH, Path)
        self.assertIsInstance(settings.INPUT_DIR, Path)
        self.assertIsInstance(settings.OUTPUT_DIR, Path)
    
    def test_default_values(self):
        """Test default configuration values."""
        settings = Settings()
        self.assertEqual(settings.DEFAULT_STYLE, "realistic")
        self.assertEqual(settings.DEFAULT_SMOOTHNESS, 5)
        self.assertEqual(settings.PROCESS_TIMEOUT, 300)
    
    def test_allowed_extensions(self):
        """Test allowed file extensions."""
        settings = Settings()
        self.assertIn(".jpg", settings.ALLOWED_EXTENSIONS)
        self.assertIn(".jpeg", settings.ALLOWED_EXTENSIONS)
        self.assertIn(".png", settings.ALLOWED_EXTENSIONS)


if __name__ == '__main__':
    unittest.main()
