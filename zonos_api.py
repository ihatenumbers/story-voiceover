from zyphra import ZyphraClient
import base64
import os

from dotenv import load_dotenv
load_dotenv()

client = ZyphraClient(api_key=os.environ["ZYPHRA_API_KEY"])

def audio_to_text(text, speaker, output_path):
    with open(speaker, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')

    client.audio.speech.create(
        text=text,
        speaker_audio=audio_base64,
        model="zonos-v0.1-transformer",
        output_path=output_path
    )
