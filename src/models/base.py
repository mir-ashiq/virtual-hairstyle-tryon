"""
Base model interface for hairstyle transfer models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class BaseModel(ABC):
    """Abstract base class for hairstyle transfer models."""
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize the model.
        
        Args:
            model_path: Path to model weights/config
        """
        self.model_path = model_path
        self.is_initialized = False
        self.logger = logger
    
    @abstractmethod
    def setup(self) -> bool:
        """
        Setup and initialize the model.
        
        Returns:
            True if setup successful, False otherwise
        """
        pass
    
    @abstractmethod
    def process(
        self,
        face_image: Image.Image,
        hairstyle_image: Image.Image,
        **kwargs
    ) -> Image.Image:
        """
        Process hairstyle transfer.
        
        Args:
            face_image: Target face image
            hairstyle_image: Reference hairstyle image
            **kwargs: Additional model-specific parameters
            
        Returns:
            Processed result image
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get model information.
        
        Returns:
            Dictionary with model metadata
        """
        pass
    
    def validate_setup(self) -> bool:
        """
        Validate model is properly set up.
        
        Returns:
            True if model is ready, False otherwise
        """
        return self.is_initialized
    
    def cleanup(self) -> None:
        """Cleanup model resources."""
        self.logger.info(f"Cleaning up {self.__class__.__name__}")
