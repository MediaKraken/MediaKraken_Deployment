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

sys.path.append('.')
from common import common_hardware_chromecast


class TestCommonHardwareChromecast:

    @classmethod
    def setup_class(self):
        self.chrome_device = common_hardware_chromecast.CommonHardwareChromecast()

    @classmethod
    def teardown_class(self):
        pass

    # find chromecast as dict
    def test_com_chromecast_discover_dict(self):
        """
        Test function
        """
        self.chrome_device.com_chromecast_discover()

    # get detail by name
    def test_com_chromecast_info(self):
        """
        Test function
        """
        self.chrome_device.com_chromecast_info()

    # get status by name
    def test_com_chromecast_status(self):
        """
        Test function
        """
        self.chrome_device.com_chromecast_status()

    # connect to device
    #    def com_chromecast_connect_by_name(self, key_name):

    # play youtube video
    #    def com_chromecast_play_yt(self, yt_id):

    # play media file
    #    def com_chromecast_play_media(self, media_file, media_type):

    # send chromecast commands
    #    def com_chromecast_device_command(self, command):
