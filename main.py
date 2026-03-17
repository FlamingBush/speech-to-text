import argparse
from file_input import transcribe_wav_file
from mic_input import transcribe_microphone


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline speech-to-text with Vosk")
    parser.add_argument(
        "--model",
        default="models/en-us",
        help="Path to the Vosk model directory",
    )
    parser.add_argument(
        "--file",
        help="Path to a WAV file to transcribe",
    )
    parser.add_argument(
        "--mic",
        action="store_true",
        help="Use live microphone input",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=16000,
        help="Sample rate for microphone input",
    )

    args = parser.parse_args()

    if args.file:
        transcribe_wav_file(args.file, args.model)
    elif args.mic:
        transcribe_microphone(args.model, args.sample_rate)
    else:
        parser.error("Use either --file <wavfile> or --mic")


if __name__ == "__main__":
    main()
