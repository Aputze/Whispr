import os
import tempfile
import time
import glob
from flask import Flask, render_template, request, jsonify, flash
from faster_whisper import WhisperModel
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'whispr-secure-key-2025-audio-transcription'

# Transcription Configuration
FORCE_LANGUAGE = "he"  # Set to "he" for Hebrew, "en" for English, or None for auto-detection
WHISPER_MODEL_SIZE = "small"  # Options: "tiny", "base", "small", "medium", "large" - small is much more accurate than base

def cleanup_old_temp_files():
    """Clean up old temporary audio files from the temp directory"""
    try:
        temp_dir = tempfile.gettempdir()
        # Find all old whisper audio files (older than 1 hour) - all supported formats
        patterns = [
            "whisper_audio_*.m4a",
            "whisper_audio_*.mp3", 
            "whisper_audio_*.wav",
            "whisper_audio_*.aac",
            "whisper_audio_*.m4b",
            "whisper_audio_*.mp4"
        ]
        
        old_files = []
        for pattern in patterns:
            full_pattern = os.path.join(temp_dir, pattern)
            old_files.extend(glob.glob(full_pattern))
        
        current_time = time.time()
        files_deleted = 0
        
        for file_path in old_files:
            try:
                # Check if file is older than 1 hour (3600 seconds)
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > 3600:  # 1 hour
                    os.remove(file_path)
                    files_deleted += 1
                    print(f"Deleted old temp file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")
        
        if files_deleted > 0:
            print(f"Cleaned up {files_deleted} old temporary files")
        
    except Exception as e:
        print(f"Error during temp file cleanup: {e}")

