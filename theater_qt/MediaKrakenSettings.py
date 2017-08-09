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
                                 'Run application in windowed fullscreen mode']}}

'''


    {'type': 'options',
     'title': 'Resolution',
     'desc': 'Set resolution for GUI and playback',
     'section': 'Video',
     'key': 'Resolution',
     'options': ['Window Size', 'Screen Size', '(4k) 3840 x 2160', '1920x1080p', '1920x1080i',
         '1280x720p', '1280x720i']},
    {'type': 'options',
     'title': 'Main Display',
     'desc': 'Select main screen for GUI and playback',
     'section': 'Video',
     'key': 'Display_Screen',
     'options': ['Display #1', 'Display #2', 'Display #3', 'Display #4']},
    {'type': 'options',
     'title': 'Sleep Mode',
     'desc': 'Select timer for entering sleep mode',
     'section': 'Video',
     'key': 'Sleep_Time',
     'options': ['Never', '3 min', '10 min', '15 min', '30 min', '1 hour', '3 hour']}])

# library settings
mediakraken_settings_library_json = json.dumps([
    {'type': 'title',
     'title': 'Library Settings'},
    {'type': 'bool',
     'title': 'Show Plot of Unwatched',
     'desc': 'Show the plot of unwatched media',
     'section': 'Library',
     'key': 'Show_Plot_Unwatched'},
    {'type': 'options',
     'title': 'Flatten TV Show Seasons',
     'desc': 'Whether to display season(s) in directories',
     'section': 'Library',
     'key': 'Flatten_TV_Show_Seasons',
     'options': ['If Only One Season', 'Always', 'Never']},
    {'type': 'bool',
     'title': 'Group Movies',
     'desc': 'Group media into known collections',
     'section': 'Library',
     'key': 'Group_Movies_in_Sets'}])

# playback settings
mediakraken_settings_playback_json = json.dumps([
    {'type': 'title',
     'title': 'Media Playback Settings'},
    {'type': 'options',
     'title': 'Preferred audio stream',
     'desc': 'Set language for preferred audio stream',
     'section': 'Playback',
     'key': 'Preferred_Audio_Language',
     'options': ['Original Stream Language', 'English']},
    {'type': 'bool',
     'title': 'Play next media',
     'desc': 'Automatically start next media file after end of media',
     'section': 'Playback',
     'key': 'Play_Next_Media_Automatically'}])

'''