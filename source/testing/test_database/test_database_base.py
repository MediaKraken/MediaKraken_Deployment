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


class TestDatabaseBase:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    @pytest.mark.parametrize(("resource_name"), [
        ('mm_media'),
        ('fake_table')])
    def test_db_table_index_check(self, resource_name):
        """
        # check for table or index
        """
        self.db_connection.db_rollback()
        self.db_connection.db_table_index_check(resource_name)

    @pytest.mark.parametrize(("table_name", "expected_result"), [
        ('mm_options_and_status', 1),
        ('fake_table', None)])
    def test_db_table_count(self, table_name, expected_result):
        """
        # return count of records in table
        """
        self.db_connection.db_rollback()
        assert self.db_connection.db_table_count(table_name) == expected_result

    @pytest.mark.parametrize(("query_string"), [
        ('select 1 from mm_media'),
        ('select fake_colum from fake_table')])
    def test_db_query(self, query_string):
        """
        # general run anything
        """
        self.db_connection.db_rollback()
        self.db_connection.db_query(query_string)
