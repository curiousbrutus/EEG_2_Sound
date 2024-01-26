import numpy as np
import pandas as pd
import soundfile as sf

# Assuming you have the EEG sound wave data (replace this with your actual data)
eeg_sound_wave = np.random.rand(44100)  # Replace this line with your EEG data

# Normalize the EEG sound wave
eeg_sound_wave_normalized = eeg_sound_wave / np.max(np.abs(eeg_sound_wave))

# Save the EEG sound wave to .wav file
output_path = 'path/to/output/folder/'
sf.write(output_path + 'eeg_sound_wave.wav', eeg_sound_wave_normalized, 44100)

# Chords data (unchanged from your original code)
chords_data = pd.DataFrame({
    'Chord': ['Em', 'D', 'C', 'G', 'B7', 'Am', 'F', 'G7', 'E', 'A'],
    'Frequency1': [329.63, 293.66, 261.63, 392.00, 466.16, 440.00, 349.23, 392.00, 329.63, 440.00],
    'Frequency2': [392.00, 349.23, 329.63, 493.88, 587.33, 523.25, 440.00, 466.16, 392.00, 523.25],
    'Frequency3': [493.88, 440.00, 392.00, 587.33, 698.46, 659.25, 523.25, 587.33, 493.88, 659.25],
    'Duration': [3.0, 2.5, 2.5, 3.0, 3.0, 3.0, 2.5, 2.5, 3.0, 3.0]
})

# Generate sound waves from chords data
full_sound_wave = np.array([])

for index, row in chords_data.iterrows():
    chord_duration = int(row['Duration'] * 44100)
    time = np.arange(0, row['Duration'], 1 / 44100)
    chord_wave = np.sin(2 * np.pi * row['Frequency1'] * time) + \
                  np.sin(2 * np.pi * row['Frequency2'] * time) + \
                  np.sin(2 * np.pi * row['Frequency3'] * time)
    chord_wave /= np.max(np.abs(chord_wave))  # Normalize
    full_sound_wave = np.concatenate([full_sound_wave, chord_wave[:chord_duration]])

# Normalize the entire sound wave
full_sound_wave_normalized = full_sound_wave / np.max(np.abs(full_sound_wave))

# Save the complete music piece to .wav file
sf.write(output_path + 'complete_music_piece.wav', full_sound_wave_normalized, 44100)
