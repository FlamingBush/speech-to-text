import json
import os
from datetime import datetime


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def transcript_log_path(output_dir: str) -> str:
    ensure_dir(output_dir)
    date_str = datetime.now().strftime("%Y%m%d")
    return os.path.join(output_dir, f"transcripts_{date_str}.jsonl")


def save_transcript_entry(
    transcript_dir: str,
    audio_path: str,
    transcript_text: str,
) -> str:
    path = transcript_log_path(transcript_dir)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "audio_path": audio_path,
        "transcript": transcript_text,
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return path
