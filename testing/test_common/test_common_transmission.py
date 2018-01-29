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
import pytest  # pylint: disable=W0611
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

    def test_com_trans_get_torrent_list(self):
        """
        Test function
        """
        self.transmission_connection.com_trans_get_torrent_list()

#    def com_trans_add_torrent(self, torrent_path):


#    def com_trans_remove_torrent(self, torrent_hash):


#    def com_tran_name(self, torrent_no):


#    def com_trans_torrent_detail(self, torrent_no):


#    def com_trans_torrent_start(self, torrent_no):


#    def com_trans_torrent_stop(self, torrent_no):
