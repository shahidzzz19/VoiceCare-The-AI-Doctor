import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# gTTS Function
def text_to_speech_with_gtts(input_text, output_filepath):
    audioobj = gTTS(text=input_text, lang="en", slow=False)
    audioobj.save(output_filepath)

    wav_filepath = output_filepath.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(output_filepath)
    audio.export(wav_filepath, format="wav")

    play_audio(wav_filepath)

# ElevenLabs Function
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

    wav_filepath = output_filepath.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(output_filepath)
    audio.export(wav_filepath, format="wav")

    play_audio(wav_filepath)

# Cross-platform Audio Player
def play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{filepath}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', filepath])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Audio playback error: {e}")

# Example usage
input_text = "Hi this is VoiceCare: The AI Doctor! Testing text to speech."
text_to_speech_with_gtts(input_text, "gtts_testing.mp3")
# text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing.mp3")