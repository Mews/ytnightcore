from youtubesearchpython import VideosSearch
from youtube import download_yt_mp3, search

videos = search("x for breakfast ken carson", limit=5)

for video in videos:
    print(video.title, video.author)