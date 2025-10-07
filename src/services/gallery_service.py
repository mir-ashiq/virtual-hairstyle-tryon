"""
Gallery service for managing hairstyle samples and collections.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PIL import Image
import logging

from ..config import get_settings

logger = logging.getLogger(__name__)


class HairstyleGalleryService:
    """Service for managing hairstyle gallery and samples."""
    
    def __init__(self):
        """Initialize the gallery service."""
        self.settings = get_settings()
        self.hairstyles_dir = self.settings.HAIRSTYLES_DIR
        self.examples_dir = self.settings.EXAMPLES_DIR
        self.hairstyles_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
        
        # Initialize gallery structure
        self._initialize_gallery()
    
    def _initialize_gallery(self) -> None:
        """Initialize gallery directory structure."""
        categories = [
            'short',
            'medium',
            'long',
            'curly',
            'straight',
            'wavy',
            'formal',
            'casual',
            'colored',
            'natural'
        ]
        
        for category in categories:
            category_path = self.hairstyles_dir / category
            category_path.mkdir(parents=True, exist_ok=True)
    
    def get_categories(self) -> List[str]:
        """
        Get list of hairstyle categories.
        
        Returns:
            List of category names
        """
        categories = [
            d.name for d in self.hairstyles_dir.iterdir()
            if d.is_dir()
        ]
        return sorted(categories)
    
    def get_hairstyles_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        Get hairstyles in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            List of dictionaries with hairstyle info
        """
        category_path = self.hairstyles_dir / category
        
        if not category_path.exists():
            self.logger.warning(f"Category not found: {category}")
            return []
        
        hairstyles = []
        for img_path in category_path.glob("*"):
            if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                hairstyles.append({
                    'name': img_path.stem,
                    'path': str(img_path),
                    'category': category
                })
        
        return hairstyles
    
    def get_all_hairstyles(self) -> List[Dict[str, str]]:
        """
        Get all hairstyles from all categories.
        
        Returns:
            List of dictionaries with hairstyle info
        """
        all_hairstyles = []
        
        for category in self.get_categories():
            hairstyles = self.get_hairstyles_by_category(category)
            all_hairstyles.extend(hairstyles)
        
        return all_hairstyles
    
    def get_example_pairs(self) -> List[Tuple[str, str]]:
        """
        Get example face-hairstyle pairs for demos.
        
        Returns:
            List of tuples (face_path, hairstyle_path)
        """
        if not self.examples_dir.exists():
            return []
        
        pairs = []
        
        # Look for paired examples (face1.png + hair1.png, etc.)
        face_files = sorted(self.examples_dir.glob("*face*.png"))
        hair_files = sorted(self.examples_dir.glob("*hair*.png"))
        
        for face_file in face_files:
            # Try to find matching hair file
            face_num = ''.join(filter(str.isdigit, face_file.stem))
            if face_num:
                hair_file = self.examples_dir / f"hair{face_num}.png"
                if not hair_file.exists():
                    hair_file = self.examples_dir / f"example_hair{face_num}.png"
                
                if hair_file.exists():
                    pairs.append((str(face_file), str(hair_file)))
        
        # Also check for generic examples
        generic_face = self.examples_dir / "example_face.png"
        generic_hair = self.examples_dir / "example_hair.png"
        
        if generic_face.exists() and generic_hair.exists():
            if (str(generic_face), str(generic_hair)) not in pairs:
                pairs.append((str(generic_face), str(generic_hair)))
        
        return pairs
    
    def add_hairstyle(
        self,
        image: Image.Image,
        name: str,
        category: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Add a new hairstyle to the gallery.
        
        Args:
            image: PIL Image of the hairstyle
            name: Name for the hairstyle
            category: Category to add to
            metadata: Optional metadata dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            category_path = self.hairstyles_dir / category
            category_path.mkdir(parents=True, exist_ok=True)
            
            # Save image
            image_path = category_path / f"{name}.png"
            image.save(image_path)
            
            # Save metadata if provided
            if metadata:
                metadata_path = category_path / f"{name}.json"
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Added hairstyle '{name}' to category '{category}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add hairstyle: {str(e)}")
            return False
    
    def get_gallery_stats(self) -> Dict[str, int]:
        """
        Get statistics about the gallery.
        
        Returns:
            Dictionary with gallery statistics
        """
        stats = {
            'total_categories': len(self.get_categories()),
            'total_hairstyles': len(self.get_all_hairstyles()),
            'total_examples': len(self.get_example_pairs())
        }
        
        # Per-category counts
        for category in self.get_categories():
            count = len(self.get_hairstyles_by_category(category))
            stats[f'category_{category}'] = count
        
        return stats
