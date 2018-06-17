'''
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
'''

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
    req_results = requests.get(yt_link)
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


class CommonNetworkYoutube(object):
    """
    Class for interfacing with youtube
    """

    def __init__(self, youtube_api_key):
        self.youtube_inst = youtubeapi.YoutubeAPI({'key': youtube_api_key})

    def com_net_yt_video_info(self, video_id):
        return self.youtube_inst.get_video_info(video_id)

    def com_net_yt_search_all(self, search_string):
        """
        Search playlists, channels and videos
        """
        return self.youtube_inst.search(search_string)

    def com_net_yt_search_video(self, search_string):
        """
        Search only Videos
        """
        return self.youtube_inst.search_videos(search_string)

    def com_net_yt_search_in_channel(self, search_string, channel_id):
        """
        Search only Videos in a given channel
        """
        video_list = self.youtube_inst.search_channel_videos(
            search_string, channel_id, 50)
        # TODO
        results = self.youtube_inst.search_advanced({'fake': 'param'})

    def com_net_yt_channel_by_name(self, channel_name):
        return self.youtube_inst.get_channel_by_name(channel_name)

    def com_net_yt_channel_by_id(self, channel_id):
        return self.youtube_inst.get_channel_by_id(channel_id)

    def com_net_yt_playlist_by_id(self, playlist_id):
        return self.youtube_inst.get_playlist_by_id(playlist_id)

    def com_net_yt_playlist_by_channel(self, channel_id):
        return self.youtube_inst.get_playlists_by_channel_id(channel_id)

    def com_net_yt_items_in_playlist(self, playlist_id):
        return self.youtube_inst.get_playlist_items_by_playlist_id(playlist_id)

    def com_net_yt_activities_by_channel(self, channel_id):
        return self.youtube_inst.get_activities_by_channel_id(channel_id)

    def com_net_yt_vid_id_from_url(self, url_name):
        return self.youtube_inst.parse_vid_from_url(url_name)
