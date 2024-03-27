import librosa
import numpy as np
import matplotlib.pyplot as plt

'''
You can determine the minimum, maximum, and average dB values 
to set a threshold for identifying voice regions based on dB levels. 
After visually inspecting the waveform and setting a threshold,
adding 80 to it, you can conveniently apply this threshold value to `audio_crop.py`.
'''

# Load audio file
audio_path = "voice2face-data/audio/input.wav"
y, sr = librosa.load(audio_path, sr=None)

# Calculate spectrum and check maximum and minimum dB values
D = librosa.amplitude_to_db(librosa.stft(y), ref=np.max)
max_db = np.max(D)
min_db = np.min(D)

# Set threshold value
threshold_db = -60

# Consider regions with dB values above the threshold as voice regions
voice_indices = np.where(D > threshold_db)

print("Threshold:", threshold_db)
print("Maximum dB value in regions with voice:", np.max(D[voice_indices]))
print("Minimum dB value in regions with voice:", np.min(D[voice_indices]))

# Calculate average dB value in regions with voice
average_db = np.mean(D[voice_indices])
print("Average dB value in regions with voice:", average_db)

# Plot waveform and spectrum
plt.figure(figsize=(12, 6))

# Plot waveform
plt.subplot(2, 1, 1)
plt.plot(y)
plt.title("Waveform")
plt.xlabel("Sample")
plt.ylabel("Amplitude")

# Plot spectrum
plt.subplot(2, 1, 2)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Log-frequency power spectrogram')

plt.tight_layout()
plt.show()
