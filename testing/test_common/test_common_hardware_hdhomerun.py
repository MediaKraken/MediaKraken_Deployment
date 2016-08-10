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
from MK_Common_Hardware_HDHomeRun import *


class Test_MK_Common_Hardware_HDHomeRun_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Hardware_HDHomeRun.MK_Common_Hardware_HDHomeRun_API()


    @classmethod
    def teardown_class(self):
        pass


    # discover items
    def test_MK_Common_HDHomeRun_Discover(self):
        MK_Common_HDHomeRun_Discover()


    # item list
    def test_MK_Common_HDHomeRun_List(self):
        MK_Common_HDHomeRun_List()


    # item detail
#    def MK_Common_HDHomeRun_Detail(self, ndx):


    # firmware upgrade
#    def MK_Common_HDHomeRun_Upgrade(self, ndx, firmware_file):


    # set lock request
#    def MK_Common_HDHomeRun_Lock_Request(self, ndx):


    # release lock
#    def MK_Common_HDHomeRun_Lock_Release(self, ndx):


    # get lock owner
#    def MK_Common_HDHomeRun_Lock_Owner(self, ndx):


    # set tuner
#    def MK_Common_HDHomeRun_Set_Tuner(self, ndx, tuner_no):


    # get tuner status
#    def MK_Common_HDHomeRun_Get_Tuner_Status(self, ndx):
