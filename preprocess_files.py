import os
import soundfile as sf
import numpy as np
import inspect

def get_classes_from_module(module):
    classes = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and obj.__module__ == module.__name__:
            classes[name] = obj
    return classes

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