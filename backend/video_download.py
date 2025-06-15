import json
import subprocess
import sys
import os
import shutil

storage_path = '/Users/santoshramesh/Desktop/Re.Watch/Re.Watch/storage'

def clearing_storage():
    if os.path.exists(storage_path):
        shutil.rmtree(storage_path)
        print(f"Storage cleared: {storage_path} has been removed.")
    else:
        print(f"No storage found at: {storage_path}")
    os.makedirs("/Users/santoshramesh/Desktop/Re.Watch/Re.Watch/storage", exist_ok=True) 

def get_heat_map(video_url):
    """
    Fetches the heat map data for a YouTube video using yt-dlp.
    
    Args:
        video_url (str): The URL of the YouTube video.
    
    Returns:
        dict: Heat map data if available, otherwise None.
    """
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--skip-download",
        video_url
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        video_info = json.loads(result.stdout).get('heatmap', None)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching heat map: {e}")
        return None

def creation_video(video_url):
    clearing_storage()
    cmd = [
        "yt-dlp",
        "-f", "bv*+ba/best",   # Fallback to best if no separate streams
        "--merge-output-format", "mp4",
        "-o", os.path.join(storage_path, "%(title)s.%(ext)s"),
        video_url
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Download completed and saved in: {storage_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    creation_video(video_url)
    heat_map_data = get_heat_map(video_url)
    if heat_map_data:
        print("Heat map data fetched successfully:")
        print(heat_map_data)
    else:
        print("No heat map data available for this video.")