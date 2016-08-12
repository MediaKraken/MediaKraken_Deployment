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
sys.path.append("../common")
from MK_Common_Hardware_HDHomeRun_Py import *


class TestCommonHardwareHDHomeRunPy(object):


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Hardware_HDHomeRun_Py.MK_Common_Hardware_HDHomeRun_API_Py()


    @classmethod
    def teardown_class(self):
        pass


    # discover items
    def Test_MK_Common_HDHomeRun_Discover(self):
        MK_Common_HDHomeRun_Discover()


    # item list
    def Test_MK_Common_HDHomeRun_List(self):
        MK_Common_HDHomeRun_List()


#    def get_tuner_vstatus(self, device_adapter):


#    def set_tuner_vchannel(self, device_adapter, vchannel):


#    def set_stream(self, device_adapter, vchannel, target_uri):


#    def get_supported(self, device_adapter):


#    def scan(self, device_adapter):


    def Test_get_count(self):
        get_count()

