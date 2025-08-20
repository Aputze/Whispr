import gradio as gr
import tempfile
import os
import time
from faster_whisper import WhisperModel

def transcribe_audio(audio_file, model_size):
    """Transcribe audio using Whisper model"""
    if audio_file is None:
        return "Please upload an audio file."
    
    try:
        # Load the model
        print(f"Loading {model_size} model...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        
        # Advanced transcription parameters for better accuracy
        transcribe_params = {
            "beam_size": 10,
            "best_of": 10,
            "temperature": 0.0,
            "condition_on_previous_text": True,
            "word_timestamps": True,
            "compression_ratio_threshold": 2.4,
            "log_prob_threshold": -1.0,
            "no_speech_threshold": 0.6,
            "initial_prompt": "This is Hebrew speech. Please transcribe accurately with proper Hebrew grammar and pronunciation.",
            "language": "he"  # Force Hebrew for better accuracy
        }
        
        print("Starting transcription...")
        segments, info = model.transcribe(audio_file, **transcribe_params)
        
        # Extract and clean transcription text
        transcription_text = ""
        segments_list = list(segments)
        
        total_confidence = 0
        valid_segments = 0
        
        for segment in segments_list:
            clean_text = segment.text.strip()
            if clean_text:
                # Hebrew text processing
                clean_text = clean_text.replace("  ", " ")
                clean_text = clean_text.replace(" .", ".")
                clean_text = clean_text.replace(" ,", ",")
                clean_text = clean_text.replace(" ?", "?")
                clean_text = clean_text.replace(" !", "!")
                
                transcription_text += clean_text + " "
                
                # Calculate confidence
                if hasattr(segment, 'avg_logprob'):
                    total_confidence += segment.avg_logprob
                    valid_segments += 1
        
        # Final text cleanup
        transcription_text = transcription_text.strip()
        while "  " in transcription_text:
            transcription_text = transcription_text.replace("  ", " ")
        
        if transcription_text and not transcription_text.endswith(('.', '!', '?')):
            transcription_text += "."
        
        # Calculate confidence percentage
        avg_confidence = (total_confidence / valid_segments) if valid_segments > 0 else 0
        confidence_percentage = min(100, max(0, (avg_confidence + 2) * 25))
        
        # Calculate duration
        duration = segments_list[-1].end if segments_list else 0
        
        # Format result with metadata
        result = f"""**Transcription:**
{transcription_text}

**Metadata:**
• Language: {info.language}
• Duration: {duration:.1f} seconds
• Confidence: {confidence_percentage:.1f}%
• Model: {model_size}"""
        
        print("Transcription completed successfully!")
        return result
        
    except Exception as e:
        error_msg = f"Error during transcription: {str(e)}"
        print(error_msg)
        return error_msg

# Create the Gradio interface
def create_interface():
    with gr.Blocks(
        title="Whispr - Audio Transcription",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 800px !important;
            margin: auto !important;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        """
    ) as demo:
        
        gr.Markdown(
            """
            <div class="header">
            
            # 🎤 Whispr
            ### Audio Transcription with OpenAI Whisper
            
            Upload your audio file and choose a model size for transcription.
            Optimized for Hebrew speech but works with multiple languages.
            
            </div>
            """,
            elem_classes="header"
        )
        
        with gr.Row():
            with gr.Column(scale=2):
                audio_input = gr.Audio(
                    label="📁 Upload Audio File",
                    type="filepath",
                    sources=["upload", "microphone"]
                )
                
                model_dropdown = gr.Dropdown(
                    choices=["tiny", "base", "small", "medium", "large"],
                    value="small",
                    label="🤖 Choose Whisper Model",
                    info="Larger models are more accurate but slower"
                )
                
                transcribe_btn = gr.Button(
                    "🚀 Transcribe Audio",
                    variant="primary",
                    size="lg"
                )
            
            with gr.Column(scale=3):
                output_text = gr.Textbox(
                    label="📝 Transcription Result",
                    placeholder="Upload an audio file and click 'Transcribe Audio' to see the result here...",
                    lines=15,
                    max_lines=20,
                    show_copy_button=True
                )
        
        # Add model size information
        gr.Markdown(
            """
            ### Model Information:
            - **Tiny (39MB)**: Fastest, basic accuracy
            - **Base (74MB)**: Good balance of speed and accuracy  
            - **Small (244MB)**: Better accuracy, recommended
            - **Medium (769MB)**: High accuracy, slower
            - **Large (1550MB)**: Best accuracy, slowest
            """
        )
        
        # Connect the transcribe button to the function
        transcribe_btn.click(
            fn=transcribe_audio,
            inputs=[audio_input, model_dropdown],
            outputs=output_text,
            show_progress=True
        )
        
        # Auto-transcribe when audio is uploaded
        audio_input.change(
            fn=transcribe_audio,
            inputs=[audio_input, model_dropdown],
            outputs=output_text,
            show_progress=True
        )
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
