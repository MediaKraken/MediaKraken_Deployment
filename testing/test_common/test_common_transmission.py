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
from common import common_transmission


class TestCommonTransmission(object):


    @classmethod
    def setup_class(self):
        self.transmission_connection = common_transmission.CommonTransmission()


    @classmethod
    def teardown_class(self):
        pass


    def test_common_transmission_get_torrent_list(self):
        """
        Test function
        """
        self.transmission_connection.com_transmission_get_torrent_list()


#    def common_transmission_Add_Torrent(self, torrent_path):


#    def common_transmission_Remove_Torrent(self, torrent_hash):


#    def com_Trnasmission_Name(self, torrent_no):


#    def common_transmission_Torrent_Detail(self, torrent_no):


#    def common_transmission_Torrent_Start(self, torrent_no):


#    def common_transmission_Torrent_Stop(self, torrent_no):
