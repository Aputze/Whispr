Write-Host "Installing ClinInsight Dependencies..." -ForegroundColor Green
Write-Host ""

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python not found. Please install Python 3.8+ and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Installing basic packages..." -ForegroundColor Yellow
try {
    pip install flask==2.3.3 werkzeug==2.3.7 python-dotenv==1.0.0 numpy
    Write-Host "Basic packages installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Warning: Some basic packages failed to install. Continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Installing PyTorch (CPU version for better compatibility)..." -ForegroundColor Yellow
try {
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
    Write-Host "PyTorch installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Warning: PyTorch installation failed. Trying alternative method..." -ForegroundColor Yellow
    try {
        pip install torch torchaudio
        Write-Host "PyTorch installed with alternative method!" -ForegroundColor Green
    } catch {
        Write-Host "Error: PyTorch installation failed. Please check your internet connection." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Step 3: Installing OpenAI Whisper..." -ForegroundColor Yellow
try {
    pip install openai-whisper
    Write-Host "Whisper installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error: Whisper installation failed. Trying alternative method..." -ForegroundColor Red
    try {
        pip install --upgrade pip setuptools wheel
        pip install openai-whisper --no-cache-dir
        Write-Host "Whisper installed with alternative method!" -ForegroundColor Green
    } catch {
        Write-Host "Error: Whisper installation still failed. Please check the error messages above." -ForegroundColor Red
        Read-Host "Press Enter to continue anyway"
    }
}

Write-Host ""
Write-Host "Step 4: Verifying installation..." -ForegroundColor Yellow
try {
    python -c "import whisper; print('Whisper installed successfully!')"
    Write-Host "Verification completed!" -ForegroundColor Green
} catch {
    Write-Host "Warning: Whisper verification failed. The app may not work properly." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Installation completed!" -ForegroundColor Green
Write-Host "You can now run: python app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "If you encountered errors, try:" -ForegroundColor Yellow
Write-Host "1. Upgrading pip: python -m pip install --upgrade pip" -ForegroundColor White
Write-Host "2. Installing Visual C++ build tools (for Windows)" -ForegroundColor White
Write-Host "3. Using conda instead of pip if available" -ForegroundColor White

Read-Host "Press Enter to exit"
