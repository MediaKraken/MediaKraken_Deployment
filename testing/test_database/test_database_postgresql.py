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


import pytest
import sys
sys.path.append("../common")
sys.path.append("../server") # for db import
import database as database_base


class Test_database_postgresql:


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # return tables sizes (includex indexes, etc)
    # query provided by postgresql wiki
    def test_MK_Server_Database_Postgresql_Table_Sizes(self):
        self.db.MK_Server_Database_Postgresql_Table_Sizes()
        self.db.MK_Server_Database_Rollback()


    # return tables and row count
    # query provided by postgresql wiki
    def test_MK_Server_Database_Postgresql_Row_Count(self):
        self.db.MK_Server_Database_Postgresql_Row_Count()
        self.db.MK_Server_Database_Rollback()


    # vacuum stats by day list
    @pytest.mark.parametrize(("days"), [
        (1),
        (60)])
    def test_MK_Server_Database_Postgresql_Vacuum_Stat_By_Day(self, days):
        self.db.MK_Server_Database_Postgresql_Vacuum_Stat_By_Day(days)
        self.db.MK_Server_Database_Rollback()


    # vacuum table
    @pytest.mark.parametrize(("table_name"), [
        ('mm_media'),
        ('mm_media_fake_table')])
    def test_MK_Server_Database_Postgresql_Vacuum_Table(self, table_name):
        self.db.MK_Server_Database_Postgresql_Vacuum_Table(table_name)
        self.db.MK_Server_Database_Rollback()


    # set isolation level
    # def MK_Server_Database_Postgesql_Set_Isolation_Level(self, isolation_level):
#        self.db.MK_Server_Database_Rollback()
