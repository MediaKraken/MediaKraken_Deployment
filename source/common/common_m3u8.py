'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

from . import common_file

# global statics
M3U_HEADER = 'EXTM3U\n'
M3U_LINE_HEADER = 'EXTINF:'

'''
#EXTM3U
#EXTINF:111,3rd Bass - Al z A-B-Cee z
mp3/3rd Bass/3rd bass - Al z A-B-Cee z.mp3
'''


def com_m3u_write(playlist_data, m3u_file_name):
    """
    Write out m3u from list
    """
    m3u_data = M3U_HEADER
    for playlist_item_seconds, playlist_item_name, playlist_item_filename in playlist_data:
        m3u_data += M3U_LINE_HEADER + playlist_item_seconds + ',' + playlist_item_name + '\n' \
                    + playlist_item_filename + '\n'
    common_file.com_file_save_data(m3u_file_name, m3u_data, False, False, None)
