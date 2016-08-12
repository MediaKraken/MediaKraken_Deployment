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
from com_Hardware_Synology import *


class TestCommonSynology(object):


    @classmethod
    def setup_class(self):
        self.db = com_Hardware_Synology.com_Synology_API()


    @classmethod
    def teardown_class(self):
        pass


# connect to synology    
# def com_Synology_Connect(self, addr, user_name, user_password):


    # get nas info
    def Test_com_Synology_Info(self):
        com_Synology_Info()


    # get share list
    def Test_com_Synology_Shares_List(self):
        com_Synology_Shares_List()

