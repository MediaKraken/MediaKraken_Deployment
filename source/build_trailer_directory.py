"""
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
"""

import os
from string import ascii_lowercase

from common import common_global

trailer_dir = [
    'trailer',
    'behind',
    'clip',
    'carpool',
    'featurette',
]


def build_trailer_dirs():
    for trailer_info in trailer_dir:
        for ndx in ascii_lowercase:
            for ndx2 in ascii_lowercase:
                os.makedirs(os.path.join(common_global.static_data_directory + '/meta/trailers',
                                         trailer_info, ndx, ndx2), exist_ok=True)
