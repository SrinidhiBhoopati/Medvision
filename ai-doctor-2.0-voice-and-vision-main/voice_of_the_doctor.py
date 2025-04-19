import os
from gtts import gTTS
from elevenlabs import Voice, stream, save
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key for ElevenLabs
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Function to convert text to speech using Google Text-to-Speech (gTTS)
def text_to_speech_with_gtts(input_text, output_filepath):
    try:
        # Generate speech and save it as an MP3 file
        audioobj = gTTS(text=input_text, lang="en", slow=False)
        audioobj.save(output_filepath)
        print(f"GTTS Audio saved at {output_filepath}")
    except Exception as e:
        print(f"Error in GTTS: {e}")

# Function to convert text to speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    try:
        # Specify the voice model and other parameters
        voice = Voice(name="Aria", model="eleven_monolingual_v1")
        # Generate the audio using ElevenLabs API
        audio = stream(
            text=input_text,
            voice=voice,
        )
        # Save the generated audio
        save(audio, output_filepath)
        print(f"ElevenLabs Audio saved successfully at {output_filepath}")
    except Exception as e:
        print(f"Error in ElevenLabs: {e}")

# Function to convert MP3 to WAV using pydub
def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    try:
        # Load the MP3 file and export it as a WAV file
        sound = AudioSegment.from_mp3(mp3_filepath)
        sound.export(wav_filepath, format="wav")
        print(f"Converted MP3 to WAV at {wav_filepath}")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")

# Function to play WAV audio
def play_audio_wav(wav_filepath):
    try:
        # Load and play the WAV file using pydub
        sound = AudioSegment.from_wav(wav_filepath)
        play(sound)
        print(f"Playing WAV audio from {wav_filepath}")
    except Exception as e:
        print(f"An error occurred while trying to play the WAV file: {e}")

# Test the ElevenLabs function (generate MP3 using ElevenLabs)
text_to_speech_with_elevenlabs("Hello, this is a test.", "final.mp3")

# Convert the generated MP3 to WAV (optional step)
convert_mp3_to_wav("final.mp3", "final.wav")

# Play the WAV file (optional step)
play_audio_wav("final.wav")
