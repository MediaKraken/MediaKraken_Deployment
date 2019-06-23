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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseiradio:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

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

    @pytest.mark.parametrize(("active_station", "search_value", "offset", "records"), [
        (True, None, None, None),
        (True, None, 100, 100),
        (True, None, 100000000, 1000),
        (False, None, None, None),
        (False, None, 100, 100),
        (False, None, 100000000, 1000)])
    def test_db_iradio_list(self, active_station, search_value, offset, records):
        """
        # iradio list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_iradio_list(
            offset, records, active_station, search_value)
