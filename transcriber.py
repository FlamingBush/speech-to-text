import json
import wave
from vosk import Model, KaldiRecognizer


class SpeechToText:
    def __init__(self, model_path: str) -> None:
        self.model = Model(model_path)

    def transcribe_wav_file(self, filename: str) -> str:
        with wave.open(filename, "rb") as wf:
            if wf.getnchannels() != 1:
                raise ValueError("Audio file must be mono.")
            if wf.getsampwidth() != 2:
                raise ValueError("Audio file must be 16-bit PCM.")
            if wf.getcomptype() != "NONE":
                raise ValueError("Audio file must be uncompressed PCM WAV.")

            recognizer = KaldiRecognizer(self.model, wf.getframerate())
            results = []

            while True:
                data = wf.readframes(4000)
                if not data:
                    break

                if recognizer.AcceptWaveform(data):
                    chunk_result = json.loads(recognizer.Result())
                    text = chunk_result.get("text", "").strip()
                    if text:
                        results.append(text)

            final_result = json.loads(recognizer.FinalResult())
            final_text = final_result.get("text", "").strip()
            if final_text:
                results.append(final_text)

            return " ".join(results).strip()
