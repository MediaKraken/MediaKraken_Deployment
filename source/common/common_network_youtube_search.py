"""
  Copyright (C) 2020 Quinn D Granfor <spootdev@gmail.com>

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

# https://github.com/alexmercerind/youtube-search-python
# pip install youtube-search-python

from youtubesearchpython import SearchPlaylists
from youtubesearchpython import SearchVideos


def com_net_yt_search(search_type='video', search_text=None, offset=1,
                      mode='json', max_results=20):
    if search_type == 'video':
        return SearchVideos(search_text, offset=offset, mode=mode,
                            max_results=max_results).result()
    else:
        return SearchPlaylists(search_text, offset=offset, mode=mode,
                               max_results=max_results).result()
