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

from . import common_global


def com_meta_chart_lyrics(artist_name, song_name):
    """
    Generate url link and fetch lyrics
    """
    lyric_text = urllib.request.urlopen('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?%s'
                                        % urllib.parse.urlencode(
        {'artist': artist_name, 'song': song_name})).read()
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'stuff': lyric_text})
    return lyric_text

# com_meta_chart_lyrics('Megadeath','Peace Sells')
# com_meta_chart_lyrics('Metallica','ride the lightning')
