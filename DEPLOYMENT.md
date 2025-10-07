# Hugging Face Deployment Guide

This guide will help you deploy the Virtual Hairstyle Try-On application to Hugging Face Spaces.

## Prerequisites

- A Hugging Face account (free at https://huggingface.co/join)
- Git installed on your local machine
- This repository cloned locally

## Method 1: Direct Upload (Easiest)

1. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Fill in the details:
     - Owner: Your username
     - Space name: `virtual-hairstyle-tryon`
     - License: MIT
     - Space SDK: Gradio
     - Gradio SDK version: 4.16.0
     - Private/Public: Choose based on preference
   - Click "Create Space"

2. **Upload files**
   - In your new Space, click on "Files and versions"
   - Upload the following files:
     - `app.py`
     - `requirements.txt`
     - `.gitignore`
     - `README_HF.md` (rename to `README.md` when uploading)
     - `examples/` folder (optional)

3. **Wait for build**
   - The Space will automatically build and deploy
   - This may take 5-10 minutes
   - Check the "Building" tab for progress

4. **Test your app**
   - Once built, the app will be available at:
     `https://huggingface.co/spaces/YOUR_USERNAME/virtual-hairstyle-tryon`

## Method 2: Git Push (Recommended for developers)

1. **Install Hugging Face CLI**
   ```bash
   pip install huggingface_hub
   ```

2. **Login to Hugging Face**
   ```bash
   huggingface-cli login
   ```
   Enter your Hugging Face token when prompted (get it from https://huggingface.co/settings/tokens)

3. **Create Space via CLI** (or create it via web interface first)
   ```bash
   huggingface-cli repo create virtual-hairstyle-tryon --type space --space_sdk gradio
   ```

4. **Prepare repository**
   ```bash
   cd virtual-hairstyle-tryon
   
   # If README_HF.md exists, use it for Hugging Face
   cp README_HF.md README.md
   
   # Add all necessary files
   git add app.py requirements.txt .gitignore README.md examples/
   git commit -m "Initial commit for Hugging Face deployment"
   ```

5. **Add Hugging Face remote and push**
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/virtual-hairstyle-tryon
   git push hf main
   ```

6. **Monitor deployment**
   - Go to your Space on Hugging Face
   - Check the "Building" tab for logs
   - Wait for deployment to complete

## Method 3: GitHub Integration (Continuous Deployment)

1. **Create a Space** on Hugging Face (as in Method 1)

2. **Link your GitHub repository**
   - In your Space settings, go to "Repository secrets"
   - Link your GitHub repository for automatic syncing

3. **Push to GitHub**
   - Every push to your GitHub repository will automatically deploy to HF Space

## Configuration

### Hardware Settings

After deployment, you can upgrade hardware in Space settings:
- **CPU Basic**: Free, slower processing (~5 min per image)
- **CPU Upgrade**: Faster CPU processing
- **GPU (T4, A10G)**: Much faster processing (~1-2 min per image)
  - Recommended for production use
  - Requires subscription or pay-as-you-go

### Environment Variables (Optional)

In Space settings, you can add:
```
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=7860
```

## Troubleshooting

### Build Fails

**Issue**: Dependencies installation fails
- Check `requirements.txt` for compatibility
- Ensure all packages support Python 3.10
- Check the build logs for specific errors

**Issue**: Out of memory during build
- This is usually fine; the app will work at runtime
- Consider using GPU hardware

### Runtime Issues

**Issue**: "Face alignment failed"
- This is user input issue, not deployment
- Add better error messages in app.py

**Issue**: Processing timeout
- Increase timeout in app.py
- Use GPU hardware for faster processing
- Default timeout is 5 minutes

### Slow Performance

**Solution**: Upgrade to GPU hardware
1. Go to Space settings
2. Select "Hardware" 
3. Choose a GPU option (requires payment)
4. Restart Space

## Testing Locally First

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Open browser to http://localhost:7860
```

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] Can upload images
- [ ] Face alignment works
- [ ] Hairstyle transfer completes
- [ ] Results display correctly
- [ ] Logs show useful information
- [ ] Examples work (if included)
- [ ] README displays correctly
- [ ] Mobile-friendly interface

## Updating Your Deployment

To update after initial deployment:

**Via Git:**
```bash
git add .
git commit -m "Update description"
git push hf main
```

**Via Web UI:**
- Upload new files directly in the Space interface
- Edit files directly in the browser

## Making Your Space Public

1. Go to Space settings
2. Change visibility to "Public"
3. Add tags for discoverability:
   - hairstyle-transfer
   - stylegan2
   - image-generation
   - gradio

## Advanced Features

### Custom Domain
- Available for paid accounts
- Set in Space settings

### Analytics
- View usage statistics in Space dashboard
- Track number of users and inference time

### API Access
- Every Gradio Space has an API
- Access at: `https://YOUR_USERNAME-virtual-hairstyle-tryon.hf.space/api`
- See API docs in Space interface

## Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/docs/)
- [Spaces Pricing](https://huggingface.co/pricing)
- [Community Forum](https://discuss.huggingface.co/)

## Support

If you encounter issues:
1. Check the build logs in your Space
2. Search Hugging Face forums
3. Open an issue on GitHub
4. Contact Hugging Face support (for platform issues)

---

Good luck with your deployment! 🚀
