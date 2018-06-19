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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_hardware_roku


@pytest.mark.parametrize(("filename"), [
    ("./cache/BigBuckBunny.ogv"),
    ("./cache/BigBuckBunny_512kb.mp4"),
    ("./cache/fake_video.mp4")])
def test_getmp4info(filename):
    """
    Test function
    """
    common_hardware_roku.getmp4info(filename)

# def extractimages(videoFile, directory, interval, mode=0, offset=0):


# def makebif(filename, directory, interval):


# def com_roku_create_bif(videoFile, first_image_offset=7, image_interval=10, option_mode=0):
