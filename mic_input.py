import queue
import sounddevice as sd
from transcriber import SpeechToText


def transcribe_microphone(model_path: str, sample_rate: int = 16000) -> None:
    audio_queue: queue.Queue[bytes] = queue.Queue()
    stt = SpeechToText(model_path=model_path, sample_rate=sample_rate)

    def callback(indata, frames, time, status) -> None:
        if status:
            print(status)
        audio_queue.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=sample_rate,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        print("Listening... Press Ctrl+C to stop.")
        while True:
            data = audio_queue.get()
            result = stt.accept_audio(data)

            if result["type"] == "final" and result["text"]:
                print(f"\nFinal: {result['text']}")
            elif result["type"] == "partial" and result["text"]:
                print(f"\rPartial: {result['text']}", end="", flush=True)
