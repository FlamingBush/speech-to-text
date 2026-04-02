import json
from vosk import Model, KaldiRecognizer


class SpeechToText:
    def __init__(self, model_path: str, sample_rate: int) -> None:
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.recognizer.SetWords(True)  # enable per-word confidence scores

    def accept_audio(self, audio_bytes: bytes) -> dict:
        try:
            if self.recognizer.AcceptWaveform(audio_bytes):
                result = json.loads(self.recognizer.Result())
                words = result.get("result", [])
                confidence = (
                    sum(w.get("conf", 1.0) for w in words) / len(words)
                    if words else None
                )
                return {
                    "type": "final",
                    "text": result.get("text", "").strip(),
                    "confidence": confidence,
                }
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] Result() parse error: {e}", flush=True)
            return {"type": "error", "text": "", "confidence": None}

        try:
            partial = json.loads(self.recognizer.PartialResult())
            return {
                "type": "partial",
                "text": partial.get("partial", "").strip(),
                "confidence": None,
            }
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] PartialResult() parse error: {e}", flush=True)
            return {"type": "error", "text": "", "confidence": None}

    def final_result(self) -> str:
        try:
            result = json.loads(self.recognizer.FinalResult())
            return result.get("text", "").strip()
        except (json.JSONDecodeError, Exception) as e:
            print(f"[transcriber] FinalResult() parse error: {e}", flush=True)
            return ""
