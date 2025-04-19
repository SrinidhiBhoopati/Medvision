# Uncomment this section if you're using pipenv
from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

system_prompt = """
You have to act as a professional doctor, I know you are not, but this is for learning purposes.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Don't add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also, always answer as if you are answering to a real person.
Don't say 'In the image I see' but say 'With what I see, I think you have ....'
Don't respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please.
"""

def process_inputs(text_query, audio_filepath, image_filepath):
    speech_to_text_output = ""
    doctor_response = ""

    # Process text input if available
    if text_query:
        speech_to_text_output = text_query
    
    # Process audio input for speech-to-text conversion
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    
    # Process image input
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,  # Add text and speech input together
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # If only text or audio is provided, handle that case
    if not image_filepath and not text_query:
        doctor_response = "Please provide either text or an image for me to analyze."
    
    # If only audio is provided, handle it
    if not image_filepath and speech_to_text_output:
        doctor_response = "I could not analyze the image, but here is the information from your speech: " + speech_to_text_output
    
    # Convert the doctor's response to speech using ElevenLabs
    voice_of_doctor = text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor

# Create Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Textbox(label="Text Input", placeholder="Enter your query here..."),  # Text query input
        gr.Audio(sources=["microphone"], type="filepath", label="Audio Input"),  # Audio input
        gr.Image(type="filepath", label="Image Input")  # Image input
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3")
    ],
    title="MEDVISION",
    theme="default"
)

from fastapi import FastAPI, Response
import os

app = FastAPI()

def stream_audio(file_path: str):
    def iterfile():
        with open(file_path, "rb") as file_like:
            yield from file_like

    return Response(iterfile(), media_type="audio/wav")

@app.get("/audio")
def get_audio():
    # Get the file path in the same folder
    file_path = os.path.join(os.getcwd(), "final.wav")  # Replace with your audio file name
    return stream_audio(file_path)

from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_wav("final.wav")
play(sound)

# Launch the Gradio app
iface.launch(debug=True, share=True)
