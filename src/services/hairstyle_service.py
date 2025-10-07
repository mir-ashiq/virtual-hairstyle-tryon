"""
Hairstyle transfer service - orchestrates the transfer process.
"""

from typing import Optional, Tuple, Callable
from pathlib import Path
from PIL import Image
import logging

from ..models import BarbershopModel
from ..utils import ImageValidator, ImageProcessor
from ..config import get_settings

logger = logging.getLogger(__name__)


class HairstyleTransferService:
    """Service for managing hairstyle transfer operations."""
    
    def __init__(self):
        """Initialize the hairstyle transfer service."""
        self.settings = get_settings()
        self.model = BarbershopModel()
        self.validator = ImageValidator()
        self.processor = ImageProcessor()
        self.logger = logger
    
    def initialize(self) -> bool:
        """
        Initialize the service and model.
        
        Returns:
            True if initialization successful
        """
        try:
            self.logger.info("Initializing hairstyle transfer service...")
            success = self.model.setup()
            if success:
                self.logger.info("Service initialized successfully")
            else:
                self.logger.error("Service initialization failed")
            return success
        except Exception as e:
            self.logger.error(f"Initialization error: {str(e)}")
            return False
    
    def validate_inputs(
        self,
        face_image: Optional[Image.Image],
        hairstyle_image: Optional[Image.Image]
    ) -> Tuple[bool, str]:
        """
        Validate input images.
        
        Args:
            face_image: Target face image
            hairstyle_image: Reference hairstyle image
            
        Returns:
            Tuple of (is_valid, message)
        """
        if face_image is None:
            return False, "Face image is required"
        
        if hairstyle_image is None:
            return False, "Hairstyle image is required"
        
        # Validate face image
        is_valid, msg = self.validator.validate_image(image=face_image)
        if not is_valid:
            return False, f"Face image validation failed: {msg}"
        
        # Validate hairstyle image
        is_valid, msg = self.validator.validate_image(image=hairstyle_image)
        if not is_valid:
            return False, f"Hairstyle image validation failed: {msg}"
        
        return True, "Validation passed"
    
    def preprocess_images(
        self,
        face_image: Image.Image,
        hairstyle_image: Image.Image,
        enhance: bool = False
    ) -> Tuple[Image.Image, Image.Image]:
        """
        Preprocess images before transfer.
        
        Args:
            face_image: Target face image
            hairstyle_image: Reference hairstyle image
            enhance: Whether to apply image enhancement
            
        Returns:
            Tuple of preprocessed images
        """
        # Convert to RGB
        face_image = self.processor.convert_to_rgb(face_image)
        hairstyle_image = self.processor.convert_to_rgb(hairstyle_image)
        
        # Optional enhancement
        if enhance:
            face_image = self.processor.enhance_image(
                face_image,
                brightness=1.05,
                contrast=1.05,
                sharpness=1.1
            )
            hairstyle_image = self.processor.enhance_image(
                hairstyle_image,
                brightness=1.05,
                contrast=1.05,
                sharpness=1.1
            )
        
        return face_image, hairstyle_image
    
    def transfer_hairstyle(
        self,
        face_image: Image.Image,
        hairstyle_image: Image.Image,
        style: str = "realistic",
        smoothness: int = 5,
        enhance: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> Tuple[Optional[Image.Image], str]:
        """
        Perform hairstyle transfer with full pipeline.
        
        Args:
            face_image: Target face image
            hairstyle_image: Reference hairstyle image
            style: Transfer style ('realistic' or 'fidelity')
            smoothness: Smoothness parameter (1-5)
            enhance: Whether to enhance images before processing
            progress_callback: Optional callback for progress updates
            
        Returns:
            Tuple of (result_image, log_message)
        """
        try:
            # Progress: Setup
            if progress_callback:
                progress_callback(0, desc="Setting up...")
            
            # Validate inputs
            if progress_callback:
                progress_callback(0.05, desc="Validating inputs...")
            
            is_valid, msg = self.validate_inputs(face_image, hairstyle_image)
            if not is_valid:
                self.logger.warning(f"Validation failed: {msg}")
                return None, f"❌ Validation Error: {msg}"
            
            # Preprocess images
            if progress_callback:
                progress_callback(0.1, desc="Preprocessing images...")
            
            face_image, hairstyle_image = self.preprocess_images(
                face_image,
                hairstyle_image,
                enhance=enhance
            )
            
            # Initialize model if needed
            if not self.model.is_initialized:
                if progress_callback:
                    progress_callback(0.15, desc="Initializing model...")
                
                if not self.initialize():
                    return None, "❌ Failed to initialize model"
            
            # Process transfer
            if progress_callback:
                progress_callback(0.2, desc="Processing hairstyle transfer...")
            
            result_image, log_msg = self.model.process(
                face_image,
                hairstyle_image,
                style=style,
                smoothness=smoothness
            )
            
            if progress_callback:
                progress_callback(1.0, desc="Complete!")
            
            return result_image, log_msg
            
        except Exception as e:
            self.logger.error(f"Transfer error: {str(e)}")
            return None, f"❌ Unexpected error: {str(e)}"
    
    def get_supported_styles(self) -> list:
        """
        Get list of supported transfer styles.
        
        Returns:
            List of style names
        """
        return ['realistic', 'fidelity']
    
    def get_model_info(self) -> dict:
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model information
        """
        return self.model.get_model_info()
