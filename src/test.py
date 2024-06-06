from youtubesearchpython import VideosSearch
from youtube import download_yt_mp3, search

videos = search("x for breakfast ken carson", limit=1)

for video in videos:
    print(video.url)
    download_yt_mp3(video.url, "temp/song")