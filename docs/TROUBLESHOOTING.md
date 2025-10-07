# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Problem: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'gradio'
```

**Solution:**
```bash
pip install -r requirements.txt
```

#### Problem: CUDA not available
```
torch.cuda.is_available() returns False
```

**Solution:**
1. Check GPU drivers: `nvidia-smi`
2. Install CUDA toolkit
3. Reinstall PyTorch with CUDA:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Runtime Issues

#### Problem: Face alignment failed

**Symptoms:**
- Error message: "Face alignment failed"
- No aligned images produced

**Solutions:**
1. Ensure faces are clearly visible
2. Use front-facing photos
3. Check image quality (resolution, lighting)
4. Try different photos
5. Verify dlib is installed: `pip install dlib`

**Debug:**
```python
# Check if faces are detected
from src.models import BarbershopModel
model = BarbershopModel()
model.setup()
success, log = model.align_faces()
print(log)
```

#### Problem: Process timeout

**Symptoms:**
- Transfer takes too long
- "Process timed out" error

**Solutions:**
1. Reduce image size:
```python
from src.utils import ImageProcessor
processor = ImageProcessor()
face_img = processor.resize_image(face_img, max_width=512, max_height=512)
```

2. Increase timeout in settings:
```python
from src.config import get_settings
settings = get_settings()
settings.PROCESS_TIMEOUT = 600  # 10 minutes
```

3. Enable GPU acceleration
4. Reduce smoothness level

#### Problem: Out of memory

**Symptoms:**
- "CUDA out of memory" error
- Application crashes
- System becomes unresponsive

**Solutions:**
1. Reduce image sizes
2. Clear GPU cache:
```python
import torch
torch.cuda.empty_cache()
```

3. Reduce batch size
4. Use CPU instead of GPU
5. Increase system RAM/swap

### Validation Issues

#### Problem: Image validation failed

**Symptoms:**
- "Image width must be at least 256px"
- "Invalid image mode"
- "File size exceeds limit"

**Solutions:**
1. Check image dimensions:
```python
from PIL import Image
img = Image.open("photo.jpg")
print(img.size)  # Should be at least (256, 256)
```

2. Convert image format:
```python
img = img.convert('RGB')
img.save("converted.jpg")
```

3. Resize image if too large:
```python
max_size = 10 * 1024 * 1024  # 10MB
img.save("compressed.jpg", quality=85, optimize=True)
```

### Model Issues

#### Problem: Model not initializing

**Symptoms:**
- "Failed to initialize model"
- Barbershop repository not cloned

**Solutions:**
1. Check internet connection
2. Manually clone Barbershop:
```bash
git clone https://github.com/ZPdesu/Barbershop.git
```

3. Install ninja:
```bash
pip install ninja
```

4. Check permissions for creating directories

**Debug:**
```python
from src.models import BarbershopModel
model = BarbershopModel()
success = model.setup()
print(f"Setup successful: {success}")
```

#### Problem: Poor transfer quality

**Symptoms:**
- Unnatural results
- Hairstyle not blending well
- Artifacts in output

**Solutions:**
1. Try different style mode (realistic vs fidelity)
2. Adjust smoothness level (try 3-5)
3. Enable image enhancement
4. Use higher quality input images
5. Ensure similar lighting in both photos
6. Use front-facing photos

**Example:**
```python
# Try different settings
result1, _ = service.transfer_hairstyle(
    face, hair, style="realistic", smoothness=5, enhance=True
)
result2, _ = service.transfer_hairstyle(
    face, hair, style="fidelity", smoothness=3, enhance=False
)
```

### UI Issues

#### Problem: Gradio interface not loading

**Symptoms:**
- Blank page
- "Connection refused" error
- Port already in use

**Solutions:**
1. Check if port is available:
```bash
lsof -i :7860
```

2. Change port:
```python
demo.launch(server_port=7861)
```

3. Check firewall settings
4. Restart application

#### Problem: Upload not working

**Symptoms:**
- Cannot upload images
- Upload button not responsive

**Solutions:**
1. Check file size (must be under 10MB)
2. Verify file format (JPG, PNG only)
3. Clear browser cache
4. Try different browser
5. Check browser console for errors

### Performance Issues

#### Problem: Slow processing

**Symptoms:**
- Takes longer than 5 minutes
- UI freezes

**Solutions:**
1. Enable GPU if available
2. Reduce image sizes
3. Lower smoothness level
4. Close other applications
5. Check system resources:
```bash
htop  # or top
nvidia-smi  # for GPU
```

#### Problem: High memory usage

**Symptoms:**
- System slowdown
- Memory warnings

**Solutions:**
1. Restart application periodically
2. Clear temp directory:
```bash
rm -rf temp/*
```

3. Monitor memory:
```python
import psutil
print(f"Memory: {psutil.virtual_memory().percent}%")
```

4. Reduce concurrent requests

### Gallery Issues

#### Problem: Hairstyles not showing

**Symptoms:**
- Empty gallery
- Categories not loading

**Solutions:**
1. Check hairstyles directory exists:
```bash
ls -la hairstyles/
```

2. Verify directory structure:
```
hairstyles/
├── short/
├── medium/
├── long/
└── ...
```

3. Add sample images to categories

4. Check permissions:
```bash
chmod -R 755 hairstyles/
```

### Testing Issues

#### Problem: Tests failing

**Symptoms:**
- Test errors
- Import errors in tests

**Solutions:**
1. Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests from project root:
```bash
cd /path/to/virtual-hairstyle-tryon
python tests/run_tests.py
```

3. Check Python path:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Debug Mode

Enable debug mode for detailed logging:

```python
import logging
from src.utils import setup_logger

setup_logger(level=logging.DEBUG, log_file="debug.log")
```

Then check the log file:
```bash
tail -f debug.log
```

## Getting Help

### Before asking for help:

1. Check this troubleshooting guide
2. Review the documentation
3. Search existing GitHub issues
4. Check logs for error messages

### When reporting issues:

Include:
- Operating system and version
- Python version
- Error messages (full traceback)
- Steps to reproduce
- Input images (if relevant)
- Configuration settings

**Example Issue Report:**
```
**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.12
- CUDA: 11.8

**Issue:**
Face alignment fails for all images

**Error:**
[paste full error traceback]

**Steps to reproduce:**
1. Upload face.jpg
2. Upload hair.jpg
3. Click transfer
4. Error appears

**Logs:**
[paste relevant logs]
```

### Useful Commands

Check versions:
```bash
python --version
pip list | grep -i gradio
pip list | grep -i torch
nvidia-smi  # GPU info
```

Test model:
```python
from src.models import BarbershopModel
model = BarbershopModel()
print(model.get_model_info())
```

Verify installation:
```bash
python -c "from src.config import get_settings; print('OK')"
python -c "from src.models import BarbershopModel; print('OK')"
python -c "from src.services import HairstyleTransferService; print('OK')"
```

## FAQ

**Q: Why is processing so slow?**
A: Processing can take 3-5 minutes on CPU. Use GPU for faster results.

**Q: Can I use this offline?**
A: After initial setup (which requires internet to download the model), it can run offline.

**Q: What image formats are supported?**
A: JPG, JPEG, and PNG formats are supported.

**Q: What's the maximum image size?**
A: 10MB file size, but smaller images (1024x1024) work best.

**Q: Why don't some hairstyles work well?**
A: Results depend on image quality, lighting, and similarity between photos.

**Q: Can I add my own hairstyles to the gallery?**
A: Yes! Add images to the appropriate category in the `hairstyles/` directory.

**Q: Is GPU required?**
A: No, but highly recommended for faster processing.

**Q: How can I improve results?**
A: Use high-quality, front-facing photos with good lighting. Try different smoothness levels.

## Contact

If you still need help:
- Open an issue on GitHub
- Check the community forum
- Review the documentation
