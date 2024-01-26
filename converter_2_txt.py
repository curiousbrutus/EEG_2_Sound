import mne

# Load the EEG data from the .set file
raw = mne.io.read_raw_eeglab('/home/jobbe/BrainAccess/Data/5_min_Music_stim/subj-2_ses-S001_task-music_stimuli_run-001_20240126_124126_eeg_09569e43-1ce9-46e8-9318-80dfba614930-raw.set', preload=True)

# Convert to a Pandas DataFrame
df = raw.to_data_frame()

# Save the DataFrame to a text file
df.to_csv('/home/jobbe/BrainAccess/Data/EEG_Eyyub/Converted Data/output_music_stim_run-001.txt', index=False, sep='\t')
