"""
Enhanced Virtual Hairstyle Try-On Application
Enterprise-level Gradio interface with advanced features.
"""

import gradio as gr
from pathlib import Path
import logging
from typing import Optional

# Import our new modular components
from src.config import get_settings
from src.utils import setup_logger
from src.services import HairstyleTransferService, HairstyleGalleryService

# Setup logging
setup_logger(
    name="virtual_hairstyle",
    level=logging.INFO,
    log_file=Path("logs/app.log")
)
logger = logging.getLogger("virtual_hairstyle")

# Initialize settings and services
settings = get_settings()
transfer_service = HairstyleTransferService()
gallery_service = HairstyleGalleryService()


def transfer_hairstyle_wrapper(
    face_img,
    hair_img,
    style: str = "realistic",
    smoothness: int = 5,
    enhance: bool = False,
    progress=gr.Progress()
):
    """
    Wrapper function for Gradio interface.
    
    Args:
        face_img: PIL Image of the face
        hair_img: PIL Image with desired hairstyle
        style: Transfer style
        smoothness: Smoothness parameter
        enhance: Whether to enhance images
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (result_image, log_message, stats_text)
    """
    try:
        logger.info("Starting hairstyle transfer process")
        
        # Call the service with progress callback
        result_img, log_msg = transfer_service.transfer_hairstyle(
            face_image=face_img,
            hairstyle_image=hair_img,
            style=style,
            smoothness=smoothness,
            enhance=enhance,
            progress_callback=progress
        )
        
        # Generate statistics
        if result_img:
            stats = f"**Transfer Complete!**\n\n"
            stats += f"- Style: {style}\n"
            stats += f"- Smoothness: {smoothness}\n"
            stats += f"- Enhancement: {'Enabled' if enhance else 'Disabled'}\n"
            stats += f"- Image Size: {result_img.size[0]}x{result_img.size[1]}px"
        else:
            stats = "Transfer failed. See logs for details."
        
        return result_img, log_msg, stats
        
    except Exception as e:
        logger.error(f"Error in transfer wrapper: {str(e)}")
        return None, f"❌ Error: {str(e)}", "Transfer failed"


def get_model_info_text() -> str:
    """Get formatted model information."""
    info = transfer_service.get_model_info()
    
    text = f"""
## Model Information

- **Name**: {info['name']}
- **Version**: {info['version']}
- **Architecture**: {info['architecture']}
- **Paper**: [{info['paper']}]({info['paper']})
- **Repository**: [{info['repository']}]({info['repository']})
- **Authors**: {info['authors']}
- **Year**: {info['year']}
- **Status**: {'✅ Initialized' if info['is_initialized'] else '⏳ Not Initialized'}

### Supported Options

- **Styles**: {', '.join(info['supported_styles'])}
- **Smoothness Range**: {info['smoothness_range'][0]} - {info['smoothness_range'][1]}
"""
    return text


def get_gallery_stats_text() -> str:
    """Get formatted gallery statistics."""
    stats = gallery_service.get_gallery_stats()
    
    text = f"""
## Gallery Statistics

- **Total Categories**: {stats['total_categories']}
- **Total Hairstyles**: {stats['total_hairstyles']}
- **Example Pairs**: {stats['total_examples']}

### Per Category
"""
    
    for key, value in stats.items():
        if key.startswith('category_'):
            category = key.replace('category_', '').title()
            text += f"- **{category}**: {value} hairstyles\n"
    
    return text


