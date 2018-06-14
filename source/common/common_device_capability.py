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

# put the "preferred" item first in the array, as it will default to that on no match
DEVICE_COMPATIBILITY = {
    'ATV': {
        'NP': {},
        'Shield': {},
        'S805': {},
        'S905': {},
    },
    # FLAC (up to 96kHz/24-bit)
    'Chromecast': {
        'V2': {'VidContainer': ['mp4', 'webm'],
               'VidCodec': ['x264', 'vp8'],
               'AudioCodec': ['aac', 'flac', 'mp3', 'ogg', 'opus', 'wav'],
               'AudioChannel': ['6.1'],
               'AudioPass': ['ac3', 'eac3'],
               'ImageFormat': ['bmp', 'gif', 'jpeg', 'png', 'webp'],
               'MaxImageRes': '1280x720',
               'MaxVideoRes': ['720/60', '1080/30']},
        'Ultra': {'VidContainer': ['mp4', 'webm'],
                  'VidCodec': ['x264', 'x265', 'vp8', 'vp9'],
                  'AudioCodec': ['aac', 'flac', 'mp3', 'ogg', 'opus', 'wav'],
                  'AudioChannel': ['6.1'],
                  'AudioPass': ['ac3', 'eac3'],
                  'ImageFormat': ['bmp', 'gif', 'jpeg', 'png', 'webp'],
                  'MaxImageRes': '1280x720',
                  'MaxVideoRes': '2160/60'}
    },
    'Fire': {
        'Stick': {},
        'TV': {},
    },
    'HDHomeRun': {
        'HDHR-US': 2,
        'HDHR-EU': 2,
        'HDHR3-US': 2,
        'HDHR3-DT': 2,
        'HDHR3-EU': 2,
        'HDHR3-CC': 3,
        'HDHR3-4DC': 4,
        'HDHR4-2US': 2,
        'HDHR4-2DT': 2,
        'HDHR4-2IS': 2,
        'HDTC-2US': 2,
        'HDHR5-2US': 2,
        'HDHR5-4US': 4,
        'HDHR5-2DT': 2,
        'HDHR5-4DT': 4,
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
                return_video_container = video_container  # no change
            else:
                return_video_container = device_model['VidContainer'][0]
            # determine vid codec to use
            if video_codec in device_model['VidCodec']:
                return_video_codec = video_codec  # no change
            else:
                return_video_codec = device_model['VidCodec'][0]
            # determine audio codec to use
            if audio_codec in device_model['AudioCodec']:
                return_audio_codec = audio_codec  # no change
            else:
                return_audio_codec = device_model['AudioCodec'][0]
            # determine audio channels to use
            if audio_channels in device_model['AudioChannel']:
                return_audio_channels = audio_channels  # no change
            else:
                return_audio_channels = device_model['AudioChannel'][0]
    return return_video_container, return_video_codec, return_audio_codec, return_audio_channels
