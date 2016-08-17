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


def com_net_youtube_fetch_video_by_url(url_location, file_name):
    """
    # fetch video via youtube-dl
    """
    ydl_opts = {}
    ydl_opts["outtmpl"] = file_name
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_location])


def com_net_youtube_fetch_video_list(search_string, max_files):
    """
    # fetch youtube trailers for title
    """
    return common_google.com_google_youtube_search(search_string, max_files)
