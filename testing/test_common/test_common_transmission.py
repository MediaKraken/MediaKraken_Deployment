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
from MK_Common_Transmission import *


class Test_MK_Common_Transmission_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_Transmission.MK_Common_Transmission_API()


    @classmethod
    def teardown_class(self):
        pass


    def test_MK_Common_Transmission_Get_Torrent_List(self):
        MK_Common_Transmission_Get_Torrent_List()


#    def MK_Common_Transmission_Add_Torrent(self, torrent_path):


#    def MK_Common_Transmission_Remove_Torrent(self, torrent_hash):


#    def MK_Common_Trnasmission_Name(self, torrent_no):


#    def MK_Common_Transmission_Torrent_Detail(self, torrent_no):


#    def MK_Common_Transmission_Torrent_Start(self, torrent_no):


#    def MK_Common_Transmission_Torrent_Stop(self, torrent_no):
