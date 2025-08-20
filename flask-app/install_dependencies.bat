@echo off
echo Installing ClinInsight Dependencies...
echo.

echo Step 1: Installing basic packages...
pip install flask==2.3.3 werkzeug==2.3.7 python-dotenv==1.0.0 numpy

echo.
echo Step 2: Installing PyTorch (CPU version for better compatibility)...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

echo.
echo Step 3: Installing OpenAI Whisper...
pip install openai-whisper

echo.
echo Step 4: Verifying installation...
python -c "import whisper; print('Whisper installed successfully!')"

echo.
echo Installation completed! You can now run: python app.py
pause
