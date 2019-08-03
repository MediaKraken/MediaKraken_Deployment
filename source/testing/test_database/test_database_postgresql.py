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
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extensions import ISOLATION_LEVEL_READ_COMMITTED  # the default


class TestDatabasePostgresql:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    # query provided by postgresql wiki
    def test_db_pgsql_table_sizes(self):
        """
        # return tables sizes (includex indexes, etc)
        """
        self.db_connection.db_rollback()
        self.db_connection.db_pgsql_table_sizes()

    # query provided by postgresql wiki
    def test_db_pgsql_row_count(self):
        """
        # return tables and row count
        """
        self.db_connection.db_rollback()
        self.db_connection.db_pgsql_row_count()

    @pytest.mark.parametrize(("days"), [
        (1),
        (60)])
    def test_db_pgsql_vacuum_stat_by_day(self, days):
        """
        # vacuum stats by day list
        """
        self.db_connection.db_rollback()
        self.db_connection.db_pgsql_vacuum_stat_by_day(days)

    @pytest.mark.parametrize(("table_name"), [
        ('mm_media'),
        ('mm_media_fake_table')])
    def test_db_pgsql_vacuum_table(self, table_name):
        """
        # vacuum table
        """
        self.db_connection.db_rollback()
        self.db_connection.db_pgsql_vacuum_table(table_name)

    @pytest.mark.parametrize(("isolation_level"), [
        (ISOLATION_LEVEL_AUTOCOMMIT),
        (ISOLATION_LEVEL_READ_COMMITTED)])
    def test_db_pgsql_set_iso_level(self, isolation_level):
        """
        # set isolation level
        """
        self.db_connection.db_rollback()
        self.db_connection.db_pgsql_set_iso_level(isolation_level)

    @pytest.mark.parametrize(("table_name", "expected_result"), [
        ('mm_media', 'mm_media'),
        ('mm_media_fake_table', None)])
    def test_db_pgsql_table_exits(self, table_name, expected_result):
        self.db_connection.db_rollback()
        assert self.db_connection.db_pgsql_table_exits(
            table_name) == expected_result
