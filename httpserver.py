import torch
from TeraTTS import TTS
from ruaccent import RUAccent
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import nest_asyncio
import uvicorn
import os
import soundfile as sf

accentizer = RUAccent()
accentizer.load(omograph_model_size='turbo', use_dictionary=True)
tts_version = TTS("TeraTTS/natasha-g2p-vits", add_time_to_end=1.0, tokenizer_load_dict=True)

def generate_audio(tts_version, text, save_path="combined_audio.wav", accentizer=accentizer):
    text = accentizer.process_all(text)
    audio = np.array([])
    i = 0
    for texts in range(1000, len(text), 1000):
# 'length_scale' можно использовать для замедления аудио для лучшего звучания (по умолчанию 1.1, указано здесь для примера)
        tts_res = tts_version(text[texts-1000:texts])
        # print(tts_res.shape, type(tts_res))
        # audio = np.hstack((audio, tts_res))  # Создать аудио. Можно добавить ударения, используя '+'
        tts_version.save_wav(tts_res, f"./text{i}.wav")
        i += 1
    try:
        # audio = np.hstack((audio, tts(text[i*1000:])))
        tts_res = tts_version(text[i*1000:])
        tts_version.save_wav(tts_res, f"./text{i}.wav")
    except:
        pass
    input_folder = "."
    concatenate_wavs(input_folder, save_path)
    return True

def concatenate_wavs(input_folder, output_file):
    concatenated_audio = []
    wav_files = []

    # Filter only wav files and sort them alphabetically
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):  # Changed condition here
            wav_files.append(os.path.join(input_folder, filename))
    wav_files.sort()  # Important for consistent order. You can remove if order doesn't matter.

    if not wav_files:
        print("No WAV files found in the input folder.")
        return

    # Get the samplerate from the first file (assuming it's the same for all)
    filepath = wav_files[0]  # Use the first WAV file
    try:
        _, samplerate = sf.read(filepath)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    for filepath in wav_files:
        try:
            audio, _ = sf.read(filepath)
            concatenated_audio.extend(audio)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            continue  # Skip to the next file if there's an error

    concatenated_audio = np.array(concatenated_audio)  # Convert to NumPy array

    try:
        sf.write(output_file, concatenated_audio, samplerate)
        print(f"Successfully concatenated audio to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os

app = FastAPI()
UPLOAD_DIR = "upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@app.post("/upload")
async def upload_file(file: UploadFile):
    print(file.filename)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    print(file_path)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename, "status": "uploaded"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, (filename+".txt"))
    if not os.path.exists(file_path):
        return {"error" : "File not found!"}
    with open(f'{filename}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    generate_audio(tts_version, text, save_path=f"./{filename}.wav")
    return FileResponse(file_path, filename=filename)

nest_asyncio.apply()
uvicorn.run(app, host="127.0.0.1", port=8000)