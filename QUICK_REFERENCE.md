# Quick Reference Guide

## Installation

```bash
# Automated setup (recommended)
python setup.py

# Manual setup
pip install -r requirements.txt
```

## Running the Application

```bash
# Enhanced version (recommended)
python app_enhanced.py

# Original version
python app.py
```

## Basic Usage

### Programmatic API

```python
from src.services import HairstyleTransferService
from PIL import Image

# Initialize service
service = HairstyleTransferService()
service.initialize()

# Load images
face = Image.open("face.jpg")
hairstyle = Image.open("hairstyle.jpg")

# Transfer hairstyle
result, log = service.transfer_hairstyle(
    face_image=face,
    hairstyle_image=hairstyle,
    style="realistic",      # or "fidelity"
    smoothness=5,           # 1-5
    enhance=False          # optional enhancement
)

# Save result
if result:
    result.save("output.png")
```

### Web UI

1. Run: `python app_enhanced.py`
2. Open: http://localhost:7860
3. Upload face and hairstyle images
4. Adjust settings
5. Click "Transfer Hairstyle"

## Common Tasks

### Run Tests
```bash
python tests/run_tests.py
```

### Format Code
```bash
black src/ tests/ app_enhanced.py
isort src/ tests/ app_enhanced.py
```

### Check Code Quality
```bash
flake8 src/ tests/ app_enhanced.py
```

### Run Examples
```bash
python examples/api_examples.py
```

### View Documentation
- API: `docs/api/API.md`
- Architecture: `docs/ARCHITECTURE.md`
- Performance: `docs/PERFORMANCE.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

## Configuration

### Environment Variables
```bash
export GRADIO_SERVER_PORT="7860"
export BARBERSHOP_STYLE="realistic"
export BARBERSHOP_SMOOTH="5"
```

### Settings in Code
```python
from src.config import get_settings

settings = get_settings()
settings.DEFAULT_STYLE = "fidelity"
settings.PROCESS_TIMEOUT = 600
```

## Key Components

### Services
- `HairstyleTransferService` - Main transfer logic
- `HairstyleGalleryService` - Gallery management

### Models
- `BarbershopModel` - Hairstyle transfer model
- `BaseModel` - Abstract base class

### Utilities
- `ImageValidator` - Input validation
- `ImageProcessor` - Image processing
- `setup_logger()` - Logging setup

## Troubleshooting

### Face alignment failed
- Ensure clear, front-facing photos
- Check image quality and lighting
- Try different images

### Process timeout
- Reduce image size
- Increase timeout setting
- Enable GPU if available

### Out of memory
- Reduce image dimensions
- Clear GPU cache: `torch.cuda.empty_cache()`
- Use CPU instead of GPU

### Poor results
- Try different style (realistic vs fidelity)
- Adjust smoothness level
- Enable image enhancement
- Use higher quality inputs

## File Structure

```
virtual-hairstyle-tryon/
├── src/               # Source code
│   ├── config/       # Configuration
│   ├── models/       # AI models
│   ├── services/     # Business logic
│   └── utils/        # Utilities
├── tests/            # Test suite
├── docs/             # Documentation
├── hairstyles/       # Gallery
├── examples/         # Examples
└── app_enhanced.py   # Main app
```

## Supported Formats

- **Images**: JPG, JPEG, PNG
- **Max Size**: 10MB
- **Min Dimensions**: 256x256 pixels

## Transfer Styles

- **realistic**: Natural-looking blend (recommended)
- **fidelity**: Preserves more details

## Smoothness Levels

- **1-2**: Minimal smoothing
- **3**: Balanced (recommended)
- **4-5**: Maximum smoothing

## API Access

### Gradio Client
```python
from gradio_client import Client

client = Client("YOUR_SPACE_URL")
result = client.predict(
    face_img,
    hair_img,
    "realistic",
    5,
    False
)
```

## Gallery Categories

- Short, Medium, Long
- Curly, Straight, Wavy
- Formal, Casual
- Colored, Natural

## Support

- Issues: GitHub Issues
- Docs: `docs/` directory
- Examples: `examples/api_examples.py`

## Version

- Current: 2.0.0
- Type: Enterprise Edition
- Status: Production Ready
