# Re.Watch
Youtube Summarizer / Video-to-Tik Tok Format Using Youtube API for rewatched moments

# New Layout

Transcript.py: 
- Case 1: Uses VTT for transcript with time intervals
- Case 2: Downloads whole video audio and uses Whisper model for transcripting.

Video_download.py:
- Def extract_moments: Using important keywords / start of most rewatched moments, works in partner of the transcript to download clips of full sentences so no words are broken. However, need edge case protection for when a most rewatched moment doesn't have audio.
- Def download_clips: just takes the seconds and downloads the clips of the video

Summarizer.py:
- Takes the transcript and uses an open-source LLM to write a few paragraphs of the video.
- Writes auto-complete query questions for the user to ask.

