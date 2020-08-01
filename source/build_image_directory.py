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

import os
from string import ascii_lowercase

image_dir = [
    'backdrop',
    'banner',
    'box_bluray',
    'box_cd',
    'box_dvd',
    'box_hddvd',
    'box_laserdisc',
    'box_uhd',
    'box_vhs',
    'chapter',
    'character',
    'fanart',
    'game',
    'game_box',
    'game_media',
    'logo',
    'media_bluray',
    'media_cd',
    'media_dvd',
    'media_hddvd',
    'media_laserdisc',
    'media_uhd',
    'media_vhs',
    'person',
    'poster',
    'profile',
    'still',
]


def build_image_dirs():
    for image_info in image_dir:
        for i in ascii_lowercase:
            os.makedirs(os.path.join('/mediakraken/web_app_sanic/static/meta/images',
                                     image_info, i))
    # since a-z won't be used
    os.makedirs('/mediakraken/web_app_sanic/static/meta/images/episodes', exist_ok=True)
