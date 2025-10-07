"""
Configuration settings for the Virtual Hairstyle Try-On application.
"""

import os
from typing import Optional
from pathlib import Path


class Settings:
    """Application settings and configuration."""
    
    # Application metadata
    APP_NAME: str = "Virtual Hairstyle Try-On"
    APP_VERSION: str = "2.0.0"
    
    # Directory paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    BARBERSHOP_PATH: Path = BASE_DIR / "Barbershop"
    INPUT_DIR: Path = BARBERSHOP_PATH / "input"
    UNPROCESSED_DIR: Path = BARBERSHOP_PATH / "unprocessed"
    OUTPUT_DIR: Path = BARBERSHOP_PATH / "output"
    DATA_DIR: Path = BASE_DIR / "data"
    EXAMPLES_DIR: Path = BASE_DIR / "examples"
    HAIRSTYLES_DIR: Path = BASE_DIR / "hairstyles"
    TEMP_DIR: Path = BASE_DIR / "temp"
    
    # Model settings
    MODEL_NAME: str = "Barbershop"
    MODEL_REPO_URL: str = "https://github.com/ZPdesu/Barbershop.git"
    DEFAULT_STYLE: str = os.getenv("BARBERSHOP_STYLE", "realistic")
    DEFAULT_SMOOTHNESS: int = int(os.getenv("BARBERSHOP_SMOOTH", "5"))
    
    # Processing settings
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png"}
    PROCESS_TIMEOUT: int = 300  # 5 minutes
    ALIGNMENT_SEED: int = 42
    
    # Server settings
    SERVER_HOST: str = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    GRADIO_ANALYTICS: bool = os.getenv("GRADIO_ANALYTICS_ENABLED", "False").lower() == "true"
    
    # UI settings
    THEME_PRIMARY_HUE: str = "blue"
    THEME_SECONDARY_HUE: str = "cyan"
    MAX_CONTAINER_WIDTH: str = "1400px"
    
    # Feature flags
    ENABLE_WEBCAM: bool = True
    ENABLE_BATCH_PROCESSING: bool = True
    ENABLE_HISTORY: bool = True
    ENABLE_QUALITY_CHECKS: bool = True
    
    # Quality thresholds
    MIN_IMAGE_WIDTH: int = 256
    MIN_IMAGE_HEIGHT: int = 256
    MIN_FACE_CONFIDENCE: float = 0.5
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        directories = [
            cls.BARBERSHOP_PATH,
            cls.INPUT_DIR,
            cls.UNPROCESSED_DIR,
            cls.OUTPUT_DIR,
            cls.HAIRSTYLES_DIR,
            cls.TEMP_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_directories()
    return _settings
