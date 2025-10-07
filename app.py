import gradio as gr
import torch
import os
import sys
import subprocess
import shutil
from PIL import Image
import numpy as np
from pathlib import Path

# Setup paths
BARBERSHOP_PATH = "./Barbershop"
INPUT_DIR = os.path.join(BARBERSHOP_PATH, "input")
UNPROCESSED_DIR = os.path.join(BARBERSHOP_PATH, "unprocessed")
OUTPUT_DIR = os.path.join(BARBERSHOP_PATH, "output")

def setup_barbershop():
    """Clone and setup Barbershop repository"""
    # Check if key files exist instead of just directory
    align_face_script = os.path.join(BARBERSHOP_PATH, "align_face.py")
    main_script = os.path.join(BARBERSHOP_PATH, "main.py")
    
    if not os.path.exists(align_face_script) or not os.path.exists(main_script):
        print("Setting up Barbershop repository...")
        
        # Remove existing directory if it's incomplete
        if os.path.exists(BARBERSHOP_PATH):
            shutil.rmtree(BARBERSHOP_PATH)
        
        print("Cloning Barbershop repository...")
        subprocess.run(["git", "clone", "https://github.com/ZPdesu/Barbershop.git"], check=True)
        
        # Install ninja
        subprocess.run([sys.executable, "-m", "pip", "install", "ninja"], check=True)
        
        # Remove default image if exists
        default_img = os.path.join(UNPROCESSED_DIR, "90.jpg")
        if os.path.exists(default_img):
            os.remove(default_img)
    
    print("✅ Barbershop setup complete")
    
    # Ensure directories exist
    os.makedirs(UNPROCESSED_DIR, exist_ok=True)
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_image(image, filename):
    """Save PIL image to unprocessed directory"""
    if image is not None:
        filepath = os.path.join(UNPROCESSED_DIR, filename)
        image.save(filepath)
        return filepath
    return None

def align_faces():
    """Run face alignment"""
    current_dir = os.getcwd()
    try:
        os.chdir(BARBERSHOP_PATH)
        result = subprocess.run(
            [sys.executable, "align_face.py", "-seed", "42"],
            capture_output=True,
            text=True
        )
        os.chdir(current_dir)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        os.chdir(current_dir)
        return False, str(e)

def get_aligned_images():
    """Get list of aligned images"""
    if os.path.exists(INPUT_DIR):
        return [f for f in os.listdir(INPUT_DIR) if f.endswith(('.png', '.jpg', '.jpeg'))]
    return []

