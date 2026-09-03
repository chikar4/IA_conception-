import time

import keyboard
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
PUSH_TO_TALK_KEY = "space"

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = WhisperModel("base", device="cpu", compute_type="int8")
    return _model


def wait_for_push_to_talk(poll_interval=0.05, cancel_key=None):
    """Blocks until PUSH_TO_TALK_KEY is pressed. Returns False if cancel_key
    is pressed first."""
    while True:
        if cancel_key and keyboard.is_pressed(cancel_key):
            return False
        if keyboard.is_pressed(PUSH_TO_TALK_KEY):
            return True
        time.sleep(poll_interval)


def record_audio():
    """Records audio from the mic while PUSH_TO_TALK_KEY stays held down."""
    frames = []

    def callback(indata, frames_count, time_info, status):
        frames.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
        while keyboard.is_pressed(PUSH_TO_TALK_KEY):
            sd.sleep(50)

    if not frames:
        return np.zeros((0,), dtype=np.float32)

    return np.concatenate(frames, axis=0).flatten()


def transcribe(audio, language="fr"):
    if audio.size == 0:
        return ""
    model = _get_model()
    segments, _ = model.transcribe(audio, language=language)
    return " ".join(segment.text.strip() for segment in segments).strip()
