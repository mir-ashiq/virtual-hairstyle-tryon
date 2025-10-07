# API Documentation

## Overview

The Virtual Hairstyle Try-On application provides a comprehensive API for hairstyle transfer operations.

## Core Components

### Configuration (`src.config`)

#### Settings Class

Manages all application configuration and settings.

```python
from src.config import get_settings

settings = get_settings()
print(settings.APP_NAME)
print(settings.DEFAULT_STYLE)
```

**Key Settings:**
- `APP_NAME`: Application name
- `APP_VERSION`: Current version
- `DEFAULT_STYLE`: Default transfer style ("realistic" or "fidelity")
- `DEFAULT_SMOOTHNESS`: Default smoothness level (1-5)
- `PROCESS_TIMEOUT`: Maximum processing time in seconds

### Models (`src.models`)

#### BarbershopModel

Main model class for hairstyle transfer.

```python
from src.models import BarbershopModel
from PIL import Image

model = BarbershopModel()
model.setup()

face_img = Image.open("face.jpg")
hair_img = Image.open("hairstyle.jpg")

result, log = model.process(
    face_image=face_img,
    hairstyle_image=hair_img,
    style="realistic",
    smoothness=5
)
```

**Methods:**
- `setup()`: Initialize the model
- `process(face_image, hairstyle_image, **kwargs)`: Perform transfer
- `get_model_info()`: Get model metadata
- `align_faces()`: Run face alignment
- `get_aligned_images()`: Get aligned image list

### Services (`src.services`)

#### HairstyleTransferService

High-level service for hairstyle transfer operations.

```python
from src.services import HairstyleTransferService
from PIL import Image

service = HairstyleTransferService()
service.initialize()

face_img = Image.open("face.jpg")
hair_img = Image.open("hairstyle.jpg")

result, log = service.transfer_hairstyle(
    face_image=face_img,
    hairstyle_image=hair_img,
    style="realistic",
    smoothness=5,
    enhance=True
)
```

**Methods:**
- `initialize()`: Initialize the service
- `transfer_hairstyle(...)`: Full transfer pipeline
- `validate_inputs(...)`: Validate input images
- `preprocess_images(...)`: Preprocess images
- `get_supported_styles()`: Get available styles
- `get_model_info()`: Get model information

#### HairstyleGalleryService

Manages hairstyle gallery and collections.

```python
from src.services import HairstyleGalleryService

gallery = HairstyleGalleryService()

# Get all categories
categories = gallery.get_categories()

# Get hairstyles in a category
hairstyles = gallery.get_hairstyles_by_category("short")

# Get statistics
stats = gallery.get_gallery_stats()

# Get example pairs
examples = gallery.get_example_pairs()
```

**Methods:**
- `get_categories()`: Get list of categories
- `get_hairstyles_by_category(category)`: Get hairstyles by category
- `get_all_hairstyles()`: Get all hairstyles
- `get_example_pairs()`: Get example image pairs
- `add_hairstyle(...)`: Add new hairstyle to gallery
- `get_gallery_stats()`: Get gallery statistics

### Utilities (`src.utils`)

#### ImageValidator

Validates image files and content.

```python
from src.utils import ImageValidator
from PIL import Image

validator = ImageValidator()

# Validate image
is_valid, message = validator.validate_image(image=img)

# Validate file
is_valid, message = validator.validate_image(file_path=path)
```

**Methods:**
- `validate_file_size(file_path)`: Check file size
- `validate_file_type(file_path)`: Check file extension
- `validate_image_content(image)`: Check image properties
- `validate_image(...)`: Comprehensive validation

#### ImageProcessor

Image processing and enhancement utilities.

```python
from src.utils import ImageProcessor
from PIL import Image

processor = ImageProcessor()

# Resize image
resized = processor.resize_image(img, max_width=1024, max_height=1024)

# Enhance image
enhanced = processor.enhance_image(
    img,
    brightness=1.1,
    contrast=1.1,
    sharpness=1.2
)

# Convert to RGB
rgb_img = processor.convert_to_rgb(img)

# Get statistics
stats = processor.get_image_stats(img)
```

