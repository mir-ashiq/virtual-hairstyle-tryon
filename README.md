# 🎨 Virtual Hairstyle Try-On with Barbershop Model

[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/YOUR_USERNAME/virtual-hairstyle-tryon)

An interactive web application for AI-powered hairstyle transfer using the Barbershop model. Try on different hairstyles from reference photos with realistic results!

## 🌟 Features

- **Interactive Web UI**: User-friendly Gradio interface for easy hairstyle transfer
- **Real-time Processing**: Upload photos and get results in minutes
- **Advanced Controls**: Adjustable style and smoothness parameters
- **Webcam Support**: Take photos directly from your camera
- **Multiple Style Modes**: Choose between realistic and fidelity transfer modes
- **Detailed Logs**: Track the processing steps and results

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/mir-ashiq/virtual-hairstyle-tryon.git
cd virtual-hairstyle-tryon
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
Navigate to `http://localhost:7860`

### Hugging Face Spaces Deployment

#### One-Click Deployment

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Space name**: virtual-hairstyle-tryon
   - **License**: MIT
   - **Space SDK**: Gradio
   - **Space hardware**: CPU basic (or GPU for faster processing)
4. Clone this repository to your Space
5. The app will automatically deploy!

#### Manual Deployment

1. **Create a new Space on Hugging Face**
```bash
# Install huggingface_hub
pip install huggingface_hub

# Login to Hugging Face
huggingface-cli login
```

2. **Push to Hugging Face**
```bash
# Add Hugging Face as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/virtual-hairstyle-tryon

# Push to Hugging Face
git push hf main
```

3. **Configure Space Settings**
- Go to your Space settings on Hugging Face
- Set SDK to "Gradio"
- Set Python version to 3.10 or higher
- (Optional) Enable GPU for faster processing

## 📖 How to Use

1. **Upload Your Face Photo**: The person who will receive the new hairstyle
2. **Upload Hairstyle Reference**: A photo with the desired hairstyle
3. **Adjust Settings**:
   - **Style**: Choose between "realistic" (natural blend) or "fidelity" (preserves details)
   - **Smoothness**: Higher values create smoother transitions (1-5)
4. **Click "Transfer Hairstyle"**: Wait 3-5 minutes for processing
5. **Download Result**: Save your new look!

## 💡 Tips for Best Results

✅ **Do:**
- Use clear, front-facing photos
- Ensure faces are well-lit and visible
- Use similar quality photos for both inputs
- Try different smoothness values for best results

❌ **Avoid:**
- Blurry or low-resolution images
- Extreme angles or partial faces
- Heavily filtered or edited photos
- Images with multiple faces

## 🔧 Technical Details

### Model Information

This application uses the **Barbershop** model for hairstyle transfer:
- **Paper**: [Barbershop: GAN-based Image Compositing using Segmentation Masks](https://arxiv.org/abs/2106.01505)
- **Authors**: Zhu et al. (2021)
- **Architecture**: Based on StyleGAN2
- **Original Repository**: [ZPdesu/Barbershop](https://github.com/ZPdesu/Barbershop)

### Processing Pipeline

1. **Face Alignment**: Detects and aligns facial features in both images
2. **Embedding**: Encodes images into StyleGAN2 latent space (1100 iterations)
3. **Transfer**: Blends hairstyle from reference to target face
4. **Refinement**: Applies smoothing for natural-looking results

### Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA (optional, for GPU acceleration)
- 4GB+ RAM (8GB+ recommended)
- Processing time: 3-5 minutes per transfer (CPU), 1-2 minutes (GPU)

## 📁 Repository Structure

```
virtual-hairstyle-tryon/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore patterns
├── code/                # Analysis scripts
│   └── image_processor.py
├── data/                # Sample datasets
│   ├── II2S_Images/
│   └── actors/
├── notebooks/           # Jupyter notebooks
│   ├── 01-Exploratory-Data-Analysis.ipynb
│   └── 02-Barbershop-Model.ipynb
└── output/             # Generated results
```

## 🎯 Research & Analysis

This repository also contains research notebooks for analyzing the Barbershop model:

- **`notebooks/01-Exploratory-Data-Analysis.ipynb`**: EDA of the image dataset
- **`notebooks/02-Barbershop-Model.ipynb`**: Model testing and analysis
- **`code/image_processor.py`**: Image property analysis utilities

The Barbershop model has been tested on datasets featuring Thai actors/actresses and Thai friends from school as part of a school project in Harbour Space University.

## 📊 Sample Results

<img width="1078" alt="Screenshot 2024-03-05 at 7 40 18 PM" src="https://github.com/ginoasuncion/virtual-hairstyle-tryon/assets/13530187/6e669ba0-81a8-4a81-931d-c41a34254fdf">

<img width="1078" alt="Screenshot 2024-03-05 at 7 40 08 PM" src="https://github.com/ginoasuncion/virtual-hairstyle-tryon/assets/13530187/ee5a0ae7-90a5-4881-98f6-40087982f1cb">

## 🛠️ Configuration

### Environment Variables

You can configure the app using environment variables:

```bash
# Gradio settings
export GRADIO_SERVER_NAME="0.0.0.0"
export GRADIO_SERVER_PORT="7860"

# Model settings (optional)
export BARBERSHOP_SMOOTH=5
export BARBERSHOP_STYLE="realistic"
```

### Advanced Settings

Edit `app.py` to modify:
- Transfer parameters (style, smoothness)
- UI theme and styling
- Processing timeouts
- Image size limits

## 🐛 Troubleshooting

### Common Issues

**"Face alignment failed"**
- Ensure faces are clearly visible and front-facing
- Check image quality and lighting
- Try different photos

**"Process timed out"**
- Increase timeout in `app.py` (default: 5 minutes)
- Use GPU hardware on Hugging Face for faster processing

**"Out of memory"**
- Reduce image size before uploading
- Use GPU space on Hugging Face
- Close other applications

**Dependencies installation fails**
- Update pip: `pip install --upgrade pip`
- Install system dependencies: `apt-get install cmake build-essential`

## 📝 Citation

If you use this application in your research, please cite the original Barbershop paper:

```bibtex
@article{zhu2021barbershop,
  title={Barbershop: GAN-based Image Compositing using Segmentation Masks},
  author={Zhu, Peihao and Abdal, Rameen and Femiani, John and Wonka, Peter},
  journal={arXiv preprint arXiv:2106.01505},
  year={2021}
}
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

The Barbershop model is subject to its own license. Please refer to the [original repository](https://github.com/ZPdesu/Barbershop) for more information.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [Barbershop](https://github.com/ZPdesu/Barbershop) by Zhu et al. for the hairstyle transfer model
- [Gradio](https://gradio.app/) for the web interface framework
- [Hugging Face](https://huggingface.co/) for hosting and deployment platform
- Original researchers at Harbour Space University for testing and validation

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact the repository maintainers.

---

**⚠️ Disclaimer**: This is a research demo. Results may vary based on input quality. The model works best with clear, front-facing photos. Processing times may vary depending on hardware.
