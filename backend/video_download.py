import json
import subprocess
import os
import shutil
from numpy import floor

storage_path = '/Users/santoshramesh/Desktop/Re.Watch/Re.Watch/storage'
clip_length = 10.0  # Length of each clip in seconds
extract_multiplier = 0.5  # Multiplier for the number of clips to extract

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
        return video_info
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching heat map: {e}")
        return None
    
def extract_moments(heat_map: list, multiplier):
    selected_clips = []

    video_duration = heat_map[-1]['end_time']
    max_clips = min(10, floor(video_duration / 10 * multiplier))
    ranked_segments = sorted(heat_map, key=lambda x: -x['value'])
    selected_clips = []
    used_ranges = []

    for seg in ranked_segments:
        seg_len = seg['end_time'] - seg['start_time']
        seg_center = (seg['start_time'] + seg['end_time']) / 2

        # CASE 1: Segment is longer than clip_length
        if seg_len > clip_length:
            current_start = seg['start_time']
            while current_start + clip_length <= seg['end_time']:
                clip = (round(current_start, 2), round(current_start + clip_length, 2))
                if not overlaps(clip, used_ranges):
                    selected_clips.append({'start': clip[0], 'end': clip[1], 'value': seg['value']})
                    used_ranges.append(clip)
                    if len(selected_clips) == max_clips:
                        return selected_clips
                current_start += clip_length
            continue

        # CASE 2: Segment is shorter than clip_length
        # Try centering a 10s window on the segment
        clip_start = max(0, seg_center - clip_length / 2)
        clip_end = min(video_duration, clip_start + clip_length)
        clip = (round(clip_start, 2), round(clip_end, 2))

        if not overlaps(clip, used_ranges):
            selected_clips.append({'start': clip[0], 'end': clip[1], 'value': seg['value']})
            used_ranges.append(clip)
            if len(selected_clips) == max_clips:
                break

    return selected_clips


def overlaps(new_clip, used_clips):
    # Check if new_clip overlaps any previously used clip
    for used in used_clips:
        if not (new_clip[1] <= used[0] or new_clip[0] >= used[1]):
            return True
    return False

def download_clip(video_url: str, start_seconds: int, end_seconds: int, output_name: str):
    time_range = f"*{start_seconds}-{end_seconds}"
    output_template = os.path.join(storage_path, output_name + ".%(ext)s")

    cmd = [
        "yt-dlp",
        "--download-sections", time_range,
        "-f", "best",
        "-o", output_template,
        video_url
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Download completed and saved in: {storage_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")
    
def video_creation(video_url):
    clearing_storage()
    heat_map_data = get_heat_map(video_url)
    if heat_map_data:
        clips = extract_moments(heat_map_data, extract_multiplier)
        if clips:
            clips.sort(key=lambda clip: clip['start'])
            print("Extracted moments:", clips)
            i = 1
            for clip in clips:
                output_name = f"clip_{i}"
                download_clip(video_url, clip['start'], clip['end'], output_name)
                i += 1
        else:
            print("No moments extracted from the heat map.")
    else:
        print("No heat map data available for this video.")
    print(extract_moments)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=wVyu7NB7W6Y&ab_channel=Veritasium"
    video_creation(video_url)