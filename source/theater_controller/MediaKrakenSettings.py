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

import json

# base mediakraken settings
mediakraken_settings_base_json = json.dumps([
    {'type': 'title',
     'title': 'MediaKraken Server Settings'},
    {'type': 'string',
     'title': 'MediaKraken Server Host/IP',
     'desc': 'Hostname or IP of MediaKraken server to connect to',
     'section': 'MediaKrakenServer',
     'key': 'host'},
    {'type': 'numeric',
     'title': 'MediaKraken Server Port',
     'desc': 'Port number for MediaKraken server',
     'section': 'MediaKrakenServer',
     'key': 'port'}])

# audio settings
mediakraken_settings_audio_json = json.dumps([
    {'type': 'title',
     'title': 'Audio Device/Channel'},
    {'type': 'options',
     'title': 'Channels',
     'desc': 'Number of audio channels to output',
     'section': 'Audio',
     'key': 'Channels',
     'options': ['7.1', '6.1', '5.1', '2.1']},
    {'type': 'options',
     'title': 'Output Device',
     'desc': 'Device to output audio',
     'section': 'Audio',
     'key': 'Default_Device',
     'options': ["Default Device", "Passthrough"]},
    {'type': 'title',
     'title': 'Audio Passthrough Settings'},
    {'type': 'bool',
     'title': 'Audio Passthrough',
     'desc': 'Enable audio passthrough for receiver',
     'section': 'Passthrough',
     'key': 'Enable'},
    {'type': 'bool',
     'title': 'DTS Passthrough',
     'desc': 'Receiver supports DTS passthrough',
     'section': 'Passthrough',
     'key': 'DTS'},
    {'type': 'bool',
     'title': 'DTS-HD Passthrough',
     'desc': 'Receiver supports DTS-HD passthrough',
     'section': 'Passthrough',
     'key': 'DTSHD'},
    {'type': 'bool',
     'title': 'DTS-X',
     'desc': 'Receiver supports DTS-X passthrough',
     'section': 'Passthrough',
     'key': 'DTSX'},
    {'type': 'bool',
     'title': 'AC-3 Dolby Digital Passthrough',
     'desc': 'Receiver supports AC-3 passthrough',
     'section': 'Passthrough',
     'key': 'AC3'},
    {'type': 'bool',
     'title': 'EAC-3 Dolby Digital Passthrough',
     'desc': 'Receiver supports EAC-3 passthrough',
     'section': 'Passthrough',
     'key': 'EAC3'},
    {'type': 'bool',
     'title': 'True-HD Passthrough',
     'desc': 'Receiver supports True-HD passthrough',
     'section': 'Passthrough',
     'key': 'TRUEHD'},
    {'type': 'bool',
     'title': 'Dolby Atmos Passthrough',
     'desc': 'Receiver supports Dolby Atmos passthrough',
     'section': 'Passthrough',
     'key': 'Atmos'}])

# video settings
mediakraken_settings_video_json = json.dumps([
    {'type': 'title',
     'title': 'Video Settings'},
    {'type': 'bool',
     'title': 'Blank Displays',
     'desc': 'Blank other displays in multimonitor environment',
     'section': 'Video',
     'key': 'Blank_Displays'},
    {'type': 'bool',
     'title': 'Fullscreen',
     'desc': 'Run application fullscreen for GUI and playback',
     'section': 'Video',
     'key': 'Fullscreen'},
    {'type': 'bool',
     'title': 'Fullscreen Window',
     'desc': 'Run application in windowed fullscreen mode',
     'section': 'Video',
     'key': 'Fullscreen_Window'},
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
