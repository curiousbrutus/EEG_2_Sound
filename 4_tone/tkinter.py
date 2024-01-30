import tkinter as tk
from threading import Thread
import time
import numpy as np
from scipy.signal import butter, filtfilt
from sonecULES import EEGDevice, extract_audio_features, synthesize_music

class EEGMusicApp:
    def __init__(self, master):
        self.master = master
        self.master.title("EEG Music Generator")

        self.eeg_device = EEGDevice()
        self.synthesizer = None
        self.is_streaming = False

        # UI elements
        self.start_button = tk.Button(master, text="Start Streaming", command=self.start_streaming)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop Streaming", command=self.stop_streaming, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.quit_button = tk.Button(master, text="Quit", command=self.quit_app)
        self.quit_button.pack(pady=10)

        # EEG data variables
        self.eeg_data = np.zeros((22, 1024))  # Update with your actual EEG data shape

    def start_streaming(self):
        self.eeg_device.connect()
        self.is_streaming = True

        self.synthesizer = tk.Tk()  # Replace with your music generation setup
        self.synthesizer.title("Music Synthesizer")

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Start a thread for real-time EEG processing
        Thread(target=self.process_eeg_data).start()

    def stop_streaming(self):
        self.is_streaming = False
        self.eeg_device.disconnect()

        self.synthesizer.destroy()
        self.synthesizer = None

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def process_eeg_data(self):
        while self.is_streaming:
            new_data = self.eeg_device.read(1024)
            
            # Replace with your EEG feature extraction and music generation logic
            audio_features = extract_audio_features(new_data)
            music = synthesize_music(audio_features)

            # Update UI or play the music as needed
            # For simplicity, let's just print the generated music
            print("Generated Music:", music)

            time.sleep(0.1)  # Adjust the sleep time as needed

    def quit_app(self):
        if self.is_streaming:
            self.stop_streaming()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EEGMusicApp(root)
    root.mainloop()
