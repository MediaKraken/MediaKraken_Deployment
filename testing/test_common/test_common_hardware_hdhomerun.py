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
from com_Hardware_HDHomeRun import *


class TestCommonHardwareHDHomeRun(object):


    @classmethod
    def setup_class(self):
        self.db = com_Hardware_HDHomeRun.com_Hardware_HDHomeRun_API()


    @classmethod
    def teardown_class(self):
        pass


    # discover items
    def Test_com_HDHomeRun_Discover(self):
        com_HDHomeRun_Discover()


    # item list
    def Test_com_HDHomeRun_List(self):
        com_HDHomeRun_List()


    # item detail
#    def com_HDHomeRun_Detail(self, ndx):


    # firmware upgrade
#    def com_HDHomeRun_Upgrade(self, ndx, firmware_file):


    # set lock request
#    def com_HDHomeRun_Lock_Request(self, ndx):


    # release lock
#    def com_HDHomeRun_Lock_Release(self, ndx):


    # get lock owner
#    def com_HDHomeRun_Lock_Owner(self, ndx):


    # set tuner
#    def com_HDHomeRun_Set_Tuner(self, ndx, tuner_no):


    # get tuner status
#    def com_HDHomeRun_Get_Tuner_Status(self, ndx):