def cleanup_temp_file(filepath):
    """Safely remove a temporary file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Successfully cleaned up: {os.path.basename(filepath)}")
            return True
    except Exception as e:
        print(f"Failed to clean up {filepath}: {e}")
    return False

# Configure upload settings
UPLOAD_FOLDER = os.path.abspath('uploads')  # Use absolute path
ALLOWED_EXTENSIONS = {'m4a', 'mp3', 'wav', 'aac', 'm4b', 'mp4'}

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Clean up old temp files on each page load
    cleanup_old_temp_files()
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Check if file was uploaded
        if 'audio_file' not in request.files:
            print("No audio_file in request.files")
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['audio_file']
        
        # Check if file was selected
        if file.filename == '':
            print("No filename provided")
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"Processing file: {file.filename}")
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        
        # Use tempfile for Windows compatibility with Whisper
        import tempfile
        temp_dir = tempfile.gettempdir()
        temp_filename = f"whisper_audio_{os.getpid()}_{int(time.time())}.{filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(temp_dir, temp_filename)
        
        # Convert to raw string for Windows compatibility
        filepath = os.path.normpath(filepath)
        
        print(f"Saving file to: {filepath}")
        print(f"Temp directory: {temp_dir}")
        print(f"Directory exists: {os.path.exists(temp_dir)}")
        print(f"Directory writable: {os.access(temp_dir, os.W_OK)}")
        
        # Ensure the file is saved
        file.save(filepath)
        
        # Verify file was saved
        if not os.path.exists(filepath):
            print(f"File was not saved successfully to {filepath}")
            return jsonify({'error': 'Failed to save uploaded file'}), 500
        
        print(f"File saved successfully. Size: {os.path.getsize(filepath)} bytes")
        
        try:
            # Get model size from request (or use default)
            requested_model = request.form.get('model_size', WHISPER_MODEL_SIZE)
            print(f"Requested model: {requested_model}")
            
            # Load Whisper model (this will download the model on first use)
            print(f"Loading faster-whisper model: {requested_model}")
            model = WhisperModel(requested_model, device="cpu", compute_type="int8")
            
            # Verify file still exists before transcription
            if not os.path.exists(filepath):
                print(f"File disappeared before transcription: {filepath}")
                return jsonify({'error': 'File not found during transcription'}), 500
            
            print(f"File exists before transcription: {filepath}")
            print(f"File size before transcription: {os.path.getsize(filepath)} bytes")
            
            # Try to open the file to ensure it's accessible
            try:
                with open(filepath, 'rb') as test_file:
                    print("File is readable and accessible")
            except Exception as e:
                print(f"File access test failed: {e}")
                return jsonify({'error': f'File access failed: {str(e)}'}), 500
            
            # Transcribe the audio using faster-whisper with improved parameters
            print("Transcribing audio...")
            # Better parameters for accuracy:
            # - beam_size=5: Better search algorithm
            # - best_of=5: Consider top 5 candidates
            # - temperature=0.0: Deterministic output
            # - condition_on_previous_text=True: Better context
            # Configure language parameter with professional-grade settings
            transcribe_params = {
                "beam_size": 10,           # Increased from 5 to 10 for better search
                "best_of": 10,             # Increased from 5 to 10 for better candidates
                "temperature": 0.0,        # Keep deterministic
                "condition_on_previous_text": True,
                "word_timestamps": True,   # Word-level timing for precision
                "compression_ratio_threshold": 2.4,  # Better audio quality detection
                "log_prob_threshold": -1.0,          # Filter out low-confidence words
                "no_speech_threshold": 0.6,          # Better silence detection
                "initial_prompt": "This is Hebrew speech. Please transcribe accurately with proper Hebrew grammar and pronunciation."  # Context hint
            }
            
            # Add language if specified
            if FORCE_LANGUAGE:
                transcribe_params["language"] = FORCE_LANGUAGE
                print(f"Forcing language: {FORCE_LANGUAGE}")
            
            segments, info = model.transcribe(filepath, **transcribe_params)
            
            # Extract the full transcription text with professional formatting
            transcription_text = ""
            segments_list = list(segments)
            
            for segment in segments_list:
                # Clean up the text and add proper spacing
                clean_text = segment.text.strip()
                if clean_text:
                    # Better Hebrew text processing
                    clean_text = clean_text.replace("  ", " ")  # Remove double spaces
                    clean_text = clean_text.replace(" .", ".")  # Fix spacing around periods
                    clean_text = clean_text.replace(" ,", ",")  # Fix spacing around commas
                    clean_text = clean_text.replace(" ?", "?")  # Fix spacing around question marks
                    clean_text = clean_text.replace(" !", "!")  # Fix spacing around exclamation marks
                    
                    transcription_text += clean_text + " "
            
            # Final text cleanup and Hebrew-specific improvements
            transcription_text = transcription_text.strip()
            
            # Remove any remaining double spaces
            while "  " in transcription_text:
                transcription_text = transcription_text.replace("  ", " ")
            
            # Ensure proper sentence endings
            if transcription_text and not transcription_text.endswith(('.', '!', '?')):
                transcription_text += "."
            
            print("Transcription completed successfully!")
            print(f"Detected language: {info.language}")
            print(f"Language probability: {info.language_probability}")
            
            # Calculate duration and confidence metrics
            duration = segments_list[-1].end if segments_list else 0
            
            # Calculate overall confidence score
            total_confidence = 0
            valid_segments = 0
            for segment in segments_list:
                if hasattr(segment, 'avg_logprob') and segment.avg_logprob is not None:
                    total_confidence += segment.avg_logprob
                    valid_segments += 1
            
            avg_confidence = (total_confidence / valid_segments) if valid_segments > 0 else 0
            confidence_percentage = min(100, max(0, (avg_confidence + 2) * 25))  # Convert to 0-100 scale
            
            # Clean up the uploaded file
            cleanup_temp_file(filepath)
            
            return jsonify({
                'success': True,
                'transcription': transcription_text,
                'language': info.language,
                'duration': duration,
                'confidence': round(confidence_percentage, 1),
                'model_used': requested_model
            })
            
        except Exception as e:
            print(f"Error during transcription: {str(e)}")
            print(f"File path that caused error: {filepath}")
            print(f"File exists after error: {os.path.exists(filepath)}")
            # Clean up file on error
            cleanup_temp_file(filepath)
            raise e
            
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/cleanup')
def manual_cleanup():
    """Manual cleanup endpoint for removing old temp files"""
    try:
        cleanup_old_temp_files()
        return jsonify({'success': True, 'message': 'Cleanup completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Clean up old files on startup
    print("Starting Whispr - Audio Transcription App")
    cleanup_old_temp_files()
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
    print(f"Upload folder writable: {os.access(UPLOAD_FOLDER, os.W_OK)}")
    app.run(debug=True, host='0.0.0.0', port=8000)
