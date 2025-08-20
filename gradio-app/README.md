# Gradio App - Whispr Audio Transcription

This folder contains the Gradio interface version of Whispr, optimized for Hugging Face Spaces deployment.

## What's Inside
- `app.py` - Main Gradio application (moved from root)
- `hf_app.py` - Hugging Face Spaces version (from nested folder)
- `requirements.txt` - Python dependencies for Gradio version
- `README_HF.md` - Hugging Face Spaces configuration file

## Features
- Modern, interactive Gradio interface
- Audio file upload and microphone recording
- Model size selection
- Real-time transcription with progress bars
- Optimized for Hugging Face Spaces

## How to Run
```bash
cd gradio-app
pip install -r requirements.txt
python app.py
```

## For Hugging Face Spaces
1. Use `hf_app.py` as your main app file (or rename it to `app.py`)
2. Rename `README_HF.md` to `README.md` for the Spaces configuration
3. Upload the files to your Hugging Face Space
4. The app will automatically deploy with the Gradio interface

## Dependencies
- Gradio for the interface
- faster-whisper for audio transcription
- torch and torchaudio for PyTorch backend
