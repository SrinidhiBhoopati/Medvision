# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
#import elevenlabs
load_dotenv()

# Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS
import subprocess
import platform

# Function to play audio across platforms using ffplay
def play_audio(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath], shell=True)  # Use shell=True for Windows
        elif os_name == "Linux":  # Linux
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Function to convert text to speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    # Generate speech using gTTS
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    # Play the generated audio
    play_audio(output_filepath)

# Example Usage for gTTS
input_text = "MEDVISION-an ai powered medical chatbot"
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

# Example Usage for ElevenLabs (if uncommented and setup)
#input_text = "Hi, this is a test with ElevenLabs and ffplay!"
#text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="elevenlabs_testing_autoplay.mp3")
