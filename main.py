import re
from backend.transcript import createTranscript
from backend.summarizer import analyze_and_summarize
from backend.video_download import video_creation

def main():
    print("Welcome to the YouTube Transcript Fetcher!")
    print("You can enter a YouTube URL to fetch the transcript.")
    while True:
        url = input("Enter YouTube URL: ")
        if url.startswith("https://www.youtube.com"):
            match = re.search(r"v=([^&]+)", url.strip())
            if match:
                video_id = match.group(1)
                print(f"Extracted video ID: {video_id}")
                transcript = createTranscript(video_id)
                print("Transcript fetched successfully!")
                video_creation(url, transcript)
                print(transcript)
                print("Analyzing and summarizing the transcript...")
                summary = analyze_and_summarize(transcript)
                print("Summary:")
                print(summary)
        else:
            print("Invalid YouTube URL")
            break

if __name__ == "__main__":
    main()