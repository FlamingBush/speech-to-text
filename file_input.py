import wave
from transcriber import SpeechToText


def transcribe_wav_file(filename: str, model_path: str) -> None:
    with wave.open(filename, "rb") as wf:
        if wf.getnchannels() != 1:
            raise ValueError("Audio file must be mono.")
        if wf.getsampwidth() != 2:
            raise ValueError("Audio file must be 16-bit PCM.")
        if wf.getcomptype() != "NONE":
            raise ValueError("Audio file must be uncompressed PCM WAV.")

        sample_rate = wf.getframerate()
        stt = SpeechToText(model_path=model_path, sample_rate=sample_rate)

        while True:
            data = wf.readframes(4000)
            if not data:
                break

            result = stt.accept_audio(data)
            if result["type"] == "final" and result["text"]:
                print(f"Final: {result['text']}")

        tail = stt.final_result()
        if tail:
            print(f"Final tail: {tail}")
