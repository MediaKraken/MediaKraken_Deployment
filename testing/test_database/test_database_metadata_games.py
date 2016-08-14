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


class TestDatabaseMetadataGames(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.srv_db_close()


    # return game system data
    # def srv_db_meta_game_system_by_guid(self, guid):
#        self.db.srv_db_rollback()


    # def srv_db_meta_game_system_list_count(self):
    def Test_srv_db_meta_game_system_list_count(self):
        self.db.srv_db_meta_game_system_list_count()
        self.db.srv_db_rollback()


    # return list of game systems
    # def srv_db_meta_game_system_list(self, offset=None, records=None):
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_meta_game_system_list(self, offset, records):
        self.db.srv_db_meta_game_system_list(offset, records)
        self.db.srv_db_rollback()


    # return list of games count
    # def srv_db_meta_game_list_count(self):
    def Test_srv_db_meta_game_list_count(self):
        self.db.srv_db_meta_game_list_count()
        self.db.srv_db_rollback()


    # return list of games
    # def srv_db_meta_game_list(self, offset=None, records=None):
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_srv_db_meta_game_list(self, offset, records):
        self.db.srv_db_meta_game_list(offset, records)
        self.db.srv_db_rollback()


    # return game data
    # def srv_db_meta_game_by_guid(self, guid):
#        self.db.srv_db_rollback()


    # game list by system count
    # def srv_db_meta_game_by_system_count(self, guid):
#        self.db.srv_db_rollback()


    # game list by system count
    # def srv_db_meta_game_by_system(self, guid, offset=None, records=None):
#        self.db.srv_db_rollback()


    # game by sha1
    # def srv_db_meta_game_by_sha1(self, sha1_hash):
#        self.db.srv_db_rollback()


    # game by name and system short name
    # def srv_db_meta_game_by_name_and_system(self, game_name, game_system_short_name):
#        self.db.srv_db_rollback()