# Create enhanced Gradio interface
with gr.Blocks(
    title=settings.APP_NAME,
    theme=gr.themes.Soft(
        primary_hue=settings.THEME_PRIMARY_HUE,
        secondary_hue=settings.THEME_SECONDARY_HUE,
    ),
    css=f"""
    .gradio-container {{
        max-width: {settings.MAX_CONTAINER_WIDTH} !important;
    }}
    .header {{
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }}
    .section-header {{
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }}
    .stats-box {{
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
    }}
    .footer {{
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        color: #666;
        border-top: 2px solid #eee;
    }}
    """
) as demo:
    
    # Header
    gr.Markdown(
        f"""
        <div class="header">
        <h1>🎨 {settings.APP_NAME}</h1>
        <p style="font-size: 1.2em;">Enterprise-Level AI-Powered Hairstyle Transfer</p>
        <p>Version {settings.APP_VERSION} | Powered by {settings.MODEL_NAME}</p>
        </div>
        """,
        elem_classes="header"
    )
    
    with gr.Tabs():
        # Main Transfer Tab
        with gr.TabItem("🪄 Hairstyle Transfer", id=0):
            gr.Markdown(
                """
                <div class="section-header">
                <h3>Transform Your Look with AI</h3>
                <p>Upload your photo and a reference hairstyle image to see yourself with a new look!</p>
                </div>
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 👤 Your Face Photo")
                    face_input = gr.Image(
                        type="pil",
                        label="Upload Your Photo",
                        sources=["upload", "webcam"] if settings.ENABLE_WEBCAM else ["upload"],
                        height=350
                    )
                    gr.Markdown(
                        """
                        **Tips:**
                        - Use a clear, front-facing photo
                        - Ensure good lighting
                        - Face should be clearly visible
                        """
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 💇 Reference Hairstyle")
                    hair_input = gr.Image(
                        type="pil",
                        label="Upload Hairstyle Reference",
                        sources=["upload"],
                        height=350
                    )
                    gr.Markdown(
                        """
                        **Tips:**
                        - Choose a similar photo style
                        - Front-facing works best
                        - Clear hairstyle visibility
                        """
                    )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Transfer Settings")
                    
                    style_choice = gr.Radio(
                        choices=transfer_service.get_supported_styles(),
                        value=settings.DEFAULT_STYLE,
                        label="Transfer Style",
                        info="Realistic: Natural blend | Fidelity: Preserves more details"
                    )
                    
                    smoothness = gr.Slider(
                        minimum=1,
                        maximum=5,
                        value=settings.DEFAULT_SMOOTHNESS,
                        step=1,
                        label="Smoothness Level",
                        info="Higher values = smoother transitions (1-5)"
                    )
                    
                    enhance_images = gr.Checkbox(
                        label="Enhance Images",
                        value=False,
                        info="Apply automatic image enhancement before processing"
                    )
                    
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Transfer Statistics")
                    stats_box = gr.Markdown(
                        "Transfer statistics will appear here after processing...",
                        elem_classes="stats-box"
                    )
            
            transfer_btn = gr.Button(
                "🚀 Transfer Hairstyle",
                variant="primary",
                size="lg",
                scale=2
            )
            
            gr.Markdown("### ✨ Result")
            
            with gr.Row():
                with gr.Column(scale=2):
                    output_image = gr.Image(
                        type="pil",
                        label="Transformed Result",
                        height=500
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Process Log")
                    info_box = gr.Textbox(
                        label="Processing Information",
                        lines=12,
                        max_lines=20,
                        placeholder="Processing information will appear here...",
                        show_copy_button=True
                    )
            
            # Connect the transfer button
            transfer_btn.click(
                fn=transfer_hairstyle_wrapper,
                inputs=[face_input, hair_input, style_choice, smoothness, enhance_images],
                outputs=[output_image, info_box, stats_box]
            )
            
            # Add examples if available
            example_dir = Path("./examples")
            if example_dir.exists():
                face_example = example_dir / "example_face.png"
                hair_example = example_dir / "example_hair.png"
                
                if face_example.exists() and hair_example.exists():
                    gr.Markdown("### 🎯 Quick Start Examples")
                    gr.Examples(
                        examples=[[str(face_example), str(hair_example)]],
                        inputs=[face_input, hair_input],
                        label="Click the example to load it"
                    )
        
        # Gallery Tab
        with gr.TabItem("🎨 Hairstyle Gallery", id=1):
            gr.Markdown(
                """
                <div class="section-header">
                <h3>Browse Our Hairstyle Collection</h3>
                <p>Explore curated hairstyle samples organized by categories</p>
                </div>
                """
            )
            
            gallery_stats = get_gallery_stats_text()
            gr.Markdown(gallery_stats)
            
            categories = gallery_service.get_categories()
            if categories:
                gr.Markdown("### 📁 Browse by Category")
                
                category_selector = gr.Dropdown(
                    choices=categories,
                    label="Select Category",
                    value=categories[0] if categories else None
                )
                
                gallery_display = gr.Markdown("Select a category to view hairstyles")
                
                # Note: In a full implementation, we would add image galleries here
                # For now, we show the category structure
                gr.Markdown(
                    """
                    **Available Categories:**
                    - Short hairstyles
                    - Medium-length styles
                    - Long hairstyles
                    - Curly styles
                    - Straight styles
                    - Wavy styles
                    - Formal styles
                    - Casual styles
                    - Colored styles
                    - Natural styles
                    
                    *Add your own hairstyle samples to the `hairstyles/` directory!*
                    """
                )
            else:
                gr.Markdown("No hairstyle categories found. Add samples to the `hairstyles/` directory.")

        # Remote Import Tab
        with gr.TabItem("🌐 Import Online", id=2):
            gr.Markdown(
                """
                ### 🌐 Import Hairstyles from the Internet
                Add new hairstyle reference images directly by URL or via a JSON manifest.
                
                - Direct image download (PNG/JPG)
                - Bulk import with JSON manifest
                - Automatic metadata capture (source, size, dimensions)
                - Stored under `hairstyles/<category>/`
                
                **Manifest Example:**
                ```json
                {
                  "items": [
                    {"url": "https://example.com/hair1.jpg", "category": "long", "name": "wavy_long_1"},
                    {"url": "https://example.com/hair2.png", "category": "short"}
                  ]
                }
                ```
                """
            )

            with gr.Row():
                with gr.Column():
                    url_input = gr.Textbox(label="Image URL", placeholder="https://.../image.jpg")
                    url_category = gr.Textbox(label="Category", value="misc")
                    url_name = gr.Textbox(label="Optional Name", placeholder="custom-name (no extension)")
                    download_button = gr.Button("Download Image", variant="primary")
                    url_result = gr.Markdown()
                with gr.Column():
                    manifest_url = gr.Textbox(label="Manifest URL", placeholder="https://.../manifest.json")
                    manifest_default_cat = gr.Textbox(label="Default Category", value="misc")
                    manifest_button = gr.Button("Import Manifest", variant="secondary")
                    manifest_result = gr.Markdown()

            def handle_download(u, c, n):
                if not u:
                    return "⚠️ Please provide an image URL." , get_gallery_stats_text()
                ok, msg, path = gallery_service.download_image_from_url(u, category=c or "misc", name=n or None)
                stats = get_gallery_stats_text()
                if ok:
                    return f"✅ {msg}\n\nSaved: `{path}`", stats
                return f"❌ {msg}", stats

            def handle_manifest(mu, dc):
                if not mu:
                    return "⚠️ Provide a manifest URL.", get_gallery_stats_text()
                success, total, messages = gallery_service.import_manifest(mu, default_category=dc or "misc")
                report = f"Imported {success}/{total} items.\n\n" + "\n".join(f"- {m}" for m in messages[:25])
                if len(messages) > 25:
                    report += f"\n... and {len(messages)-25} more"
                stats = get_gallery_stats_text()
                return report, stats

            download_button.click(
                fn=handle_download,
                inputs=[url_input, url_category, url_name],
                outputs=[url_result, stats_box]
            )

            manifest_button.click(
                fn=handle_manifest,
                inputs=[manifest_url, manifest_default_cat],
                outputs=[manifest_result, stats_box]
            )
        
        # Model Info Tab
        with gr.TabItem("🤖 Model Information", id=3):
            gr.Markdown(
                """
                <div class="section-header">
                <h3>About the AI Model</h3>
                </div>
                """
            )
            
            model_info = get_model_info_text()
            gr.Markdown(model_info)
            
            gr.Markdown(
                """
                ## How It Works
                
                The Barbershop model uses **StyleGAN2** technology for realistic hairstyle transfer:
                
                1. **Face Alignment**: Detects and aligns facial features in both images using dlib
                2. **Embedding**: Encodes images into StyleGAN2 latent space (1100 iterations)
                3. **Transfer**: Intelligently blends hairstyle from reference to target face
                4. **Refinement**: Applies smoothing and blending for natural-looking results
                
                ## Technical Pipeline
                
                ```
                Input Images → Validation → Preprocessing → Face Alignment
                    ↓
                StyleGAN2 Embedding → Hairstyle Transfer → Post-processing
                    ↓
                Result Image
                ```
                
                ## Performance
                
                - **Processing Time**: 3-5 minutes per transfer
                - **Image Requirements**: Minimum 256x256 pixels
                - **Supported Formats**: JPG, PNG
                - **Best Results**: Clear, front-facing photos with good lighting
                """
            )
        
        # Documentation Tab
        with gr.TabItem("📖 Documentation", id=3):
            gr.Markdown(
                """
                <div class="section-header">
                <h3>User Guide & Best Practices</h3>
                </div>
                
                ## Getting Started
                
                ### Step-by-Step Guide
                
                1. **Prepare Your Images**
                   - Take or select a clear photo of your face
                   - Find a reference photo with the hairstyle you want
                   - Ensure both images show front-facing views
                
                2. **Upload Images**
                   - Click the upload area or use webcam for your face photo
                   - Upload the reference hairstyle image
                
                3. **Adjust Settings**
                   - Choose transfer style (realistic vs. fidelity)
                   - Set smoothness level (1-5)
                   - Optionally enable image enhancement
                
                4. **Process & Review**
                   - Click "Transfer Hairstyle" button
                   - Wait 3-5 minutes for processing
                   - Review the result and logs
                
                ## Tips for Best Results
                
                ### ✅ Do's
                
                - ✅ Use high-quality, well-lit photos
                - ✅ Ensure faces are clearly visible and front-facing
                - ✅ Choose reference photos with similar lighting and quality
                - ✅ Use images with similar face angles
                - ✅ Try different smoothness values if result isn't perfect
                - ✅ Enable image enhancement for low-quality photos
                
                ### ❌ Don'ts
                
                - ❌ Avoid blurry or low-resolution images
                - ❌ Don't use extreme angles or partial faces
                - ❌ Avoid heavily edited or filtered photos
                - ❌ Don't use images with multiple faces
                - ❌ Avoid images with obscured faces (sunglasses, hands)
                
                ## Troubleshooting
                
                ### Common Issues
                
                **"Face alignment failed"**
                - Ensure faces are clearly visible
                - Check that images are front-facing
                - Try different photos with better lighting
                
                **"Processing timeout"**
                - This is normal for complex transfers
                - Try again with smaller images
                - Reduce smoothness level
                
                **"Poor result quality"**
                - Increase smoothness level
                - Enable image enhancement
                - Try different style (realistic vs. fidelity)
                - Use higher quality input images
                
                ## Advanced Features
                
                ### Image Enhancement
                
                Enable this option to automatically improve input image quality:
                - Brightness adjustment
                - Contrast enhancement
                - Sharpness improvement
                - Color optimization
                
                ### Style Modes
                
                - **Realistic**: Focuses on natural-looking blends, may sacrifice some hairstyle details
                - **Fidelity**: Preserves more hairstyle details, may look less natural
                
                ### Smoothness Levels
                
                - **1-2**: Minimal smoothing, preserves maximum detail
                - **3**: Balanced approach (recommended)
                - **4-5**: Maximum smoothing, best for challenging cases
                
                ## API Access
                
                This application can be accessed programmatically:
                
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
                
                ## Privacy & Data
                
                - All processing happens in-memory
                - Images are not permanently stored
                - No data is collected or shared
                - Temporary files are cleaned up after processing
                
                ## System Requirements
                
                - **Recommended**: GPU-enabled instance for faster processing
                - **Minimum RAM**: 8GB
                - **Disk Space**: 5GB for model weights
                - **Network**: Stable internet for model download
                """
            )
        
        # About Tab
        with gr.TabItem("ℹ️ About", id=4):
            gr.Markdown(
                f"""
                <div class="section-header">
                <h3>About This Project</h3>
                </div>
                
                ## {settings.APP_NAME}
                
                **Version**: {settings.APP_VERSION}
                
                An enterprise-level AI-powered hairstyle transfer application built with modern
                software engineering practices and modular architecture.
                
                ## Features
                
                - 🎨 **Advanced AI Transfer**: State-of-the-art StyleGAN2-based hairstyle transfer
                - 🏗️ **Enterprise Architecture**: Modular, maintainable, and scalable codebase
                - ✅ **Comprehensive Validation**: Input validation and quality checks
                - 📊 **Detailed Logging**: Full process tracking and debugging
                - 🎯 **User-Friendly UI**: Intuitive interface with helpful guidance
                - 🔧 **Configurable**: Extensive configuration options
                - 📱 **Webcam Support**: Take photos directly in the app
                - 🖼️ **Gallery System**: Organized hairstyle sample library
                - 📈 **Progress Tracking**: Real-time processing updates
                - 🎨 **Image Enhancement**: Automatic quality improvement
                
                ## Technology Stack
                
                - **Framework**: Gradio 4.16.0
                - **AI Model**: Barbershop (StyleGAN2-based)
                - **Language**: Python 3.10+
                - **Architecture**: Modular service-based design
                - **Logging**: Comprehensive logging system
                - **Validation**: Multi-layer input validation
                
                ## Project Structure
                
                ```
                virtual-hairstyle-tryon/
                ├── src/
                │   ├── config/          # Configuration management
                │   ├── models/          # AI model implementations
                │   ├── services/        # Business logic layer
                │   └── utils/           # Utility functions
                ├── hairstyles/          # Hairstyle gallery
                ├── examples/            # Example images
                ├── data/               # Sample datasets
                ├── tests/              # Test suite
                ├── docs/               # Documentation
                └── app.py              # Main application
                ```
                
                ## Credits
                
                ### Original Research
                
                This application is based on the Barbershop model:
                
                **Paper**: "Barbershop: GAN-based Image Compositing using Segmentation Masks"
                **Authors**: Peihao Zhu, Rameen Abdal, John Femiani, Peter Wonka
                **Year**: 2021
                **arXiv**: [2106.01505](https://arxiv.org/abs/2106.01505)
                
                ### Implementation
                
                - [Barbershop Repository](https://github.com/ZPdesu/Barbershop) by ZPdesu
                - [Gradio](https://gradio.app/) for the web interface
                - [Hugging Face](https://huggingface.co/) for hosting platform
                
                ## License
                
                This project is licensed under the MIT License.
                The Barbershop model is subject to its original license.
                
                ## Contributing
                
                Contributions are welcome! Please:
                
                1. Fork the repository
                2. Create a feature branch
                3. Make your changes
                4. Add tests if applicable
                5. Submit a pull request
                
                ## Support
                
                For issues, questions, or suggestions:
                
                - 📧 Open an issue on GitHub
                - 💬 Check the documentation
                - 🔍 Review troubleshooting guide
                
                ## Disclaimer
                
                ⚠️ This is a research demonstration. Results may vary based on input quality.
                The model works best with clear, front-facing photos. Processing times may
                vary depending on hardware and image complexity.
                """
            )
    
    # Footer
    gr.Markdown(
        f"""
        <div class="footer">
        <p><strong>Powered by {settings.MODEL_NAME} | Built with Gradio | Version {settings.APP_VERSION}</strong></p>
        <p>© 2024 Virtual Hairstyle Try-On | Enterprise Edition</p>
        <p>⚠️ Research Demo - Results may vary based on input quality</p>
        </div>
        """,
        elem_classes="footer"
    )

# Launch configuration
if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Try to initialize service on startup
    try:
        logger.info("Initializing hairstyle transfer service...")
        transfer_service.initialize()
        logger.info("Service initialization complete")
    except Exception as e:
        logger.warning(f"Service will initialize on first use: {e}")
    
    # Launch the application
    demo.launch(
        share=False,
        server_name=settings.SERVER_HOST,
        server_port=settings.SERVER_PORT,
        show_error=True,
        show_api=True
    )
