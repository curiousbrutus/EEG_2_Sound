import threading
import time
import copy
from brainaccess.connect import SSVEP
from brainaccess.core.eeg_manager import EEGManager
import ssvep
import display
import keyboard


class Predict:
    """Prediction logic of SSVEP"""

    def __init__(self, main_app, eeg, prediction_time: float = 4, note_values=[], notes=[], note_duration=0.5):
        self.mutex = threading.Lock()
        self.eeg = eeg
        self.main_app = main_app
        self.guess: int = 0
        self.passed: bool = False
        self.sample_rate: int = 250
        self.prediction_time: float = prediction_time
        self.note_values = note_values
        self.notes = notes
        self.note_duration = note_duration
        self.threshold = 1.5
        self.clf = SSVEP()
        self.frequencies = []

    def prep_data(self, annot: bool = True):
        data = self.eeg.get_mne(
            tim=self.prediction_time, annotations=annot
        ).pick_channels(["O1", "O2"], ordered=True)
        data = data.filter(1, 90, method="fir", verbose=False)
        return data.get_data()

    def get_guess(self):
        guess = None
        pass_guess = False
        try:
            with self.mutex:
                guess = copy(self.guess)
                pass_guess = copy(self.passed)
        except Exception:
            logging.error("failed get guess")
        return guess, pass_guess

    def _pred(self):
        while self.thread_flag:
            time.sleep(1)
            data = self.prep_data(annot=False)
            try:
                guess, score = self.clf.predict(data, self.frequencies, self.sample_rate)
                with self.mutex:
                    self.guess = guess
                    self.score = score
                self.passed = self.score > self.threshold
            except Exception:
                self.guess = 9
                self.passed = False
            self.main_app.get_keys()
            if "q" in self.main_app.keys:
                self.thread_flag = False
                logging.info("user quit by pressing q")
                break
            if self.guess in self.notes:
                if self.passed:
                    self.main_app.play_note(self.note_values[self.guess])
                    self.notes.remove(self.guess)
            play_chord = False
            if len(self.notes) == 0:
                play_chord = True

            if play_chord:
                chord = []
                for n in self.notes:
                    chord.append(self.note_values[n])
                self.main_app.play_chord(chord)
                self.thread_flag = False
                # print("All notes played")
                # logging.info("all notes played")
                break

    def start(self):
        self.thread_flag = True
        self.feed_thread = threading.Thread(target=self._pred)
        self.feed_thread.start()

    def stop(self):
        self.thread_flag = False
        self.feed_thread.join()


@click.command()
@click.option(
    "--full_screen", type=bool, help="Display stimulation full screen?", default=True
)
@click.option(
    "--prediction_interval",
    type=float,
    help="Prediction interval (sec)",
    default=4,
)
@click.option(
    "--note_values", type=str, help="The values of the notes to play.", default="262,294,330"
)
@click.option(
    "--notes", type=str, help="The notes to play.", default="C,D,E"
)
@click.option(
    "--port", type=str, help="Default
