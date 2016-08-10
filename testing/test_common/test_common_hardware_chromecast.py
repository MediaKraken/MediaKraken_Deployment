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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
from MK_Common_Hardware_Chromecast import *


class Test_MK_Common_Hardware_Chromecast_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Hardware_Chromecast.MK_Common_Hardware_Chromecast_API()


    @classmethod
    def teardown_class(self):
        pass


    # find chromecast as dict
    def test_MK_Chromecast_Discover_Dict(self):
        MK_Chromecast_Discover_Dict()


    # get detail by name
    def test_MK_Chromecast_Info(self):
        MK_Chromecast_Info()


    # get status by name
    def test_MK_Chromecast_Status(self):
        MK_Chromecast_Status()


    # connect to device
#    def MK_Chromecast_Connect_By_Name(self, key_name):


    # play youtube video
#    def MK_Chromecast_Play_YT(self, yt_id):


    # play media file
#    def MK_Chromecast_Play_Media(self, media_file, media_type):


    # send chromecast commands
#    def MK_Chromecast_Device_Command(self, command):


    def test_MK_Chromecast_Device_Close(self):
        MK_Chromecast_Device_Close()

