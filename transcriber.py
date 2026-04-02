import json
from vosk import Model, KaldiRecognizer


class SpeechToText:
    def __init__(self, model_path: str, sample_rate: int) -> None:
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)

    def accept_audio(self, audio_bytes: bytes) -> dict:
        try:
            if self.recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(self.recognizer.Result())
                return {
                    "type": "final",
                    "text": result.get("text", "").strip(),
                }
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] Result() parse error: {e}", flush=True)
            return {"type": "error", "text": ""}

        try:
            partial = json.loads(self.recognizer.PartialResult())
            return {
                "type": "partial",
                "text": partial.get("partial", "").strip(),
            }
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] PartialResult() parse error: {e}", flush=True)
            return {"type": "error", "text": ""}

    def final_result(self) -> str:
        try:
            result = json.loads(self.recognizer.FinalResult())
            return result.get("text", "").strip()
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] FinalResult() parse error: {e}", flush=True)
            return ""
