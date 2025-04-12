import logging
import os
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Key (Use .env if needed)
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your_fallback_key_here"
stt_model = "whisper-large-v3"

# Step 1: Record audio from mic
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking...")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"Error recording audio: {e}")

# Step 2: Transcribe using Groq Whisper
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
            logging.info(f"Transcription: {transcription.text}")
            return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    audio_file = "patient_voice.mp3"
    record_audio(audio_file, timeout=10)
    transcription = transcribe_with_groq(stt_model, audio_file, GROQ_API_KEY)
    print(f"Patient said: {transcription}")