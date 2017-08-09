'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

# base mediakraken settings
mediakraken_settings_base_json =\
    {'MediaKrakenServer': {'Host': None, 'Port': None},
    'Audio': {'Channels': ['7.1', '6.1', '5.1', '2.1'],
    'Default_Device': ["Default Device", "Passthrough"],
    'Enable audio passthrough for receiver': False,
    'Receiver supports DTS passthrough': False,
    'Receiver supports DTS-HD passthrough': False,
    'Receiver supports DTS-X passthrough': False,
    'Receiver supports AC-3 passthrough': False,
    'Receiver supports EAC-3 passthrough': False,
    'Receiver supports True-HD passthrough': False,
    'Receiver supports Dolby Atmos passthrough': False},
    'Video': {'Blank Displays': ['Blank other displays in multimonitor environment',\
                                 'Run application fullscreen for GUI and playback',\
                                 'Run application in windowed fullscreen mode'],
              'Resolution': ['Window Size', 'Screen Size', '(4k) 3840 x 2160', '1920x1080p',
                             '1920x1080i', '1280x720p', '1280x720i'],
              'Main Display': ['Display #1', 'Display #2', 'Display #3', 'Display #4']},
    'Sleep Mode': ['Never', '3 min', '10 min', '15 min', '30 min', '1 hour', '3 hour'],
    'Library': {'Show Plot of Unwatched': False,
                'Flatten TV Show Seasons': ['If Only One Season', 'Always', 'Never'],
                'Group Movies': False},
    'Playback': {'Preferred Audio': ['Original Stream Language', 'English'],
                 'Play Next Media': False}}
