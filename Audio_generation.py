from TeraTTS import TTS
from russcent import RUSAccent
import numpy
import torch

accentizer = RUAccent()
accentizer.load(omogtaph_model_size='turbo', use_dictionary=True)

def generate_audio(tts_version, text, save_path="./text.wav", accentizer=accentizer):
    text = accentizer.process_all(text)
    audio = tts_version(text)
    tts_version.save_wav(audio, save_path)
    return True
