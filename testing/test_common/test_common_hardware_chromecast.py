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
import pytest
import sys
sys.path.append('.')
from common import common_hardware_chromecast


class TestCommonHardwareChromecast(object):


    @classmethod
    def setup_class(self):
        self.db_connection = common_hardware_chromecast.CommonHardwareChromecast()


    @classmethod
    def teardown_class(self):
        pass


    # find chromecast as dict
    def test_com_chromecast_discover_dict(self):
        """
        Test function
        """
        self.db_connection.com_chromecast_discover_dict()


    # get detail by name
    def test_com_chromecast_info(self):
        """
        Test function
        """
        self.db_connection.com_chromecast_info()


    # get status by name
    def test_com_chromecast_status(self):
        """
        Test function
        """
        self.db_connection.com_chromecast_status()


    # connect to device
#    def MK_Chromecast_Connect_by_Name(self, key_name):


    # play youtube video
#    def MK_Chromecast_Play_YT(self, yt_id):


    # play media file
#    def MK_Chromecast_Play_Media(self, media_file, media_type):


    # send chromecast commands
#    def MK_Chromecast_Device_Command(self, command):


    def test_com_chromecast_device_close(self):
        """
        Test function
        """
        self.db_connection.com_chromecast_device_close()
