from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from video import Video
from typing import List


def search(query, limit=1) -> List[Video]:
    videos = []

    videos_search = VideosSearch(query, limit=limit)

    results = videos_search.result()["result"]

    for raw_data in results:
        videos.append(Video(raw_data=raw_data))
    
    return videos


def download_yt_mp3(url:str, output_path:str):
    ydl_options = {
    "format": "bestaudio",
    "outtmpl": output_path,
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }]
    }

    with YoutubeDL(ydl_options) as ydl:
        ydl.download([url])