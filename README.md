# speech-to-text

## Option A: Local whisper (original assignment)

```bash
bash setup.sh
pip install -r requirements.txt
yt-dlp <video-url>
whisper <downloaded-video-file> --model small
```

## Option B: Groq API (whisper-large-v3-turbo)

1. Get a free API key at https://console.groq.com/keys
2. Set it in your environment:

   ```bash
   export GROQ_API_KEY="your-key-here"
   ```

3. Run the transcription script on your downloaded video:

   ```bash
   python groq_transcribe.py <downloaded-video-file>
   ```

The transcript is saved as `<video-name>.groq.txt` with timestamps printed to the terminal. Groq's API has a 25 MB upload limit, so the script automatically extracts the audio with ffmpeg when a file is too large.

## Evaluation

**Video transcribed:** (paste the YouTube URL here)

**Method used:** (local `whisper --model small` and/or Groq `whisper-large-v3-turbo`)

**Results compared to the video:**

- Accuracy of the transcription: (how well did it match what was actually said?)
- Speed: (local whisper vs. the Groq API)
- Errors noticed: (missed words, wrong names, punctuation, etc.)

Here are my expansive thoughts. 
