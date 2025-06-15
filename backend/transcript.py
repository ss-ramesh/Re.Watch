import subprocess
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import time

def createTranscript(video_id, retries=3, delay=2):
    """
    Creates a transcript for a YouTube video given its video ID, with retry logic.

    Args:
        video_id (str): The ID of the YouTube video.
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.

    Returns:
        str: The full transcript of the video, or None if unavailable.
    """
    ytt_api = YouTubeTranscriptApi()
    for attempt in range(retries):
        try:
            fetched_transcript = ytt_api.fetch(video_id)
            transcript_lines = [snippet.text for snippet in fetched_transcript]
            return "\n".join(transcript_lines)
        except NoTranscriptFound:
            print(f"No transcript found for video ID: {video_id}.")
            return None
        except TranscriptsDisabled:
            print(f"Transcripts are disabled for video ID: {video_id}.")
            return None
        except Exception as e:
            print(f"Error fetching transcript (attempt {attempt + 1}): {e}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "youtube_transcript_api"])
            time.sleep(delay)
    print(f"Failed to fetch transcript after {retries} attempts.")
    return None