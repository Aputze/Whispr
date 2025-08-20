# Whispr - Audio Transcription App

Whispr is an audio transcription application that uses OpenAI's Whisper model through the faster-whisper library. It provides two different interfaces for different use cases.

## Project Structure

```
Whispr/
├── flask-app/          # Flask web application
│   ├── app.py         # Main Flask app with REST API
│   ├── templates/     # HTML templates
│   ├── screenshots/   # Visual examples of Flask interface
│   ├── uploads/       # File upload directory
│   ├── requirements.txt # Flask dependencies
│   ├── demo.py        # Command-line demo script
│   ├── start.bat      # Windows startup script
│   ├── start.ps1      # PowerShell startup script
│   ├── install_*.bat  # Windows installation scripts
│   ├── install_*.ps1  # PowerShell installation scripts
│   └── README.md      # Flask app documentation
├── gradio-app/         # Gradio interface application
│   ├── app.py         # Main Gradio app
│   ├── hf_app.py      # Hugging Face Spaces version
│   ├── requirements.txt # Gradio dependencies
│   ├── README_HF.md   # Hugging Face Spaces config
│   └── README.md      # Gradio app documentation
└── README.md           # This file
```

## Two Versions Available

### 1. Flask App (`flask-app/`)
- **Traditional web application** with custom HTML/CSS interface
- **REST API endpoints** for programmatic access
- **File upload handling** with cleanup
- **Runs on port 8000**
- **Beautiful drag & drop interface** with model selection slider
- **Screenshots included** showing the interface
- **Complete installation scripts** for Windows users
- **Demo script** for command-line testing
- Perfect for production deployments and custom integrations

### 2. Gradio App (`gradio-app/`)
- **Modern, interactive interface** built with Gradio
- **Audio file upload and microphone recording**
- **Model size selection** with real-time feedback
- **Optimized for Hugging Face Spaces** deployment
- Perfect for demos, research, and easy deployment

## Quick Start

### Flask Version
```bash
cd flask-app
pip install -r requirements.txt
python app.py
# Open http://localhost:8000
```

**Windows Users**: Use the provided installation scripts in the `flask-app/` folder for easy setup.

### Gradio Version
```bash
cd gradio-app
pip install -r requirements.txt
python app.py
# Gradio will show the local URL
```

## Features

- **Multi-language support** (optimized for Hebrew)
- **Multiple model sizes** (tiny to large)
- **Audio format support**: m4a, mp3, wav, aac, m4b, mp4
- **Confidence scoring** and metadata
- **Automatic cleanup** of temporary files
- **Professional-grade transcription** with advanced parameters

## Model Sizes

- **Tiny (39MB)**: Fastest, basic accuracy
- **Base (74MB)**: Good balance of speed and accuracy
- **Small (244MB)**: Better accuracy, recommended
- **Medium (769MB)**: High accuracy, slower
- **Large (1550MB)**: Best accuracy, slowest

## Screenshots

Check the `flask-app/screenshots/` folder for visual examples of the Flask interface:
- **Main Interface** - Beautiful drag & drop interface with horizontal slider
- **Transcription Results** - Clean output with modern copy button
- **Model Selection Slider** - Interactive slider with snapping functionality

## What's in Each Folder

### `flask-app/` - Complete Flask Application
- Main Flask application with REST API
- HTML templates and screenshots
- Windows installation and startup scripts
- Command-line demo script
- All dependencies and documentation

### `gradio-app/` - Gradio Interface
- Modern Gradio-based interface
- Hugging Face Spaces optimized version
- Lightweight and easy to deploy
