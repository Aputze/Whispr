@echo off
echo Installing ClinInsight Dependencies using Conda...
echo.

echo Checking if conda is available...
conda --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Conda not found. Please install Anaconda or Miniconda first.
    echo Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo Conda found! Creating environment...
conda create -n clininsight python=3.9 -y

echo Activating environment...
call conda activate clininsight

echo Installing packages with conda...
conda install -c conda-forge flask=2.3.3 werkzeug=2.3.7 python-dotenv=1.0.0 numpy -y
conda install -c pytorch pytorch torchaudio cpuonly -y
conda install -c conda-forge openai-whisper -y

echo.
echo Installation completed! To use the app:
echo 1. Activate the environment: conda activate clininsight
echo 2. Run the app: python app.py
echo.
pause
