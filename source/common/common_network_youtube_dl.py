'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import youtube_dl


def com_net_yt_fetch_video_by_url(url_location, file_name):
    """
    # fetch video via youtube-dl
    """
    ydl_opts = {}
    ydl_opts["outtmpl"] = file_name
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_location])