**Methods:**
- `resize_image(...)`: Resize with aspect ratio
- `enhance_image(...)`: Apply enhancements
- `convert_to_rgb(...)`: Convert to RGB mode
- `apply_blur(...)`: Apply Gaussian blur
- `crop_center(...)`: Crop from center
- `get_image_stats(...)`: Get image statistics
- `save_image_optimized(...)`: Save with optimization

#### Logger

Logging utilities.

```python
from src.utils import setup_logger, get_logger

# Setup logger
logger = setup_logger(name="my_app", level=logging.INFO)

# Get existing logger
logger = get_logger("my_app")

logger.info("Processing started")
logger.error("An error occurred")
```

## Error Handling

All services and utilities provide comprehensive error handling:

```python
try:
    result, log = service.transfer_hairstyle(face_img, hair_img)
    if result is None:
        print(f"Transfer failed: {log}")
    else:
        result.save("output.png")
except Exception as e:
    print(f"Error: {str(e)}")
```

## Examples

### Basic Transfer

```python
from src.services import HairstyleTransferService
from PIL import Image

service = HairstyleTransferService()
service.initialize()

face = Image.open("my_face.jpg")
hairstyle = Image.open("desired_style.jpg")

result, log = service.transfer_hairstyle(
    face_image=face,
    hairstyle_image=hairstyle,
    style="realistic",
    smoothness=5
)

if result:
    result.save("result.png")
    print("Success!")
else:
    print(f"Failed: {log}")
```

### With Enhancement

```python
result, log = service.transfer_hairstyle(
    face_image=face,
    hairstyle_image=hairstyle,
    style="fidelity",
    smoothness=3,
    enhance=True  # Enable image enhancement
)
```

### Using Gallery

```python
from src.services import HairstyleGalleryService

gallery = HairstyleGalleryService()

# Browse hairstyles
for category in gallery.get_categories():
    hairstyles = gallery.get_hairstyles_by_category(category)
    print(f"{category}: {len(hairstyles)} hairstyles")
    
    for h in hairstyles:
        print(f"  - {h['name']}")
```

### Validation

```python
from src.utils import ImageValidator
from PIL import Image

validator = ImageValidator()

img = Image.open("photo.jpg")
is_valid, message = validator.validate_image(image=img)

if not is_valid:
    print(f"Validation failed: {message}")
else:
    # Proceed with transfer
    pass
```

## Response Formats

### Transfer Response

```python
(result_image, log_message)
```

- `result_image`: PIL.Image.Image or None if failed
- `log_message`: String with processing logs

### Validation Response

```python
(is_valid, message)
```

- `is_valid`: Boolean indicating validation status
- `message`: String with validation details

### Model Info Response

```python
{
    'name': 'Barbershop',
    'version': '1.0',
    'architecture': 'StyleGAN2-based',
    'paper': 'https://arxiv.org/abs/2106.01505',
    'repository': 'https://github.com/ZPdesu/Barbershop',
    'authors': 'Zhu et al.',
    'year': 2021,
    'supported_styles': ['realistic', 'fidelity'],
    'smoothness_range': [1, 5],
    'is_initialized': True
}
```

## Configuration

### Environment Variables

```bash
# Gradio settings
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"
export GRADIO_ANALYTICS_ENABLED="False"

# Model settings
export BARBERSHOP_STYLE="realistic"
export BARBERSHOP_SMOOTH="5"
```

### Programmatic Configuration

```python
from src.config import get_settings

settings = get_settings()
settings.DEFAULT_STYLE = "fidelity"
settings.DEFAULT_SMOOTHNESS = 3
settings.PROCESS_TIMEOUT = 600
```

## Best Practices

1. **Always initialize services before use**
   ```python
   service = HairstyleTransferService()
   service.initialize()
   ```

2. **Validate inputs before processing**
   ```python
   is_valid, msg = service.validate_inputs(face_img, hair_img)
   if not is_valid:
       return
   ```

3. **Handle errors gracefully**
   ```python
   try:
       result, log = service.transfer_hairstyle(...)
   except Exception as e:
       logger.error(f"Transfer failed: {e}")
   ```

4. **Use logging for debugging**
   ```python
   from src.utils import get_logger
   logger = get_logger(__name__)
   logger.info("Processing started")
   ```

5. **Clean up resources**
   ```python
   model.cleanup()
   ```
