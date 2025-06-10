from TeraTTS import TTS
from ruaccent import RUAccent
import numpy as np
import torch

from preprocess_files import concatenate_wavs

class TeraTTSClass:
    def __init__(self, version="TeraTTS/natasha-g2p-vits",
                  add_time_to_end=1.0, tokenizer_load_dict=True, 
                  omograph_model_size='turbo', use_dictionary=True):
        self.teratts = TTS(version, 
                           add_time_to_end=add_time_to_end, 
                           tokenizer_load_dict=tokenizer_load_dict)
        self.accentizer = RUAccent()
        self.accentizer.load(omograph_model_size=omograph_model_size, use_dictionary=use_dictionary)
    
    
    def generate_audio(self, text, save_path="combined_audio.wav"):
        text = self.accentizer.process_all(text)
        audio = np.array([])
        i = 0
        for texts in range(1000, len(text), 1000):
            tts_res = self.teratts(text[texts-1000:texts])
            # print(tts_res.shape, type(tts_res))
            # audio = np.hstack((audio, tts_res))  # Создать аудио. Можно добавить ударения, используя '+'
            self.teratts.save_wav(tts_res, f"./text{i}.wav")
            i += 1
        try:
            # audio = np.hstack((audio, tts(text[i*1000:])))
            tts_res = self.teratts(text[i*1000:])
            self.teratts.save_wav(tts_res, f"./text{i}.wav")
        except:
            pass
        input_folder = "."
        concatenate_wavs(input_folder, save_path)
        return True
    

