"""
Image validation utilities.
"""

from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ImageValidator:
    """Validator for image files and content."""
    
    def __init__(self):
        self.settings = get_settings()
    
    def validate_file_size(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate image file size.
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            size = file_path.stat().st_size
            if size > self.settings.MAX_IMAGE_SIZE:
                max_mb = self.settings.MAX_IMAGE_SIZE / (1024 * 1024)
                return False, f"File size exceeds {max_mb:.1f}MB limit"
            return True, "File size is valid"
        except Exception as e:
            return False, f"Error checking file size: {str(e)}"
    
    def validate_file_type(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate image file type/extension.
        
        Args:
            file_path: Path to image file
            
        Returns:
            Tuple of (is_valid, message)
        """
        extension = file_path.suffix.lower()
        if extension not in self.settings.ALLOWED_EXTENSIONS:
            allowed = ", ".join(self.settings.ALLOWED_EXTENSIONS)
            return False, f"Invalid file type. Allowed: {allowed}"
        return True, "File type is valid"
    
    def validate_image_content(self, image: Image.Image) -> Tuple[bool, str]:
        """
        Validate image content and properties.
        
        Args:
            image: PIL Image object
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check image dimensions
        width, height = image.size
        
        if width < self.settings.MIN_IMAGE_WIDTH:
            return False, f"Image width must be at least {self.settings.MIN_IMAGE_WIDTH}px"
        
        if height < self.settings.MIN_IMAGE_HEIGHT:
            return False, f"Image height must be at least {self.settings.MIN_IMAGE_HEIGHT}px"
        
        # Check image mode
        if image.mode not in ['RGB', 'RGBA']:
            return False, f"Invalid image mode: {image.mode}. Expected RGB or RGBA"
        
        return True, "Image content is valid"
    
    def validate_image(
        self,
        image: Optional[Image.Image] = None,
        file_path: Optional[Path] = None
    ) -> Tuple[bool, str]:
        """
        Comprehensive image validation.
        
        Args:
            image: PIL Image object (optional)
            file_path: Path to image file (optional)
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Validate file if path provided
            if file_path:
                is_valid, msg = self.validate_file_type(file_path)
                if not is_valid:
                    return False, msg
                
                is_valid, msg = self.validate_file_size(file_path)
                if not is_valid:
                    return False, msg
                
                # Open image if not provided
                if image is None:
                    image = Image.open(file_path)
            
            # Validate image content
            if image is not None:
                is_valid, msg = self.validate_image_content(image)
                if not is_valid:
                    return False, msg
            
            return True, "All validations passed"
            
        except Exception as e:
            logger.error(f"Error during image validation: {str(e)}")
            return False, f"Validation error: {str(e)}"


def validate_image_file(file_path: Path) -> bool:
    """
    Quick validation for image file.
    
    Args:
        file_path: Path to image file
        
    Returns:
        True if valid, False otherwise
    """
    validator = ImageValidator()
    is_valid, _ = validator.validate_image(file_path=file_path)
    return is_valid