def hairstyle_transfer(face_img, hair_img, style="realistic", smoothness=5, progress=gr.Progress()):
    """
    Perform hairstyle transfer
    
    Args:
        face_img: PIL Image of the face to receive hairstyle
        hair_img: PIL Image with the desired hairstyle
        style: Transfer style (realistic or fidelity)
        smoothness: Smoothness parameter (1-5)
    """
    try:
        progress(0, desc="Setting up...")
        
        # Setup Barbershop if needed
        setup_barbershop()
        
        # Clear previous images
        for f in os.listdir(UNPROCESSED_DIR):
            if f.endswith(('.png', '.jpg', '.jpeg')):
                os.remove(os.path.join(UNPROCESSED_DIR, f))
        
        progress(0.1, desc="Saving images...")
        
        # Save images
        face_path = save_image(face_img, "face.png")
        hair_path = save_image(hair_img, "hair.png")
        
        if not face_path or not hair_path:
            return None, "Error: Could not save images"
        
        progress(0.2, desc="Aligning faces...")
        
        # Align faces
        success, align_log = align_faces()
        if not success:
            return None, f"Face alignment failed:\n{align_log}"
        
        progress(0.4, desc="Finding aligned images...")
        
        # Get aligned image names
        aligned_imgs = get_aligned_images()
        if len(aligned_imgs) < 2:
            return None, f"Face alignment produced {len(aligned_imgs)} images. Need at least 2.\n{align_log}"
        
        # Sort to get consistent ordering
        aligned_imgs.sort()
        face_aligned = aligned_imgs[0]
        hair_aligned = aligned_imgs[1]
        
        progress(0.5, desc="Performing hairstyle transfer...")
        
        # Run hairstyle transfer
        current_dir = os.getcwd()
        try:
            os.chdir(BARBERSHOP_PATH)
            
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
                timeout=300  # 5 minutes timeout
            )
            
            os.chdir(current_dir)
            
            progress(0.9, desc="Loading result...")
            
            # Find output image
            output_path = os.path.join(OUTPUT_DIR, f"Blend_{style}")
            if os.path.exists(output_path):
                output_files = [f for f in os.listdir(output_path) if f.endswith('.png')]
                if output_files:
                    # Get the latest output
                    output_files.sort(key=lambda x: os.path.getmtime(os.path.join(output_path, x)), reverse=True)
                    result_img_path = os.path.join(output_path, output_files[0])
                    result_img = Image.open(result_img_path)
                    
                    progress(1.0, desc="Done!")
                    
                    log_msg = f"✅ Success!\n\nAligned images: {face_aligned}, {hair_aligned}\n\n"
                    log_msg += f"Style: {style}, Smoothness: {smoothness}\n\n"
                    log_msg += "Process output:\n" + result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
                    
                    return result_img, log_msg
            
            return None, f"Output image not found. Check logs:\n{result.stdout}\n{result.stderr}"
            
        except subprocess.TimeoutExpired:
            os.chdir(current_dir)
            return None, "Process timed out after 5 minutes"
        except Exception as e:
            os.chdir(current_dir)
            return None, f"Error during transfer: {str(e)}"
            
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# Create Gradio interface with advanced UI
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="cyan",
    ),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .header {
        text-align: center;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 20px;
        color: #666;
    }
    """
) as demo:
    
    gr.Markdown(
        """
        <div class="header">
        <h1>🎨 Virtual Hairstyle Try-On</h1>
        <p>Transfer hairstyles between photos using the Barbershop AI model</p>
        </div>
        """,
        elem_classes="header"
    )
    
    with gr.Tabs():
        with gr.TabItem("🪄 Hairstyle Transfer", id=0):
            gr.Markdown(
                """
                ### How to use:
                1. **Upload your face photo** - The person who will receive the new hairstyle
                2. **Upload hairstyle reference** - The photo with the desired hairstyle
                3. **Adjust settings** - Choose style and smoothness
                4. **Click "Transfer Hairstyle"** - Wait for the magic to happen!
                
                💡 **Tips for best results:**
                - Use clear, front-facing photos
                - Ensure faces are well-lit and visible
                - Photos should be similar in quality
                """
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 👤 Your Face")
                    face_input = gr.Image(
                        type="pil",
                        label="Upload Face Photo",
                        sources=["upload", "webcam"],
                        height=300
                    )
                    
                with gr.Column(scale=1):
                    gr.Markdown("### 💇 Desired Hairstyle")
                    hair_input = gr.Image(
                        type="pil",
                        label="Upload Hairstyle Reference",
                        sources=["upload"],
                        height=300
                    )
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### ⚙️ Settings")
                    style_choice = gr.Radio(
                        choices=["realistic", "fidelity"],
                        value="realistic",
                        label="Transfer Style",
                        info="Realistic: Natural blend | Fidelity: Preserves more details"
                    )
                    smoothness = gr.Slider(
                        minimum=1,
                        maximum=5,
                        value=5,
                        step=1,
                        label="Smoothness",
                        info="Higher values = smoother transitions"
                    )
                    
                with gr.Column(scale=1):
                    gr.Markdown("### ℹ️ Process Info")
                    info_box = gr.Textbox(
                        label="Logs",
                        lines=8,
                        max_lines=15,
                        placeholder="Processing information will appear here..."
                    )
            
            transfer_btn = gr.Button(
                "🚀 Transfer Hairstyle",
                variant="primary",
                size="lg"
            )
            
            gr.Markdown("### ✨ Result")
            output_image = gr.Image(
                type="pil",
                label="Result",
                height=400
            )
            
            transfer_btn.click(
                fn=hairstyle_transfer,
                inputs=[face_input, hair_input, style_choice, smoothness],
                outputs=[output_image, info_box]
            )
        
        with gr.TabItem("📖 About", id=1):
            gr.Markdown(
                """
                # About Virtual Hairstyle Try-On
                
                This application uses the **Barbershop** model for hairstyle transfer, introduced by 
                [Zhu et al.](https://arxiv.org/abs/2106.01505) in 2021.
                
                ## How it works
                
                The Barbershop model utilizes **StyleGAN2** for realistic hairstyle transfer:
                1. **Face Alignment**: Detects and aligns facial features in both images
                2. **Embedding**: Encodes images into latent space
                3. **Transfer**: Blends hairstyle from reference to target face
                4. **Refinement**: Applies smoothing for natural results
                
                ## Model Information
                
                - **Model**: Barbershop (StyleGAN2-based)
                - **Paper**: [Barbershop: GAN-based Image Compositing using Segmentation Masks](https://arxiv.org/abs/2106.01505)
                - **Repository**: [ZPdesu/Barbershop](https://github.com/ZPdesu/Barbershop)
                
                ## Credits
                
                This project is based on the original Barbershop implementation and has been adapted for 
                easy deployment on Hugging Face Spaces.
                
                ## Limitations
                
                - Works best with front-facing photos
                - Requires clear, well-lit images
                - Processing time: 3-5 minutes per transfer
                - May not work well with extreme hairstyles or unusual angles
                
                ## Tips for Best Results
                
                ✅ Use high-quality, well-lit photos  
                ✅ Ensure faces are clearly visible  
                ✅ Choose similar photo styles  
                ✅ Try different smoothness values  
                
                ❌ Avoid blurry or low-resolution images  
                ❌ Avoid extreme angles or partial faces  
                ❌ Avoid heavily edited photos  
                """
            )
        
        with gr.TabItem("🎯 Examples", id=2):
            gr.Markdown(
                """
                # Example Results
                
                Here are some example transformations achieved with this model:
                
                Upload your own images to see similar results!
                """
            )
            
            # Add example images if available
            example_dir = "./examples"
            if os.path.exists(example_dir):
                gr.Examples(
                    examples=[
                        [os.path.join(example_dir, "example_face.png"), os.path.join(example_dir, "example_hair.png")],
                    ],
                    inputs=[face_input, hair_input],
                )
    
    gr.Markdown(
        """
        <div class="footer">
        <p>Powered by Barbershop AI | Built with Gradio</p>
        <p>⚠️ This is a research demo. Results may vary based on input quality.</p>
        </div>
        """,
        elem_classes="footer"
    )

# Launch the app
if __name__ == "__main__":
    # Try to setup on startup
    try:
        setup_barbershop()
        print("✅ Barbershop setup complete")
    except Exception as e:
        print(f"⚠️ Barbershop setup will be done on first use: {e}")
    
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )
