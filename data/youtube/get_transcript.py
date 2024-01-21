import json
import scrapetube
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List

def extract_channel_name(channel_url: str) -> str:
    # Split the URL by '/' and get the last part
    parts = channel_url.split('/')
    channel_name = parts[-2]
    
    # Remove any query parameters
    if '?' in channel_name:
        channel_name = channel_name.split('?')[0]
    
    return channel_name[1:]

def get_all_video_transcript(channel_url: str, output_file: str) -> List[dict]:

    video_generator = scrapetube.get_channel(channel_url=channel_url)
    data = []
    for video in video_generator:
        video_id = video["videoId"]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except:
            # some videos don't have transcripts
            # this is an example: https://youtu.be/qQIjts6F-aI?si=vcdSUxtv27jHbvpJ
            continue

        video_title = "No Title Available"
        try:
            video_title = video.get("title", "No Title Available")
            video_title = video_title["runs"][0]["text"]
        except:
            video_title = "No Title Available"

        text_transcript = "\n".join([entry["text"] for entry in transcript])
        data.append({"title": video_title, "transcript": text_transcript})

    # Save data to JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return data

channel_urls = [
    "https://www.youtube.com/@flyteorg/videos",
    "https://www.youtube.com/@union-ai/videos",
]

for channel_url in channel_urls:
    channel_name = extract_channel_name(channel_url)
    output_file = f"{channel_name}_video_transcripts.json"
    video_data = get_all_video_transcript(channel_url, output_file)
    print(channel_url, len(video_data)) # flyte 180, union 20

# channel_url = "https://www.youtube.com/@flyteorg/videos"
# output_file = "flyteorg_video_transcripts.json"
# video_data = get_all_video_transcript(channel_url, output_file)

# channel_url = "https://www.youtube.com/@union-ai/videos"
# output_file = "union-ai_video_transcripts.json"
# video_data = get_all_video_transcript(channel_url, output_file)

