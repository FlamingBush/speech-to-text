import os
import wave
from datetime import datetime

import numpy as np
import sounddevice as sd


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def timestamp_string() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def record_wav(
    output_dir: str,
    duration_seconds: int = 5,
    sample_rate: int = 16000,
    channels: int = 1,
) -> str:
    """
    Record audio from the default microphone and save it as a WAV file.
    Returns the path to the saved file.
    """
    ensure_dir(output_dir)

    filename = f"clip_{timestamp_string()}.wav"
    filepath = os.path.join(output_dir, filename)

    print(f"Recording for {duration_seconds} seconds...")

    audio = sd.rec(
        int(duration_seconds * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="int16",
    )
    sd.wait()

    with wave.open(filepath, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # int16 = 2 bytes
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    print(f"Saved audio: {filepath}")
    return filepath
