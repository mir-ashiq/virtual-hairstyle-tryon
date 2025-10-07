"""
Barbershop model implementation for hairstyle transfer.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image
import logging

from .base import BaseModel
from ..config import get_settings

logger = logging.getLogger(__name__)


class BarbershopModel(BaseModel):
    """Barbershop GAN-based hairstyle transfer model."""
    
    def __init__(self):
        """Initialize Barbershop model."""
        super().__init__()
        self.settings = get_settings()
        self.barbershop_path = self.settings.BARBERSHOP_PATH
        self.input_dir = self.settings.INPUT_DIR
        self.unprocessed_dir = self.settings.UNPROCESSED_DIR
        self.output_dir = self.settings.OUTPUT_DIR
    
    def setup(self) -> bool:
        """
        Setup Barbershop model and dependencies.
        
        Returns:
            True if setup successful, False otherwise
        """
        try:
            # Check if key files exist instead of just directory
            align_face_script = self.barbershop_path / "align_face.py"
            main_script = self.barbershop_path / "main.py"
            
            if not align_face_script.exists() or not main_script.exists():
                logger.info("Setting up Barbershop repository...")
                
                # Remove existing directory if it's incomplete
                if self.barbershop_path.exists():
                    import shutil
                    shutil.rmtree(self.barbershop_path)
                
                logger.info("Cloning Barbershop repository...")
                subprocess.run(
                    ["git", "clone", self.settings.MODEL_REPO_URL, str(self.barbershop_path)],
                    check=True,
                    capture_output=True
                )
                
                # Install ninja
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "ninja"],
                    check=True,
                    capture_output=True
                )
                
                # Remove default image if exists
                default_img = self.unprocessed_dir / "90.jpg"
                if default_img.exists():
                    default_img.unlink()
            
            # Ensure directories exist
            self.settings.ensure_directories()
            
            self.is_initialized = True
            logger.info("Barbershop model setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup Barbershop model: {str(e)}")
            return False
    
    def align_faces(self) -> Tuple[bool, str]:
        """
        Run face alignment preprocessing.
        
        Returns:
            Tuple of (success, log_message)
        """
        current_dir = os.getcwd()
        try:
            os.chdir(self.barbershop_path)
            result = subprocess.run(
                [sys.executable, "align_face.py", "-seed", str(self.settings.ALIGNMENT_SEED)],
                capture_output=True,
                text=True,
                timeout=60
            )
            os.chdir(current_dir)
            
            success = result.returncode == 0
            log_msg = result.stdout + result.stderr
            
            if success:
                logger.info("Face alignment successful")
            else:
                logger.warning(f"Face alignment failed: {log_msg}")
            
            return success, log_msg
            
        except subprocess.TimeoutExpired:
            os.chdir(current_dir)
            logger.error("Face alignment timed out")
            return False, "Face alignment timed out after 60 seconds"
        except Exception as e:
            os.chdir(current_dir)
            logger.error(f"Face alignment error: {str(e)}")
            return False, str(e)
    
    def get_aligned_images(self) -> list:
        """
        Get list of aligned images.
        
        Returns:
            List of aligned image filenames
        """
        if self.input_dir.exists():
            aligned = [
                f for f in os.listdir(self.input_dir)
                if f.endswith(('.png', '.jpg', '.jpeg'))
            ]
            logger.info(f"Found {len(aligned)} aligned images")
            return aligned
        return []
    
    def save_image(self, image: Image.Image, filename: str) -> Optional[Path]:
        """
        Save image to unprocessed directory.
        
        Args:
            image: PIL Image to save
            filename: Target filename
            
        Returns:
            Path to saved file or None if failed
        """
        try:
            filepath = self.unprocessed_dir / filename
            image.save(filepath)
            logger.info(f"Saved image to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save image: {str(e)}")
            return None
    
    def clear_unprocessed(self) -> None:
        """Clear previous unprocessed images."""
        try:
            for f in os.listdir(self.unprocessed_dir):
                if f.endswith(('.png', '.jpg', '.jpeg')):
                    (self.unprocessed_dir / f).unlink()
            logger.info("Cleared unprocessed directory")
        except Exception as e:
            logger.warning(f"Failed to clear unprocessed directory: {str(e)}")
    
    def process(
        self,
        face_image: Image.Image,
        hairstyle_image: Image.Image,
        style: str = "realistic",
        smoothness: int = 5,
        **kwargs
    ) -> Tuple[Optional[Image.Image], str]:
        """
        Process hairstyle transfer.
        
        Args:
            face_image: Target face image
            hairstyle_image: Reference hairstyle image
            style: Transfer style ('realistic' or 'fidelity')
            smoothness: Smoothness parameter (1-5)
            
        Returns:
            Tuple of (result_image, log_message)
        """
        try:
            # Setup if needed
            if not self.is_initialized:
                if not self.setup():
                    return None, "Failed to initialize model"
            
            # Clear previous images
            self.clear_unprocessed()
            
            # Save input images
            face_path = self.save_image(face_image, "face.png")
            hair_path = self.save_image(hairstyle_image, "hair.png")
            
            if not face_path or not hair_path:
                return None, "Error: Could not save input images"
            
            # Align faces
            success, align_log = self.align_faces()
            if not success:
                return None, f"Face alignment failed:\n{align_log}"
            
            # Get aligned images
            aligned_imgs = self.get_aligned_images()
            if len(aligned_imgs) < 2:
                return None, f"Face alignment produced {len(aligned_imgs)} images. Need at least 2.\n{align_log}"
            
            # Sort for consistency
            aligned_imgs.sort()
            face_aligned = aligned_imgs[0]
            hair_aligned = aligned_imgs[1]
            
            # Run hairstyle transfer
            current_dir = os.getcwd()
            try:
                os.chdir(self.barbershop_path)
                
                cmd = [
                    sys.executable, "main.py",
                    "--im_path1", face_aligned,
                    "--im_path2", hair_aligned,
                    "--im_path3", hair_aligned,
                    "--sign", style,
                    "--smooth", str(smoothness)
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=self.settings.PROCESS_TIMEOUT
                )
                
                os.chdir(current_dir)
                
                # Find output image
                output_path = self.output_dir / f"Blend_{style}"
                if output_path.exists():
                    output_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
                    if output_files:
                        # Get the latest output
                        output_files.sort(
                            key=lambda x: os.path.getmtime(output_path / x),
                            reverse=True
                        )
                        result_img_path = output_path / output_files[0]
                        result_img = Image.open(result_img_path)
                        
                        log_msg = f"✅ Success!\n\nAligned images: {face_aligned}, {hair_aligned}\n\n"
                        log_msg += f"Style: {style}, Smoothness: {smoothness}\n\n"
                        log_msg += "Process output:\n" + (
                            result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
                        )
                        
                        logger.info("Hairstyle transfer completed successfully")
                        return result_img, log_msg
                
                return None, f"Output image not found. Check logs:\n{result.stdout}\n{result.stderr}"
                
            except subprocess.TimeoutExpired:
                os.chdir(current_dir)
                logger.error("Process timed out")
                return None, f"Process timed out after {self.settings.PROCESS_TIMEOUT} seconds"
            except Exception as e:
                os.chdir(current_dir)
                logger.error(f"Transfer error: {str(e)}")
                return None, f"Error during transfer: {str(e)}"
                
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None, f"Unexpected error: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get Barbershop model information.
        
        Returns:
            Dictionary with model metadata
        """
        return {
            'name': 'Barbershop',
            'version': '1.0',
            'architecture': 'StyleGAN2-based',
            'paper': 'https://arxiv.org/abs/2106.01505',
            'repository': 'https://github.com/ZPdesu/Barbershop',
            'authors': 'Zhu et al.',
            'year': 2021,
            'supported_styles': ['realistic', 'fidelity'],
            'smoothness_range': [1, 5],
            'is_initialized': self.is_initialized
        }
