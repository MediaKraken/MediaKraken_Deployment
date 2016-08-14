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


class TestDatabaseMediaGames(object):


    @classmethod
    def setup_class(self):
        self.db_connection.connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # audited system list count
    def test_com_media_game_system_list_count(self):
        self.db_connection.com_media_game_system_list_count()
        self.db_connection.srv_db_rollback()


    # audited system list
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_com_media_game_system_list(self, offset, records):
        self.db_connection.com_media_game_system_list(offset, records)
        self.db_connection.srv_db_rollback()


    # audited game list by system count
    # def com_media_game_list_by_system_count(self, system_id):
#        self.db_connection.srv_db_rollback()


    # audited game list by system
    # def com_media_game_list_by_system(self, system_id, offset=None, records=None):
#        self.db_connection.srv_db_rollback()


    # audited games list count
    def test_com_media_game_list_count(self):
        self.db_connection.com_media_game_list_count()
        self.db_connection.srv_db_rollback()


    # audited games list
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100,100),
        (100000000,1000)])
    def test_com_media_game_list(self, offset, records):
        self.db_connection.com_media_game_list(offset, records)
        self.db_connection.srv_db_rollback()
