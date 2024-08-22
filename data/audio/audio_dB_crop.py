import os
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
from pydub import AudioSegment

'''
Extracts human voice segments from an audio file and creates a new audio file with the detected voice segments 
within a 10-second duration.

Args:
    audio_file (str): Path to the input audio file. If the file format is .m4a, it will be converted to .wav.
    
Returns:
    save_file (str): Path to the saved audio file with detected voice segments.
'''

def detect_human_voice(audio_file):
    '''
    Detects human voice segments in an audio file.

    Args:
        audio_file (str): Path to the input audio file.

    Returns:
        voice_indices (list): List containing indices of the detected voice segments.
    '''
    # Read the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Detect voice activity
    # ----- Need to Modify threshold-----#
    voice_segments = librosa.effects.split(y, top_db=18)

    # Generate indices of voice segments
    voice_indices = []
    for start, end in voice_segments:
        voice_indices.extend(range(start, end))

    return voice_indices

def save_full_audio_with_detected_voice(audio_file, save_file):
    '''
    Saves the full audio file with detected voice segments.

    Args:
        audio_file (str): Path to the input audio file.
        save_file (str): Path to save the audio file with detected voice segments.
    '''
    # Read the entire audio file
    y, sr = librosa.load(audio_file, sr=None)

    # Detect human voice segments and get their indices
    voice_indices = detect_human_voice(audio_file)

    # Extract human voice segments using the indices
    combined_audio = y[voice_indices]

    # Save the extracted audio segments to a file
    sf.write(save_file, combined_audio, sr)

    # Visualize and save the waveform of the original and detected voice segments
    plt.figure(figsize=(12, 6))

    # Original audio waveform
    plt.subplot(2, 1, 1)
    plt.plot(y)
    plt.title("Original Audio Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    # Waveform of detected voice segments
    plt.subplot(2, 1, 2)
    plt.plot(combined_audio)
    plt.title("Detected Voice Waveform")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")

    plt.tight_layout()
    save_path = os.path.join(os.path.dirname(save_file), 'result')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_file_path = os.path.join(save_path, os.path.basename(save_file[:-4] + "_waveform_comparison.png"))
    plt.savefig(save_file_path)

    # Save the extracted audio segments to a file
    audio_save_file_path = os.path.join(save_path, os.path.basename(save_file))
    sf.write(audio_save_file_path, combined_audio, sr)

    plt.show()

# Define paths for the original file and the file to save with detected voice segments
# ------Need to modify path------ #
audio_file_path = "voice2face-data/audio/input.m4a"
save_file_path = "voice2face-data/audio/detected_voice.wav"

# Check if the file extension is ".m4a" for conversion and processing
if audio_file_path.endswith('.m4a'):
    # Convert m4a file to wav format
    wav_path = audio_file_path[:-4] + ".wav"
    audio = AudioSegment.from_file(audio_file_path)
    audio.export(wav_path, format="wav")
    # Process the converted wav file
    save_full_audio_with_detected_voice(wav_path, save_file_path)
else:
    # Process the original file without conversion
    save_full_audio_with_detected_voice(audio_file_path, save_file_path)
