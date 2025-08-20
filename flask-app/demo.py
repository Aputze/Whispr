#!/usr/bin/env python3
"""
Demo script for ClinInsight Audio Transcription
This script demonstrates how to use the transcription functionality programmatically.
"""

import os
import whisper
from pathlib import Path

def transcribe_audio_file(audio_file_path, model_size="base"):
    """
    Transcribe an audio file using OpenAI Whisper
    
    Args:
        audio_file_path (str): Path to the audio file
        model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
    
    Returns:
        dict: Transcription result with text, language, and segments
    """
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    
    print(f"Transcribing: {audio_file_path}")
    result = model.transcribe(audio_file_path)
    
    return result

def main():
    """Main demo function"""
    
    print("🎤 ClinInsight Audio Transcription Demo")
    print("=" * 50)
    
    # Example usage
    print("\nThis demo shows how to use the transcription functionality.")
    print("To test with your own audio file, modify the audio_file_path below.")
    
    # You can change this path to your audio file
    audio_file_path = "path/to/your/audio/file.m4a"  # Change this!
    
    if not os.path.exists(audio_file_path):
        print(f"\n⚠️  Audio file not found: {audio_file_path}")
        print("Please update the audio_file_path variable in this script with a valid audio file.")
        print("\nSupported formats: m4a, mp3, wav, aac, m4b, mp4")
        print("\nExample iPhone recording locations:")
        print("- Voice Memos app: Files > Voice Memos")
        print("- iCloud Drive: Voice Memos folder")
        print("- iTunes: Music folder")
        return
    
    try:
        # Transcribe the audio
        result = transcribe_audio_file(audio_file_path, model_size="base")
        
        print("\n✅ Transcription completed!")
        print(f"📝 Text: {result['text']}")
        print(f"🌍 Language: {result.get('language', 'Unknown')}")
        print(f"⏱️  Duration: {result.get('segments', [{}])[0].get('start', 0):.2f}s")
        
        # Save transcription to file
        output_file = f"{Path(audio_file_path).stem}_transcription.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Transcription of: {audio_file_path}\n")
            f.write(f"Language: {result.get('language', 'Unknown')}\n")
            f.write(f"Duration: {result.get('segments', [{}])[0].get('start', 0):.2f}s\n")
            f.write("-" * 50 + "\n")
            f.write(result['text'])
        
        print(f"\n💾 Transcription saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error during transcription: {str(e)}")
        print("Make sure you have installed the requirements: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
