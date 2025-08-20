@echo off
echo Starting ClinInsight Audio Transcription App...
echo.
echo This will install dependencies and start the web server.
echo.
pause

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting the application...
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
