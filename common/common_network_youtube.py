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
        "https://www.youtube.com/feed/trending?gl=%s" % country_code).read(),'html.parser')
    links_set=source.find_all('a',href=True)
    for i in range(len(links_set)):
     if (links_set[i]['href'].strip('')[0:6]=='/watch'):
      link_list.append(links_set[i]['href'].strip(''))
    link_list2=["www.youtube.com"+link_list[i] for i in range(len(link_list)) if i%2==0]
    print(link_list2)
    return link_list2


def com_net_yt_search(search_term, max_results=25):
    youtube = build("youtube", "v3", developerKey="AIzaSyCwMkNYp8E4H19BDzlM7-IDkNCQtw0R9lY")
    search_response = youtube.search().list(
        q=search_term,
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    print(json.dumps(search_response, indent=4, sort_keys=True))
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))
    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")
