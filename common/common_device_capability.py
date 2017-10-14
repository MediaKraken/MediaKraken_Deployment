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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611


# put the "preferred" item first in the array, as it will default to that on no match
DEVICE_COMPATIBILITY = {
    'ATV': {
        'NP': {},
        'Shield': {},
        'S805': {},
        'S905': {},
        },
    'Chromecast': {
        'V2': {'VidContainer': ['mp4', 'webm'], 'VidCodec': ['x264', 'vp8'],
               'AudioCodec': ['aac', 'flac', 'mp3', 'ogg', 'opus'], 
               'AudioChannel': ['6.1'], 'AudioPass': ['ac3', 'eac3'],
               'ImageFormat': ['BMP', 'GIF', 'JPEG', 'PNG', 'WEBP'], 'MaxImageRes': '1280x720',
               'MaxRes': ['720/60', '1080/30']},
        'Ultra': {'MaxRes': '2160/60'}
        },
    'Fire': {
        'Stick': {},
        'TV': {},
        },
    'OrangePi': {},
    'Raspberry': {
        'P1': {},
        'P2': {},
        'P3': {},
        'Zero': {},
        },
    'Roku': {},
    'Webbrowser': {
        'Chrome': {},
        'Firefox': {},
        'IE': {},
        'Safari': {},
        },
}


def com_device_compat_best_fit(device_type, device_model, video_container,
        video_codec, audio_codec, audio_channels):
    """
    Determine best "fit" for video
    """
    return_video_container = None
    return_video_codec = None
    return_audio_codec = None
    return_audio_channels = None
    if device_type in DEVICE_COMPATIBILITY:
        if device_model in DEVICE_COMPATIBILITY[device_type]:
            # determine container to use
            if video_container in device_model['VidContainer']:
                pass # no change
            else:
                return_video_container = device_model['VidContainer'][0]
            # determine vid codec to use
            if video_codec in device_model['VidCodec']:
                pass # no change
            else:
                return_video_codec = device_model['VidCodec'][0]
            # determine audio codec to use
            if audio_codec in device_model['AudioCodec']:
                pass # no change
            else:
                return_audio_codec = device_model['AudioCodec'][0]
            # determine audio channels to use
            if audio_channels in device_model['AudioChannel']:
                pass # no change
            else:
                return_audio_channels = device_model['AudioChannel'][0]
    return (return_video_container, return_video_codec, return_audio_codec, return_audio_channels)
