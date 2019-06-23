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


class TestDatabaseMetadataSports:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # metadata guid by imdb id
    # def db_meta_Sports_guid_by_thesportsdb(self, thesports_uuid):
    #        self.db_connection.db_rollback()

    def test_db_meta_sports_list_count(self):
        """
        Sports event count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_sports_list_count()

    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_meta_sports_list(self, offset, records):
        """
        Sports list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_meta_sports_list(offset, records)

    # fetch guid by event name
    # def db_meta_sports_guid_by_event_name(self, event_name):
#        self.db_connection.db_rollback()
