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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from . import common_google
from . import youtubeapi
import youtube_dl
import bs4 as bs
import urllib
from apiclient.discovery import build
import json


def com_net_yt_fetch_video_by_url(url_location, file_name):
    """
    # fetch video via youtube-dl
    """
    ydl_opts = {}
    ydl_opts["outtmpl"] = file_name
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_location])


def com_net_yt_fetch_video_list(search_string, max_files):
    """
    # fetch youtube trailers for title
    """
    return common_google.com_google_youtube_search(search_string, max_files)


def com_net_yt_trending(country_code='US'):
    link_list=[]
    source=bs.BeautifulSoup(urllib.urlopen(
        "https://www.youtube.com/feed/trending?gl=%s" % country_code).read(), 'html.parser')
    links_set=source.find_all('a',href=True)
    for i in range(len(links_set)):
        if (links_set[i]['href'].strip('')[0:6]=='/watch'):
            link_list.append(links_set[i]['href'].strip(''))
    link_list2=["www.youtube.com"+link_list[i] for i in range(len(link_list)) if i%2==0]
    return link_list2

class CommonNetworkYoutube(object):
    """
    Class for interfacing with youtube
    """
    def __init__(self):
        pass
        self.youtube_inst = youtubeapi.YoutubeAPI({'key': '/* Your API key here */'})

    def com_net_yt_video_info(self, video_id):
        return self.youtube_inst.get_video_info(video_id)

    # Search playlists, channels and videos
    def com_net_yt_search_all(self, search_string):
        return self.youtube_inst.search(search_string)

    # Search only Videos
    def com_net_yt_search_video(self, search_string):
        return self.youtube_inst.search_videos(search_string)

    # Search only Videos in a given channel
    def com_net_yt_search_in_channel(self, search_string, channel_id):
        video_list = self.youtube_inst.search_channel_videos(search_string, channel_id, 50)

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
