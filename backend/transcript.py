from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from transformers import pipeline
import re
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
            time.sleep(delay)
    print(f"Failed to fetch transcript after {retries} attempts.")
    return None

def summarize_transcript(transcript):
    """
    Summarizes the transcript of a YouTube video.

    Args:
        transcript (str): The transcript of the YouTube video.

    Returns:
        str: A summary of the video's transcript.
    """
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(transcript, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    while True:
        url = input("Enter YouTube URL: ").strip()
        match = re.search(r"v=([^&]+)", url)
        if match:
            video_id = match.group(1)
            print(f"Extracted video ID: {video_id}")
            transcript = createTranscript(video_id)
            if transcript:
                print("Transcript fetched successfully!")
                print(transcript)
                summary = summarize_transcript(transcript)
                print("Summary:")
                print(summary)
            else:
                print("Failed to fetch transcript.")
        else:
            print("Invalid YouTube URL")
            break