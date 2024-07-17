"""
    Class for real time speech recognition , translation to bytes , array, then pass it to 
    LLM to create request-response by voice chatting.
"""

import torch
from transformers import pipeline
import librosa
import io


# Byte -> Array Transformation
def convert_bytes_to_array(audio_bytes):
    audio_bytes = io.BytesIO(audio_bytes)
    audio , sample_rate = librosa.load(audio_bytes)
    print(sample_rate)
    return audio


# Creates desired model , converts bytes to array, make predictions and return them.
def transcribe_audio(audio_bytes):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    pipe = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-small",
    chunk_length_s=30,
    device=device,
    )
    audio_array = convert_bytes_to_array(audio_bytes)
    prediction = pipe(audio_array, batch_size=1)["text"]
    return prediction
