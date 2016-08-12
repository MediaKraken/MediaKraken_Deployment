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
import logging
import urllib


def com_Metadata_Chart_Lyrics(artist_name, song_name):
    """
    Generate url link and fetch lyrics
    """
    lyric_text = urllib.urlopen('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?%s'\
        % urllib.urlencode({'artist' : artist_name, 'song' : song_name})).read()
    logging.debug(lyric_text)
    return lyric_text


#com_Metadata_Chart_Lyrics('Megadeath','Peace Sells')
#com_Metadata_Chart_Lyrics('Metallica','ride the lightning')
