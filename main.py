import argparse
from recorder import record_wav
from storage import save_transcript_entry
from transcriber import SpeechToText


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Short-utterance recorder and transcriber using Vosk"
    )
    parser.add_argument(
        "--model",
        default="models/vosk-model-small-en-us-0.15",
        help="Path to the Vosk model directory",
    )
    parser.add_argument(
        "--audio-dir",
        default="sessions/audio",
        help="Directory where recorded WAV files are saved",
    )
    parser.add_argument(
        "--transcript-dir",
        default="sessions/transcripts",
        help="Directory where transcript logs are saved",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Recording duration in seconds",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Microphone sample rate",
    )

    args = parser.parse_args()

    print("Loading model...")
    stt = SpeechToText(args.model)
    print("Model loaded.")

    print("\nReady.")
    print("Press Enter to record a clip.")
    print("Type 'q' and press Enter to quit.\n")

    while True:
        user_input = input("> ").strip().lower()

        if user_input == "q":
            print("Goodbye.")
            break

        audio_path = record_wav(
            output_dir=args.audio_dir,
            duration_seconds=args.duration,
            sample_rate=args.sample_rate,
        )

        print("Transcribing...")
        transcript = stt.transcribe_wav_file(audio_path)

        if transcript:
            print(f"Transcript: {transcript}")
        else:
            print("Transcript: [no speech recognized]")

        log_path = save_transcript_entry(
            transcript_dir=args.transcript_dir,
            audio_path=audio_path,
            transcript_text=transcript,
        )

        print(f"Saved transcript log: {log_path}\n")


if __name__ == "__main__":
    main()
