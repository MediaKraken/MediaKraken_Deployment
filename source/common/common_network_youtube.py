"""
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
"""

import urllib.error
import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

from . import common_google
from . import youtubeapi


def com_net_yt_fetch_video_list(search_string, max_files):
    """
    # fetch youtube trailers for title
    """
    return common_google.com_google_youtube_search(search_string, max_files)


def com_net_yt_trending(country_code='US'):
    link_list = []
    source = BeautifulSoup(urllib.request.urlopen(
        "https://www.youtube.com/feed/trending?gl=%s" % country_code).read(), 'html.parser')
    links_set = source.find_all('a', href=True)
    for i in range(len(links_set)):
        if (links_set[i]['href'].strip('')[0:6] == '/watch'):
            link_list.append(links_set[i]['href'].strip(''))
    link_list2 = ["www.youtube.com" + link_list[i]
                  for i in range(len(link_list)) if i % 2 == 0]
    return link_list2


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
