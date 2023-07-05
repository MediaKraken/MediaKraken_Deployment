import urllib.error
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

from . import common_google
from . import youtubeapi

def com_net_yt_top_tracks(playlist_type):
    yt_link = None
    if playlist_type == 'all':
        yt_link = 'https://www.youtube.com/playlist?list=PLFgquLnL59amLh5g4ZZoSl1Wf9e0_rco7'
    elif playlist_type == 'pop':
        yt_link = 'https://www.youtube.com/playlist?list=PLDcnymzs18LWrKzHmzrGH1JzLBqrHi3xQ'
    elif playlist_type == 'electronic':
        yt_link = 'https://www.youtube.com/playlist?list=PLFPg_IUxqnZNnACUGsfn50DySIOVSkiKI'
    elif playlist_type == 'house':
        yt_link = 'https://www.youtube.com/playlist?list=PLhInz4M-OzRUsuBj8wF6383E7zm2dJfqZ'
    elif playlist_type == 'electronic dance':
        yt_link = 'https://www.youtube.com/playlist?list=PLUg_BxrbJNY5gHrKsCsyon6vgJhxs72AH'
    elif playlist_type == 'pop rock':
        yt_link = 'https://www.youtube.com/playlist?list=PLr8RdoI29cXIlkmTAQDgOuwBhDh3yJDBQ'
    elif playlist_type == 'hip hop':
        yt_link = 'https://www.youtube.com/playlist?list=PLH6pfBXQXHEC2uDmDy5oi3tHW6X8kZ2Jo'
    elif playlist_type == 'rock':
        yt_link = 'https://www.youtube.com/playlist?list=PLhd1HyMTk3f5PzRjJzmzH7kkxjfdVoPPj'
    elif playlist_type == 'alt rock':
        yt_link = 'https://www.youtube.com/playlist?list=PL47oRh0-pTouthHPv6AbALWPvPJHlKiF7'
    if yt_link is not None:
        req_results = requests.get(yt_link, timeout=5)
        data = req_results.text
        soup = BeautifulSoup(data)
        images = soup.select(".yt-thumb-clip")
        imagelinks = []
        for image in images[9:len(images)]:  # First few images are useless
            imagelinks.append(image.img["data-thumb"])
        # Titles and Videolinks
        links = soup.find_all("a",
                              class_="pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link ",
                              limit=10)
        titles = []
        videolinks = []
        for link in links:
            titles.append(link.string.strip())
            videolinks.append("https://youtube.com" + link["href"])
        return imagelinks, titles, videolinks
    else:
        return None, None, None
