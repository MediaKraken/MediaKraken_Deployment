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
import database as database_base


class TestDatabaseiradio(object):

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open()

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("radio_channel"), [
        ('http://www.mediakraken.org'),
        ('http://www.mediakraken.org')])  # so it dupes
    def test_db_iradio_insert(self, radio_channel):
        """
        # insert iradio channel
        """
        self.db_connection.db_rollback()
        self.db_connection.db_iradio_insert(radio_channel)

    @pytest.mark.parametrize(("active_station"), [
        (True,),
        (False)])
    def test_db_iradio_list_count(self, active_station):
        """
        # iradio count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_iradio_list_count(active_station)

    @pytest.mark.parametrize(("active_station", "offset", "records"), [
        (True, None, None),
        (True, 100, 100),
        (True, 100000000, 1000),
        (False, None, None),
        (False, 100, 100),
        (False, 100000000, 1000)])
    def test_db_iradio_list(self, active_station, offset, records):
        """
        # iradio list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_iradio_list(active_station, offset, records)
