#!/usr/bin/env python3
"""Transcribe an audio/video file using Groq's whisper-large-v3-turbo model.

Usage:
    python groq_transcribe.py <path-to-media-file>

Requires a GROQ_API_KEY environment variable.
Get a free key at https://console.groq.com/keys
"""

import os
import sys
from pathlib import Path

from groq import Groq

MAX_FILE_SIZE = 25 * 1024 * 1024  # Groq API limit: 25 MB


def extract_audio(input_path: Path) -> Path:
    """Extract audio to a small mp3 so large video files fit the API limit."""
    output_path = input_path.with_suffix(".groq_audio.mp3")
    os.system(
        f'ffmpeg -y -i "{input_path}" -vn -ac 1 -ar 16000 -b:a 64k "{output_path}" '
        "-loglevel error"
    )
    return output_path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python groq_transcribe.py <path-to-media-file>")
        sys.exit(1)

    media_path = Path(sys.argv[1])
    if not media_path.exists():
        print(f"File not found: {media_path}")
        sys.exit(1)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Please set your GROQ_API_KEY environment variable.")
        print("Get a free key at https://console.groq.com/keys")
        sys.exit(1)

    # Groq's API limit is 25 MB; extract audio if the file is too big
    upload_path = media_path
    if media_path.stat().st_size > MAX_FILE_SIZE:
        print("File too large for the API — extracting audio first...")
        upload_path = extract_audio(media_path)

    client = Groq(api_key=api_key)

    print(f"Transcribing {upload_path.name} with whisper-large-v3-turbo...")
    with open(upload_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(upload_path.name, audio_file),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    # Write the transcript next to the media file
    output_txt = media_path.with_suffix(".groq.txt")
    with open(output_txt, "w") as f:
        f.write(transcription.text + "\n")

    print(f"\nTranscript saved to: {output_txt}\n")
    print("----- Transcript -----")
    for segment in transcription.segments:
        start = segment["start"] if isinstance(segment, dict) else segment.start
        end = segment["end"] if isinstance(segment, dict) else segment.end
        text = segment["text"] if isinstance(segment, dict) else segment.text
        print(f"[{start:7.2f}s - {end:7.2f}s] {text}")

    # Clean up the temporary audio file
    if upload_path != media_path:
        upload_path.unlink()


if __name__ == "__main__":
    main()
