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
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class TestDatabasePostgresql(object):


    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # return tables sizes (includex indexes, etc)
    # query provided by postgresql wiki
    def test_srv_db_pgsql_table_sizes(self):
        self.db_connection.srv_db_pgsql_table_sizes()
        self.db_connection.srv_db_rollback()


    # return tables and row count
    # query provided by postgresql wiki
    def test_srv_db_pgsql_row_count(self):
        self.db_connection.srv_db_pgsql_row_count()
        self.db_connection.srv_db_rollback()


    # vacuum stats by day list
    @pytest.mark.parametrize(("days"), [
        (1),
        (60)])
    def test_srv_db_pgsql_vacuum_stat_by_day(self, days):
        self.db_connection.srv_db_pgsql_vacuum_stat_by_day(days)
        self.db_connection.srv_db_rollback()


    # vacuum table
    @pytest.mark.parametrize(("table_name"), [
        ('mm_media'),
        ('mm_media_fake_table')])
    def test_srv_db_pgsql_vacuum_table(self, table_name):
        self.db_connection.srv_db_pgsql_vacuum_table(table_name)
        self.db_connection.srv_db_rollback()


    # set isolation level
    # def srv_db_pgsql_set_isolation_level(self, isolation_level):
#        self.db_connection.srv_db_rollback()
