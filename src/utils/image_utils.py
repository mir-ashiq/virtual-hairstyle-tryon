"""
Image processing utilities.
"""

import io
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Image processing and enhancement utilities."""
    
    @staticmethod
    def resize_image(
        image: Image.Image,
        max_width: int = 1024,
        max_height: int = 1024,
        maintain_aspect: bool = True
    ) -> Image.Image:
        """
        Resize image while maintaining aspect ratio.
        
        Args:
            image: PIL Image to resize
            max_width: Maximum width
            max_height: Maximum height
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized PIL Image
        """
        width, height = image.size
        
        if maintain_aspect:
            # Calculate scaling factor
            scale = min(max_width / width, max_height / height)
            if scale < 1:  # Only resize if image is larger
                new_width = int(width * scale)
                new_height = int(height * scale)
                return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            return image.resize((max_width, max_height), Image.Resampling.LANCZOS)
        
        return image
    
    @staticmethod
    def enhance_image(
        image: Image.Image,
        brightness: float = 1.0,
        contrast: float = 1.0,
        sharpness: float = 1.0,
        color: float = 1.0
    ) -> Image.Image:
        """
        Enhance image with various filters.
        
        Args:
            image: PIL Image to enhance
            brightness: Brightness factor (1.0 = no change)
            contrast: Contrast factor (1.0 = no change)
            sharpness: Sharpness factor (1.0 = no change)
            color: Color saturation factor (1.0 = no change)
            
        Returns:
            Enhanced PIL Image
        """
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast)
        
        if sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness)
        
        if color != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(color)
        
        return image
    
    @staticmethod
    def convert_to_rgb(image: Image.Image) -> Image.Image:
        """
        Convert image to RGB mode.
        
        Args:
            image: PIL Image
            
        Returns:
            RGB PIL Image
        """
        if image.mode != 'RGB':
            return image.convert('RGB')
        return image
    
    @staticmethod
    def apply_blur(image: Image.Image, radius: int = 2) -> Image.Image:
        """
        Apply Gaussian blur to image.
        
        Args:
            image: PIL Image
            radius: Blur radius
            
        Returns:
            Blurred PIL Image
        """
        return image.filter(ImageFilter.GaussianBlur(radius))
    
    @staticmethod
    def crop_center(
        image: Image.Image,
        target_width: int,
        target_height: int
    ) -> Image.Image:
        """
        Crop image from center.
        
        Args:
            image: PIL Image to crop
            target_width: Target width
            target_height: Target height
            
        Returns:
            Cropped PIL Image
        """
        width, height = image.size
        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return image.crop((left, top, right, bottom))
    
    @staticmethod
    def get_image_stats(image: Image.Image) -> dict:
        """
        Get statistics about the image.
        
        Args:
            image: PIL Image
            
        Returns:
            Dictionary with image statistics
        """
        img_array = np.array(image)
        
        stats = {
            'width': image.size[0],
            'height': image.size[1],
            'mode': image.mode,
            'format': image.format,
            'mean_intensity': float(np.mean(img_array)),
            'std_intensity': float(np.std(img_array)),
            'min_intensity': int(np.min(img_array)),
            'max_intensity': int(np.max(img_array)),
        }
        
        return stats
    
    @staticmethod
    def save_image_optimized(
        image: Image.Image,
        output_path: Path,
        quality: int = 95,
        optimize: bool = True
    ) -> None:
        """
        Save image with optimization.
        
        Args:
            image: PIL Image to save
            output_path: Path to save image
            quality: JPEG quality (1-100)
            optimize: Whether to optimize file size
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_path.suffix.lower() in ['.jpg', '.jpeg']:
            image.save(output_path, 'JPEG', quality=quality, optimize=optimize)
        else:
            image.save(output_path, optimize=optimize)
