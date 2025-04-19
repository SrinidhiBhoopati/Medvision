from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# The system prompt for medical analysis
system_prompt = """
You have to act as a professional doctor, I know you are not, but this is for learning purposes. 
What's in this image? Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Don’t add any numbers or special characters in your response. 
Your response should be in one long paragraph. Also, always answer as if you are answering to a real person. 
Don’t say 'In the image I see' but say 'With what I see, I think you have...'. 
Don’t respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away, please.
"""

def process_inputs(text_input, audio_filepath, image_filepath):
    # If text and image are provided
    if text_input and image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + text_input,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    # If audio and image are provided
    elif audio_filepath and image_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        return "You must provide both an image and either audio or text.", None, None

    # Convert doctor's response to speech
    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output if audio_filepath else text_input, doctor_response, voice_of_doctor


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Textbox(placeholder="Type your symptoms or questions here (optional)", label="Text Input"),
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath", label="Upload Image")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text or Text Input"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("final.mp3", label="Doctor's Voice")
    ],
    title="MEDVISION",
    description="Provide an image along with either audio or text for a medical diagnosis response.",
    
)

iface.launch(debug=True)